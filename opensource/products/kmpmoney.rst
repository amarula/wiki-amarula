========
KMPMoney
========

.. note:: **TL;DR**
   - **KMPMoney is an Apache-2.0 Kotlin Multiplatform library that pairs an arbitrary-precision decimal with an explicit Currency**, so amounts can't drift into floating-point error and can't be added across currencies by accident. Targets JVM, Android and iOS from one ``commonMain`` source set.
   - Shipped with lossless allocation/splitting, cash-denomination rounding, a pluggable exchange-rate seam, JSON serialization, 99 built-in ISO currencies, and an example Jetpack Compose app demonstrating every feature live.

.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

What is KMPMoney?
------------------

`KMPMoney <https://github.com/amarula/KMP-Money>`__ gives Kotlin Multiplatform
apps something a bare ``Double`` or a bare ``BigDecimal`` does not provide on
its own: a monetary amount that cannot silently go wrong. Every amount is a
``KmpMoney``, an arbitrary-precision decimal permanently paired with a
``Currency``, and every operation on it checks that pairing before it does any
math.

.. code-block:: kotlin

    import com.amarula.kmpMoney.Currency
    import com.amarula.kmpMoney.KmpMoney

    val price = KmpMoney.of("19.99", Currency.USD)
    val tax   = price.percentage(8.5)
    val total = price + tax

    println(total.toMoneyString()) // "$ 21.69"

The problem
-----------

Store a price as ``Double`` and binary floating point starts lying almost
immediately: repeated addition and rounding drift away from the exact decimal
a till or an invoice expects. Switch to a bare ``BigDecimal`` and the precision
problem is solved, but a new one opens up: nothing stops ``10.00`` meant as
dollars from being added to ``10.00`` meant as euros. The compiler sees two
identical numbers.

KMPMoney closes both gaps at once. Amounts are backed by
`kotlin-multiplatform-bignum <https://github.com/ionspin/kotlin-multiplatform-bignum>`__'s
arbitrary-precision ``BigDecimal``, and every ``KmpMoney`` carries its
``Currency`` as part of its identity, so a mismatch doesn't produce a wrong
answer: it throws immediately.

.. code-block:: kotlin

    val usd = KmpMoney.of("10.00", Currency.USD)
    val eur = KmpMoney.of("10.00", Currency.EUR)

    usd.add(eur)
    // IllegalArgumentException: Currency mismatch: USD vs EUR

How it works
-------------

``KmpMoney`` is an immutable, ``Comparable`` data class holding a private
``BigDecimal`` and a public ``Currency``. Nothing about it is tied to a
platform; the same class compiles unchanged to JVM, Android and iOS.

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Stage
     - What happens
   * - **Create**
     - ``KmpMoney.of(amount, currency)`` parses a decimal string, ``Number``,
       or ``BigDecimal`` and pairs it with a ``Currency``; ``ofMinorUnits()``
       instead divides an integer (e.g. cents) by the currency's own decimal
       places.
   * - **Operate**
     - ``add``, ``subtract``, ``multiply``, ``divide``, the percentage
       helpers, all run on the full-precision ``BigDecimal`` underneath. Every
       binary operation calls ``requireSameCurrency`` first and throws before
       touching the numbers if the currencies don't match.
   * - **Round**
     - Only when a result needs to become a real, payable amount:
       ``round(mode)`` or ``roundToCashDenomination(d)`` snap it to the
       currency's own decimal places, or to a cash denomination like the
       nearest ``0.05`` where small coins don't circulate.
   * - **Compare**
     - ``isGreaterThan``, ``isEqualTo``, ``coerceIn``, and full ``Comparable``
       support, all still currency-checked, operating on the unrounded value
       so a chain of arithmetic never drifts because of an earlier rounding
       step.
   * - **Export**
     - ``toMoneyString()`` / ``format()`` / ``toCompactString()`` render it for
       humans; ``toMap()`` and ``KmpMoneySerializer`` render it for storage and
       JSON.

**Files.** ``KmpMoney.kt`` is the core type, arithmetic, formatting, rounding,
factories, and the one file most apps call directly. ``Currency.kt`` is pure
metadata: decimal places, symbol, symbol position, localized name, flag URL,
no behaviour of its own. ``ExchangeRateProvider.kt`` is a single ``fun``
interface plus one extension function; it knows nothing about HTTP or caching,
on purpose. ``KmpMoneyCollectionExtensions.kt`` and
``KmpMoneyFlowExtensions.kt`` each do exactly one job, ``List<KmpMoney>`` and
``Flow<KmpMoney>`` respectively, and neither one can see the other.
``KmpMoneySerializer.kt`` is the only file that knows ``kotlinx.serialization``
exists.

What are the key features?
---------------------------

* **Arithmetic** — ``add``, ``subtract``, ``multiply``, ``divide``, and the
  ``+ - *`` operators, all currency-checked.
* **Percentages** — ``percentage``, ``addPercentage`` (markup/VAT),
  ``subtractPercentage`` (back out an embedded rate).
* **Allocation** — ``allocate(ratios)`` and ``split(n)`` divide an amount
  proportionally without losing a minor unit; remainder pennies go to the
  first slots.
* **Rounding** — ``round(mode)`` and ``roundToCashDenomination(d)``, e.g.
  snapping to the nearest ``0.05`` where small coins don't circulate.
* **Conversion** — ``convertTo(currency, rate)`` plus an
  ``ExchangeRateProvider`` seam; the library does no networking or caching of
  its own, you bring the rate.
* **Comparisons** — ``isGreaterThan``, ``isLessThan``, ``isEqualTo``,
  ``isBetween``, ``coerceAtLeast``, ``coerceAtMost``, ``coerceIn``, full
  ``Comparable``.
