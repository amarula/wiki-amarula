====================================================
XLSX Import and Export, Android and iOS Side by Side
====================================================

.. note:: **TL;DR**
 Letting users get session data out of a mobile app as a real spreadsheet —
 and back in again — means picking an XLSX library per platform, agreeing on
 a sheet/header layout once, and then reimplementing it twice. We cover the
 library split (one read+write library on Android, a dedicated reader and a
 dedicated writer on iOS), the header-driven parsing that makes both importers
 resilient to column reordering, and the round-trip tests that keep the two
 independent implementations honest.

1. The problem
==============

An app that records structured sessions — timestamps, measurements, nested
sub-records — eventually gets asked for two things: let the user email the
data to someone who only has Excel, and let the user load an old export back
in. Neither feature is glamorous, but both have sharp edges:

- **The file has to open cleanly in real spreadsheet software.** Excel,
  Numbers and Google Sheets are unforgiving about malformed OOXML, so
  hand-rolling XML is a trap; a real library is worth the dependency.
- **Import has to survive a file the app didn't just write.** A user edits a
  cell, reorders a column, or opens an export from three app versions ago.
  Trusting a fixed column index breaks the first time someone inserts a
  column.
- **Two platforms, two ecosystems.** Android has one mature, batteries-included
  library for OOXML. iOS does not — which forces a different shape of solution
  entirely.

This article walks through how those constraints play out when the same
spreadsheet layout — multiple sheets, dynamic columns, a sentinel value for
missing sensor readings — is built independently on Android (Kotlin) and iOS
(Swift).

2. One library per direction, not per platform
================================================

Android gets away with a single dependency doing both jobs. iOS splits read
and write across two separate libraries, because no single actively
maintained Swift package currently does both well:

.. list-table::
   :header-rows: 1
   :widths: 15 20 20 45

   * - Platform
     - Reads
     - Writes
     - Why
   * - **Android**
     - Apache POI (``XSSFWorkbook``)
     - Apache POI (``XSSFWorkbook``)
     - One mature JVM library handles the full OOXML spec in both directions.
   * - **iOS**
     - CoreXLSX (pure Swift)
     - libxlsxwriter (C library)
     - CoreXLSX only reads; libxlsxwriter only writes. Swift has no single
       library as complete as POI, so the two directions use two different
       dependencies, bridged differently (CoreXLSX is native Swift,
       libxlsxwriter is C interop).

The iOS split has a real consequence for how the two directions feel to
write. Reading is idiomatic Swift:

.. code-block:: swift

   let file = try XLSXFile(filepath: url.path)
   guard let path = try file.parseWorksheetPaths().first,
         let worksheet = try file.parseWorksheet(at: path),
         let sharedStrings = try file.parseSharedStrings()
   else { return nil }

   for row in worksheet.data?.rows ?? [] {
       let values = row.cells.map { $0.stringValue(sharedStrings) }
       // classify columns, build domain objects
   }

Writing goes through raw C pointers instead, since libxlsxwriter has no
Swift-native API surface:

.. code-block:: swift

   let workbook = workbook_new("/path/to/export.xlsx")
   let sheet = workbook_add_worksheet(workbook, "Sessions")
   let dateFormat = workbook_add_format(workbook)
   format_set_num_format(dateFormat, "dd/MM/yyyy hh:mm:ss")

   worksheet_write_string(sheet, 0, 0, "Start Time", nil)
   worksheet_write_datetime(sheet, 1, 0, &lxwDate, dateFormat)

   workbook_close(workbook)

That second snippet is the one worth budgeting extra review time for:
``UnsafeMutablePointer`` plumbing around a C library is a different risk
profile from the rest of a typical SwiftUI codebase, and it is where most of
the export-side bugs tend to hide.

3. Agree on the schema once, implement it twice
=================================================

Because Android and iOS are separate native codebases here — not a shared
Kotlin Multiplatform module — nothing stops the two sheet layouts from
drifting apart except discipline. The fix that held up in practice: define the
header strings as an exhaustive enum on each platform (a Kotlin ``enum class``
on Android, a ``String, CaseIterable`` enum on Swift) and build every sheet's
header row by composing slices of that enum, rather than typing header
strings inline wherever a sheet gets built.

.. code-block:: kotlin

   enum class Header(val label: String) {
       START_TIME("Start Time"),
       FL_COLD_PRESSURE("FL Cold Pressure"),
       WEATHER_DEW_POINT("Weather DewPoint"),
       // ...
   }

   val pressureTempHeaders = baseHeaders + tireHeaders + weatherHeaders

The two enums still have to be kept in sync by hand across repos — this is
not a substitute for sharing code — but it turns "does iOS call it
``FL Cold Pressure`` or ``Cold Pressure FL``" from a runtime import bug into a
one-file diff review.

Both platforms also size the sheet dynamically rather than always emitting
every possible column: tire-pressure, absolute-pressure and tire-temperature
columns only appear if the sessions being exported actually contain that
data. A row of sessions with no densimeter readings produces a narrower
sheet than one that has them. That logic has to be duplicated too, and is a
natural place for the two platforms' exports to silently diverge if a column
is added on one side and forgotten on the other — worth a cross-platform test
fixture if you can manage one (more on testing in section 6).

4. A sentinel for "this reading is invalid"
=============================================

