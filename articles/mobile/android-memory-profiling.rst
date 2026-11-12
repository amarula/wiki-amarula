====================================================================
Android Memory Profiling with the Task-Based Android Studio Profiler
====================================================================

.. note:: **TL;DR**
 Memory leaks and allocation churn show up as jank, stutter, or an app the
 system eventually kills to reclaim memory. Older write-ups (including an
 internal one of ours from 2022) describe a single combined CPU/Memory/Energy
 timeline with a dedicated **MEMORY** strip you click into. Current Android
 Studio replaced that with a **task-based Profiler**: you pick a named task
 — live telemetry, a heap dump, Java/Kotlin allocation tracking, native
 allocation tracking, or a LeakCanary integration — rather than one
 do-everything window. This article walks through the current workflow and
 what each task is actually for.

1. Why this still matters
==========================

Android's garbage collector only frees memory it can prove is unreachable.
Two different problems follow from that, and they need different tools:

- **Churn** — allocating objects faster than the collector can keep up with,
  which forces GC pauses at the wrong moment and shows up as skipped frames.
- **Leaks** — something still holds a reference to an object that should be
  unreachable (most often an ``Activity`` or ``Context``), so the collector
  can never free it. A leaked ``Activity`` doesn't just waste one instance's
  worth of memory — in a Compose app it also keeps the entire composition
  hierarchy and every state object underneath it alive.

Leaked memory accumulates even while your app sits in the background,
pressuring the whole system into more frequent GC elsewhere and, eventually,
getting your process killed outright — which is what a restart "for no
reason" after switching apps usually is.

2. Starting a profiling task
==============================

Before picking a task, Android Studio asks you to choose how the app is
launched:

- **Profile 'app' with low overhead** — runs a *profileable* build (your
  ``release`` variant). Lower overhead, but you can't record Java/Kotlin
  allocations or capture a heap dump from it.
- **Profile 'app' with complete data** — runs a *debuggable* build. Required
  for allocation recording and heap dumps, and the only mode that shows the
  **Interactions** timeline (user input and lifecycle events) on a device
  running API 26+.

Both buttons live under **More actions** in the run toolbar once you've
selected a run configuration. Launching either one opens the **Profiler**
pane, where the **Home** tab lists your running processes and, below that,
the available **Tasks**. Not every task is available for every process —
pick the right launch mode first if a task you need is grayed out.

Each task also has a **Start profiler task from** dropdown: **Now** attaches
to the process as it already is, **Startup** restarts the app and begins
recording before it finishes launching — the one you want if the thing
you're chasing happens during app start. Click **Start profiler task**, use
the app, then stop the recording; it's kept in **Past Recordings** for the
rest of the Studio session, or longer if you click **Export recording**.

3. Getting the big picture first: View Live Telemetry
========================================================

If you don't yet know *what* is wrong, start with the **View Live
Telemetry** task rather than jumping straight to a heap dump. This is the
closest current equivalent to the old combined CPU/Memory/Energy strip: it
shows, in real time, CPU usage (yours against the rest of the system),
a per-thread activity timeline (green = running, yellow = waiting on I/O,
gray = asleep), and a stacked memory-by-category graph. Use it to confirm
there's actually a spike worth chasing, and whether it lines up with user
interaction or with something happening on its own — before committing to
one of the heavier, more specific tasks below.

4. Capturing and reading a heap dump
======================================

The **Analyze Memory Usage (Heap Dump)** task captures every object on the
Java heap at the moment you trigger it. It's the right tool after an
extended session, when you want to check for objects that should have been
freed by now but weren't.

What you get back:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Meaning
   * - **Allocations**
     - Number of live instances of this class.
   * - **Shallow Size**
     - Java memory used by instances of this class alone.
   * - **Native Size**
     - Native memory backing this class (e.g. a ``Bitmap``'s pixel buffer).
       Not available below Android 7.0.
   * - **Retained Size**
     - Total memory kept alive *because* instances of this class exist —
       the number worth sorting by when you're hunting the biggest leak.

A few filters make the list usable instead of overwhelming:

- The **heap** dropdown narrows to the **app heap** (the default, and
  usually the only one you care about), the **image heap** (preloaded boot
  classes — these never move or disappear, ignore them), or the **zygote
  heap**.
- The **class** dropdown's **Show activity/fragment leaks** option filters
  straight to ``Activity``/``Fragment`` instances Studio believes are still
  reachable after they should have been destroyed — the fastest path to a
  confirmed leak. **Show project classes** hides everything from libraries
  and dependencies.
- Clicking a class opens its **Instance** list, and clicking an instance
  opens **Fields** and **References** — right-click either to jump straight
  to the retaining field or the source line that allocated it.

Compose apps don't produce ``Fragment`` leaks (single-activity
architecture), but the ``Activity`` leak check matters more there, not less:
leak the host `Activity` and the whole Compose tree and every
``MutableState`` under it goes with it. Also worth a dedicated pass starting
with **Narwhal 4**: the heap dump view flags duplicate bitmaps — the same
image decoded and held in memory more than once — with a yellow warning
triangle, filterable via **Filter by → Duplicate Bitmaps**.