* **Formatting** — ``toMoneyString()``, ``format(showSymbol, useCode,
  groupingSeparator)``, ``toCompactString()`` → ``$ 1.5K``, ``$ 2.3M``.
* **Minor units** — ``toMinorUnits()`` / ``ofMinorUnits()`` for integer-cents
  storage, ``toMap()`` / ``fromMap()`` for key-value persistence.
* **Serialization** — ``KmpMoneySerializer`` for ``kotlinx.serialization``,
  round-trips as ``{"amount":"12.50","currency":"USD"}``.
* **Collections & Flow** — ``sum``, ``max``, ``min``, ``average``,
  ``sumMoneyOf`` on ``List<KmpMoney>``; ``sumMoney()``, ``totalByCurrency()``
  on ``Flow<KmpMoney>``.
* **Currency metadata** — decimal places, symbol, symbol position, localized
  display name, and a country-flag URL built into every ``Currency`` entry.

**99 ISO currencies. 3 platforms** (JVM, Android, iOS) **from 1 shared source
set. 0 network calls** made by the library itself.

Two ways to convert
--------------------

KMPMoney doesn't hardcode where exchange rates come from. There's a bare path
and a pluggable one, and both end up rounding the same way, to the target
currency's own decimal places, half-away-from-zero.

- ``convertTo(targetCurrency, rate)`` — the caller already has the rate, from
  its own cache, a prior API call, a fixed table, and hands it straight to the
  call.
- ``convertTo(targetCurrency, provider)`` — a provider implementing the
  single-method ``ExchangeRateProvider`` ``fun`` interface supplies the rate
  instead.

The trade-off is honest: either way, the library does zero networking and zero
caching. If an app needs live rates, it has to fetch and cache them itself.
What KMPMoney promises is only that whichever rate it's handed gets rounded
correctly.

What you get
-------------

Everything above lives on one type, so it composes: a converted amount can be
split, a split can be formatted, a formatted amount can still be compared.

.. code-block:: kotlin

    val price = KmpMoney.of("1234.5", Currency.USD)

    price.toMoneyString()    // "$ 1,234.50"
    price.toCompactString()  // "$ 1.2K"
    price.toMap()            // {amount=1234.50, currency=USD}

    Json.encodeToString(KmpMoneySerializer, price)
    // {"amount":"1234.50","currency":"USD"}

    KmpMoney.of("100.00", Currency.USD).split(3)
    // [33.34 USD, 33.33 USD, 33.33 USD]  -- sums back to exactly 100.00

Getting started
-----------------

.. list-table::
   :header-rows: 0
   :widths: 25 75

   * - **Kotlin**
     - 2.3.21
   * - **JVM target**
     - 21
   * - **Android**
     - ``minSdk`` 24, targets SDK 36
   * - **iOS**
     - ``arm64`` and the ``arm64`` simulator
   * - **kotlin-multiplatform-bignum**
     - 0.3.10 (pulled in transitively)

.. code-block:: kotlin

    dependencies {
        implementation("com.amarulasolutions:kmp-money:0.1.0")
    }

Or build it from source:

.. code-block:: bash

    git clone https://github.com/amarula/KMP-Money
    cd KMP-Money
    ./gradlew :kmp-money:test

A separate example module, a single-screen Jetpack Compose app, pairs every
category above with a small live demo backed by real ``KmpMoney`` calls, from
currency mismatches to JSON round-trips. Run it with ``./gradlew
:example:installDebug`` on a connected device or emulator.

Current status and limitations
---------------------------------

This is ``0.1.0``, pre-1.0: the public API can still move. A few other edges
are worth knowing before depending on it:

- **Currency is a closed, hardcoded enum.** 99 ISO currencies plus an
  ``UNKNOWN`` fallback. A currency added to ISO 4217 after this release
  doesn't exist until the enum is updated, and there is no way to register a
  custom one at runtime.
- **No exchange-rate fetching or caching, by design.** ``convertTo`` always
  needs a rate handed to it, from a literal, a provider, or otherwise; nothing
  in the library goes and fetches one itself.
- **Rounding defaults to half-away-from-zero everywhere.** A different mode
  has to be passed explicitly on every call that takes one; there's no global
  switch.
- **``allocate()`` / ``split()`` always give the remainder to the first
  slots**, in ratio order. There's no round-robin or largest-remainder
  alternative.
- **Pulling in KMPMoney pulls in Compose Multiplatform too.** ``Currency.kt``'s
  localized display names are Compose resources, and ``KmpMoney`` itself is
  ``@Stable``-annotated for Compose recomposition. A pure JVM backend service
  that only wants currency-safe arithmetic still gets the Compose runtime on
  its classpath.
- **Non-decimal subdivisions aren't modelled.** Everything is expressed in a
  currency's own decimal places; historical or commodity currencies with
  non-decimal minor units aren't represented.

Development
-------------

.. code-block:: bash

    ./gradlew :kmp-money:test                            # unit tests
    ./gradlew ktlintCheck detekt koverHtmlReport          # lint, static analysis, coverage
    ./gradlew :example:installDebug                       # the example app

Licence
--------

Apache License 2.0. Use it, modify it, bundle it inside a closed-source app,
no obligation to publish anything in return. Attribution via the ``LICENSE``
file, and keeping the notice on files you redistribute unmodified, is all it
asks.

.. tip::
   Building a Kotlin Multiplatform app that handles money and want currency
   bugs caught at compile time instead of in production? Amarula Solutions
   provides custom feature development, integration support, and commercial
   licensing for this project.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