Sensor data has gaps: a pressure transducer that briefly disconnects, a
sample taken before a value was ready. Writing ``0`` for a missing reading is
actively worse than leaving it blank, because ``0`` is a plausible real value
that silently corrupts any downstream average. Both platforms instead apply a
custom cell number format that displays the text ``N/A`` while keeping the
underlying cell numeric (so formulas referencing the column still behave):

.. code-block:: kotlin

   val invalidFormat = workbook.createCellStyle().apply {
       dataFormat = workbook.createDataFormat().getFormat("\"N/A\"")
   }

.. code-block:: swift

   let invalidFormat = workbook_add_format(workbook)
   format_set_num_format(invalidFormat, "\"N/A\"")

The same idea shows up for durations: lap and split times are stored as
numbers but formatted ``hh:mm:ss.00`` so they read as times rather than raw
seconds, and dates get ``dd/MM/yyyy hh:mm:ss``. None of this is exotic Excel
functionality — it's the same handful of custom number formats on both
platforms — but it's the detail that makes an exported file look native to
someone opening it, instead of looking like a CSV that got lucky.

5. Importing: parse by header text, not by column index
==========================================================

The import side on both platforms makes the same architectural choice:
scan the header row once, and classify every column by matching its text
against known header substrings, rather than assuming column *N* always
means the same thing.

.. code-block:: kotlin

   val tirePressureColumns = headerRow.filter { isTirePressureHeader(it.text) }
   val tireTemperatureColumns = headerRow.filter { isTireTemperatureHeader(it.text) }
   val splitColumns = headerRow.filter { isSplitHeader(it.text) }

   // every data row is then read by column reference, not by position
   for (row in dataRows) {
       val pressures = tirePressureColumns.map { row.cell(it.reference)?.numericValue }
       // ...
   }

This pays off directly against the dynamic-header behavior from section 3: a
file exported with four tire-pressure columns imports fine into a build that
now expects five, and a column that moved because someone inserted a new one
upstream doesn't silently shift every value one slot to the left. The cost is
that a *renamed* header is invisible to both importers — a header-text typo
fix that ships without a migration note will quietly stop matching any old
export.

Where the two platforms differ is in what a parse failure means. Android
treats a malformed file as an exception: the whole import is wrapped in a
``try``/``catch`` around file IO, decoding and row parsing, logged, and
surfaced as a failure to the user. iOS's importer instead returns ``nil`` from
an otherwise non-throwing path for a corrupt file, an empty sheet, a missing
header row, or a shared-strings parse failure, with a ``print`` log and no
error detail reaching the UI. Both end up showing the user a generic
"import failed" message, but only one of them gives you a stack trace when
it happens in the field — worth normalizing to exceptions (or a typed
``Result``) on both sides if you're setting this pattern up fresh.

A platform-specific wrinkle on iOS: CoreXLSX reports cell references relative
to the row they came from, not an absolute sheet coordinate, so matching a
header column against a later data row needs the row number substituted back
into the reference by hand (turning ``A1`` into ``A47`` for row 47) before
the lookup works. It's a small amount of code, but it's the kind of detail
that's invisible until an importer starts dropping a specific column on rows
past the first page of data.

6. Round-tripping instead of mocking
======================================

Both platforms test import/export the same way, and it's the approach worth
copying: build a realistic set of domain objects against an in-memory
database, export them to a real XLSX file, reimport that file, and assert
field-by-field equality against the originals.

.. code-block:: kotlin

   @Test
   fun `pressure session survives export and import`() {
       val original = buildPressureSession()
       val file = exporter.export(listOf(original))
       val reimported = importer.import(file).sessions.first()
       assertEquals(original.tirePressures, reimported.tirePressures)
       assertEquals(original.weather, reimported.weather)
   }

This catches an entire class of bug that mocking the library would miss
entirely: a number format that round-trips through Excel's actual float
representation and comes back off by a rounding error, a header match that
works for the exact string literal in the test but not the string the real
exporter emits, or a sheet index that's wrong only once a second sheet type
exists. Neither platform tests the XLSX libraries themselves — that's Apache
POI's and CoreXLSX/libxlsxwriter's job — they test that *this app's* mapping
between domain objects and spreadsheet rows survives a full trip through a
real file.

7. What to decide before writing either importer
===================================================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Decision
     - What both platforms here chose
   * - Library per platform
     - One read+write library if your platform has one (Android/POI); a
       dedicated reader and a dedicated writer if it doesn't (iOS).
   * - In-memory vs. streaming
     - Both load the whole workbook in memory on export and import. Fine for
       session logs; revisit if a single export could run into the tens of
       thousands of rows.
   * - Column lookup
     - By header text, not position — resilient to reordering, blind to
       renames.
   * - Missing values
     - A custom number format displaying ``N/A``, not a blank cell or a ``0``.
   * - Failure mode
     - Pick one: throw with a message, or return nothing. Don't let the two
       platforms disagree, and don't let either one swallow the actual cause.
   * - Test strategy
     - Round-trip through the real library, not mocks.

.. tip::
   Shipping spreadsheet import/export, or any other file-format bridge,
   across a native Android and iOS app and want the two implementations
   reviewed for drift? Amarula Solutions provides Android and iOS
   development and architecture reviews.
   `Contact our mobile team <https://www.amarulasolutions.com/contact/>`_
