==================================================================================
Upgrading Patchwork from 2.1 to 3.2 — Django 1.11 to 5.1 and PostgreSQL 10 to 14
==================================================================================

.. note:: **TL;DR**

   - We migrated an internal **Patchwork** patch-tracking instance from
     **2.1.0 (2018)** to **3.2.1**, moving Django 1.11 → 5.1, Python 3.8 → 3.10,
     PostgreSQL 10 → 14, and replacing ``manage.py runserver`` with
     **gunicorn**.
   - The database migration itself takes **ten seconds** for ~4,800 patches.
     Everything difficult was around it: a legacy migration whose file no
     longer exists, PostgreSQL sequences the upgrade leaves broken, and an
     SMTP relay that had been quietly failing for years.
   - Six findings here are worth knowing before attempting this on any
     2.x instance — the sequence bug in particular will silently break patch
     ingestion days later if you miss it.

|

Why Upgrade At All
------------------

Patchwork 2.1.0 was released in June 2018 and depends on **Django 1.11**,
which has been out of security support since **April 2020**. The database
sat on **PostgreSQL 10**, end-of-life since **November 2022**, and the
service was served by ``manage.py runserver`` — Django's *development*
server — behind an Apache reverse proxy.

There is also a forward-looking reason. Patchwork is being rewritten in Go
as **4.0**, and its migration tool reads only a **3.x schema at Django
migration 0042 or later**. An instance at 2.1.0 cannot be exported. Reaching
3.2.1 is therefore not optional for anyone wanting a future path;
it is the bridge.

|

The Starting Point
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Component
     - Before
     - After
   * - Patchwork
     - 2.1.0 (June 2018)
     - 3.2.1
   * - Django
     - 1.11.29 (EOL April 2020)
     - 5.1
   * - Python
     - 3.8.20
     - 3.10
   * - PostgreSQL
     - 10.23 (EOL November 2022)
     - 14
   * - Application server
     - ``manage.py runserver``
     - gunicorn
   * - Database auth
     - password over TCP
     - peer auth over Unix socket

The instance held roughly 4,500 patches, 1,200 series, 3,800 comments and
five user accounts — small enough that the data migration is trivial, large
enough to be a realistic rehearsal.

The upstream documentation recommends stepping through intermediate releases
rather than jumping. That advice is about *testing*, not the database:
Django migrations are cumulative and a 2.1 → 3.2.1 hop applies cleanly
in one pass. The reason to rehearse is that the 3.0.0 migrations
(``0042_add_cover_model`` and ``0043_merge_patch_submission``) are
**irreversible and non-atomic** — a failure part-way leaves the schema
half-converted with no way back except a restore.

|

Strategy: Rehearse On A Copy
----------------------------

The single most valuable decision was to run the entire migration against a
restored copy first. Every problem documented below was found there, on a
throwaway database, rather than during a maintenance window.

The shape of it:

#. **Back up.** ``pg_dump -Fc`` the live database. The instance had never had
   a working backup — the only file resembling one was 0 bytes.
#. **Prepare the target cluster.** PostgreSQL 14 was already installed on the
   host (idle on a separate port), so no new server was needed.
#. **Build a new virtualenv** alongside the old one, so rollback never
   requires rebuilding anything.
#. **Deploy the new tree** to a sibling directory, leaving the running
   version untouched.
#. **Restore the dump into a scratch database and migrate it.** Verify row
   counts, render pages, then discard.
#. **Cut over in a maintenance window** by re-pointing a symlink.

Because the old cluster is only ever *read from*, rollback is a symlink flip
plus a static-file snapshot. Nothing about the migration is committed until
the moment you decide it is.

|

What Actually Broke
-------------------

None of the following appeared in the upgrade documentation. All six were
found by rehearsing or by testing paths a browser does not cover.

A Migration Recorded In The Database With No Matching File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``django_migrations`` table contained
``patchwork | 0020_auto_20180904_2313`` — a record of a migration that
exists nowhere: not in the live tree, not in the upstream 2.1.0 release, not
in 3.2.1. Someone had run ``makemigrations`` on the server in September 2018
and the resulting file was later deleted.