5. Catching the leak as it happens: allocation tracking
==========================================================

A single heap dump tells you what's alive *right now*; it doesn't tell you
*where* an object was allocated or whether it should have been freed by the
next dump. **Track Memory Consumption (Java/Kotlin Allocations)** records
every allocation and deallocation over a time window instead of a single
instant — this is the task to reach for when a heap dump shows a suspicious
class but you need the call stack that created it.

By default it records **every** allocation, which can visibly slow the app
down while profiling if it allocates heavily; switch **Allocation Tracking**
to **Sampled** to collect at intervals instead of continuously. The garbage
icon forces a GC event mid-recording, the same way the old profiler's
trash-can button did — useful for confirming something survives a collection
it shouldn't.

Once stopped, the **Table** tab is sortable by **Total Count**
(allocations minus deallocations — what's still around) or by raw
**Allocations** (peak churn). Clicking into an instance shows its
**Allocation Call Stack**, and a **Visualization** tab aggregates the whole
time range by call stack and thread. If you're chasing a JNI reference leak
specifically, **View JNI heap** filters to objects referenced from native
code — useful since those references are released manually and don't follow
normal Java GC rules.

6. Native memory
==================

If your app has any native code — or even if it doesn't, since the
framework itself uses native memory for things like image decoding — a leak
can be entirely invisible to the Java-side tasks above. **Track Memory
Consumption (Native Allocations)**, built on the Perfetto `heapprofd`
backend, records native allocation call stacks the same way the Java task
records Java ones. It has to be started from **Startup**, not attached to a
running process, so plan for an app restart when you reach for it.

7. Two shortcuts worth knowing about
=======================================

Two more recent additions change the economics of leak-hunting enough to
mention on their own:

- **LeakCanary as a Profiler task** (Android Studio Quail 2+): rather than
  adding the LeakCanary library to your app and reading its on-device
  notifications, the Profiler can run the same analysis for you and surface
  results directly in Studio — moving the analysis off the test device and
  onto your development machine, which is both faster and lets you profile
  a release-shaped build without shipping LeakCanary in it.
- **Duplicate bitmap detection** in the heap dump view (Narwhal 4+, see
  section 4) — catches a specific, very common leak pattern (the same image
  decoded repeatedly instead of cached) without you having to spot it by
  reading retained sizes by hand.

8. What actually causes these leaks
======================================

The tools above find leaks; they don't explain them. In rough order of how
often each one shows up in review:

- A **static field, singleton, or long-lived object** holding an
  ``Activity`` or ``Context`` directly — use ``applicationContext`` instead
  when the reference needs to outlive the screen.
- A **non-static inner class** — an anonymous ``Runnable``, a ``Handler``
  callback, a listener — implicitly captures its outer ``Activity`` or
  ``Fragment`` and outlives it if it's posted with a delay or never removed.
- A **registered listener or observer that's never unregistered** —
  location updates, broadcast receivers, RxJava subscriptions left
  undisposed, coroutine scopes that outlive the screen they were launched
  from.
- In Compose specifically: a lambda or state holder that **captures
  ``Context``** and is held longer than the composition, or cleanup that
  belongs in a ``DisposableEffect``'s ``onDispose`` block but was never
  written.
- A **cache with no eviction policy** holding objects (bitmaps, in
  particular) well past the point they're still needed.

9. Provoking leaks instead of waiting for them
=================================================

Small leaks hide at the bottom of a heap dump until they've accumulated
enough to be worth noticing. Two reliable ways to force the issue instead of
waiting:

- **Rotate the device** repeatedly while the app is in different states.
  Rotation recreates the ``Activity``, which is exactly when a reference
  held by an async callback or a state holder outlives the screen it came
  from.
- **Background and foreground the app** repeatedly (home button, then
  switch back), which exercises the same lifecycle teardown without needing
  a physical rotation.

10. Beyond Android Studio
============================

Not every investigation needs the IDE attached. ``adb shell dumpsys
meminfo <package>`` gives a memory breakdown from the command line, and
Logcat surfaces GC events as they happen — both useful for a quick check or
for scripting against CI. A captured heap dump is saved as an ``.hprof``
file; if you want to analyze it with a non-Studio tool like ``jhat``, convert
it first with the ``hprof-conv`` tool shipped in
``{android_sdk}/platform-tools/``, since Android's `.hprof` format isn't the
same as the Java SE one:

.. code-block:: console

   $ hprof-conv heap-original.hprof heap-converted.hprof

.. tip::
   Chasing a memory leak, or want a performance review before a release
   ships? Amarula Solutions provides Android development, profiling, and
   architecture reviews.
   `Contact our mobile team <https://www.amarulasolutions.com/contact/>`_