This turns out to be **harmless**. Django builds its migration graph from the
files present and ignores applied records it cannot resolve. The rehearsal
confirmed it — all 26 migrations from ``0027`` through ``0046`` applied
without complaint. Do not spend time hunting the file.

PostgreSQL Sequences The Migration Leaves Broken
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**This is the one that matters.** Migration ``0042`` populates
``patchwork_cover`` and ``patchwork_covercomment`` using raw ``INSERT``
statements with **explicit primary keys**. In PostgreSQL, supplying an
explicit ID does not advance the table's sequence. Both sequences were left
uninitialised while their tables held thousands of rows.

The symptom appears days later, not immediately: the next cover letter
imported from a mailing list is assigned a primary key that already exists,
and the insert fails on a duplicate key. On a patch tracker this means
**ingestion silently breaks for every series that carries a cover letter** —
the submissions that matter most.

Detect and repair after migrating:

.. code-block:: sql

   -- Any row where seq_at is below max_id, or NULL, will collide
   SELECT t.tbl, t.max_id, s.last_value AS seq_at
   FROM (
               SELECT 'patchwork_cover' AS tbl, (SELECT max(id) FROM patchwork_cover) AS max_id
     UNION ALL SELECT 'patchwork_covercomment', (SELECT max(id) FROM patchwork_covercomment)
   ) t
   LEFT JOIN pg_sequences s
     ON s.sequencename = replace(pg_get_serial_sequence(t.tbl, 'id'), 'public.', '');

   SELECT setval('patchwork_cover_id_seq',        (SELECT max(id) FROM patchwork_cover));
   SELECT setval('patchwork_covercomment_id_seq', (SELECT max(id) FROM patchwork_covercomment));

Using ``pg_get_serial_sequence`` matters because Django's ``RenameModel``
renames tables but **leaves sequences under their original names** — a
renamed table's sequence may still be called something quite different, and
the counter travels with it intact. Only tables built by raw ``INSERT`` are
affected.

Both ``setval`` calls must be run again after every future migration, since
Django recreates the sequences.

``collectstatic`` Must Precede The Service Restart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``ManifestStaticFilesStorage``, every ``{% static %}`` lookup resolves
through a JSON manifest that Django reads **once at process start** and
caches. Restarting before collecting leaves you serving a stale manifest and
returning ``500`` on every page that renders a stylesheet:

.. code-block:: text

   ValueError: Missing staticfiles manifest entry for 'js/jquery-3.6.0.min.js'

The error names a file that demonstrably exists on disk, which sends you
looking in entirely the right place for entirely the wrong reason. The order
is always **collect, then restart**.

The Static Directory Belonged To The Wrong User
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``STATIC_ROOT`` was owned by ``www-data`` (Apache) while the service ran as
``patchwork``, so ``collectstatic`` failed on its first file. Apache only
ever *reads* that directory, so the fix is to give it to the service user:

.. code-block:: bash

   sudo chown -R patchwork:patchwork /opt/patchwork/static

Do **not** solve this by running ``collectstatic`` as ``www-data``. Django
configures logging at startup and the handler opens a ``patchwork``-owned log
file, so every management command as that user dies with
``ValueError: Unable to configure handler 'file'`` before doing anything.

gunicorn Needs To Be Told What To Serve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trivial, but it cost time because ``Restart=always`` disguised it as a
crash-loop rather than a configuration error:

.. code-block:: text

   Error: No application module specified.

The service was up and down on a three-second cycle. The ``ExecStart`` line
must end with the WSGI application:

.. code-block:: ini

   ExecStart=/opt/virtualenvs/patchwork-3.2/bin/gunicorn \
       --workers 3 --bind 127.0.0.1:8100 --timeout 120 \
       --access-logfile - --error-logfile - \
       patchwork.wsgi:application

CSRF Fails Behind A TLS-Terminating Proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django **4.0** added ``Origin``-header checking to CSRF verification. With
Apache terminating TLS and proxying over plain HTTP, Django believes the
request arrived insecurely, compares the browser's
``Origin: https://...`` against ``http://...``, and returns ``403``.

.. code-block:: text

   Forbidden (403) — CSRF verification failed. Request aborted.

This affects **every POST on the site** — logins, patch updates,
everything — so it is not a cosmetic problem. Two changes fix it properly:

.. code-block:: apache

   # Apache vhost, inside the :443 block
   RequestHeader set X-Forwarded-Proto "https"

.. code-block:: python

   # settings/production.py
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

Setting ``CSRF_TRUSTED_ORIGINS`` also clears the 403 and needs no Apache
change, but leaves ``request.is_secure()`` false, so generated links stay
``http://``. Prefer the proxy header.

``parsemail.sh`` And The Interpreter It Finds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Incoming mail is piped from the MTA into ``patchwork/bin/parsemail.sh``.
In 3.x that script has **no leading** ``PW_PYTHON=`` assignment — the only
one is indented inside a ``[ -z "$PW_PYTHON" ]`` guard. A naive
substitution anchored to the start of the line matches nothing and silently
leaves the script falling back to bare ``python``, which on a host with
Python 2 present resolves to the wrong interpreter:

.. code-block:: text

   ImportError: No module named django

The consequence is worse than an error message. ``parsemail.sh`` ends with
``exit 0`` by design, so the MTA treats a failed parse as successful
delivery and **discards the message**. The website looks perfectly healthy
while quietly eating patches. Set the interpreter before the guard and grep
to confirm the edit landed:

.. code-block:: bash

   sudo sed -i '/^PATCHWORK_BASE=/a PW_PYTHON=/opt/virtualenvs/patchwork-3.2/bin/python' \
     patchwork/bin/parsemail.sh
   grep -n "PW_PYTHON" patchwork/bin/parsemail.sh

|

A Known Upstream Issue You Will Inherit
----------------------------------------

Upstream bug `#556 <https://github.com/getpatchwork/patchwork/issues/556>`__
(open, no fix released) leaves cover letters created *before* the v3
migration in **both** ``patchwork_cover`` and ``patchwork_patch``, the
duplicates identifiable by a ``NULL`` ``state_id``. On our instance that was
388 rows.

The practical impact is bounded. The default patch list applies an *Action
Required* state filter, and ``NULL`` matches no state, so they are hidden by
default — they appear only when browsing ``?state=*`` or through the REST
API. Replies to those older covers also attach to the patch URL rather than
the cover URL.

**Do not run the workaround posted in that issue thread.** It is unfinished:
it ends with a ``DELETE`` failing on a foreign key from ``patchwork_event``,
and the final ``DELETE`` was proposed but never reached. Let a future
upstream migration handle it.

|

Results
-------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Metric
     - Result
   * - Migrations applied
     - 26 (``0027`` → ``0046``), all successful
   * - Migration runtime
     - ~10 seconds
   * - Downtime
     - ~15 minutes end to end
   * - Data loss
     - none
   * - Log volume
     - 1.7 GB of unbounded access log → rotating, 32 MB × 5

Replacing ``runserver`` with gunicorn also eliminated the access-log growth
at its source: request lines now go to the journal rather than the
application log, where the system's own rotation applies.

|

Lessons Worth Carrying Forward
------------------------------

#. **Rehearse against a restored copy.** Every failure above was found on a
   throwaway database. The migration takes ten seconds; the rehearsal costs
   minutes and removes the entire class of "discovered at 2am" problems.
#. **Verify your edits landed.** Three times during this migration a
   substitution silently matched nothing and reported success. A ``grep``
   afterwards would have caught all three. This applies to mail-server
   configuration too — ``postmap`` before ``reload``, always.
#. **Test the paths a browser cannot reach.** The broken ``parsemail.sh``
   and the failing SMTP relay were both invisible from the web interface.
   Send a real message through the real path, and read the mail log.
#. **Run the version ladder in the right order.** Restore, then migrate, then
   repair sequences, then collect static, then restart. Interleaving these
   leaves the database in a state that misreports itself — we briefly had a
   ``django_migrations`` table claiming a fresh-install migration alongside
   ``0046`` while the schema was still 2.1.0-shaped.
#. **Keep the old environment until ordinary traffic has flowed.** The old
   tree, venv and database cluster cost nothing to leave in place and turn a
   bad surprise into a symlink flip.

|

.. note::

   Amarula Solutions runs and maintains open-source development
   infrastructure, including Patchwork, Gerrit, Jenkins and LDAP-based
   authentication. If you are planning a similar migration —
   `get in touch <https://www.amarulasolutions.com/contact/>`__.
