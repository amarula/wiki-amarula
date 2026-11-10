===================================================================
Kotlin Flow: Cold Streams, Hot Streams, and the Operators Between
===================================================================

.. note:: **TL;DR**

   - **Flow is Kotlin's coroutine-based stream type** — a suspending,
     cancellable alternative to callbacks, LiveData and RxJava for
     asynchronous and reactive data. A plain ``flow { }`` is **cold**: it runs
     from scratch for every collector. ``StateFlow`` and ``SharedFlow`` are
     **hot**: one running producer, shared by whoever is currently collecting.
   - Covers the transformation operators (``map``, ``filter``, ``transform``,
     ``zip``), the flattening operators (``flatMapConcat``, ``flatMapMerge``,
     ``flatMapLatest``), context switching with ``flowOn``, exception
     transparency with ``catch``/``retry``, buffering with ``buffer()``, and
     ``StateFlow``/``SharedFlow`` including ``stateIn``/``shareIn``.

|

A ``Flow<T>`` is an asynchronous stream of values, built directly on Kotlin
coroutines. Like ``LiveData`` and RxJava's ``Observable``, it implements the
observer pattern: a source produces values over time, and one or more
collectors react to them as they arrive. What Flow adds is that every step —
producing, transforming, and collecting — is a suspending function, so it
composes with the rest of a coroutine-based codebase without callbacks,
disposables, or a separate reactive runtime to learn.

Creating and collecting a Flow
-------------------------------

.. code-block:: kotlin

    val numbersFlow: Flow<Int> = flow {
        repeat(60) {
            emit(it + 1) // suspends until the collector is ready for it
            delay(1000)  // suspends this coroutine for a second
        }
    }

.. code-block:: kotlin

    lifecycleScope.launch {
        repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.numbersFlow.collect {
                binding.textTimer.text = it.toString()
            }
        }
    }

That second snippet is worth pausing on: ``collect`` inside a bare
``lifecycleScope.launch`` keeps running even while the screen is stopped (e.g.
the user switched apps), which wastes work and can crash on a view that no
longer exists. Current Android guidance wraps the collection in
``repeatOnLifecycle(Lifecycle.State.STARTED)`` instead — it cancels the
collection when the lifecycle drops below ``STARTED`` and restarts it when it
comes back, automatically.

Cold flows vs. hot flows
-------------------------

**Cold** — a plain ``flow { }`` builder does nothing until something calls
``collect`` on it, and it has no notion of a "subscriber list": every call to
``collect`` starts an entirely new, independent execution of the builder
block from the top. Two collectors on the same cold flow do not share a run;
they each get their own.

**Hot** — ``StateFlow`` and ``SharedFlow`` are active independently of
whether anything is collecting them. A value emitted into a hot flow is
delivered to every collector that happens to be actively collecting at that
moment; a collector that starts later simply missed it (unless replay is
configured, see below).

Flow builders
--------------

- ``flow { }`` — the general-purpose builder for emitting an arbitrary,
  possibly suspending sequence of values.
- ``flowOf(1, 2, 3)`` — builds a flow from a fixed, already-known set of
  values.
- ``someIterable.asFlow()`` — adapts an existing ``Iterable``, ``Sequence``,
  or range into a ``Flow``.
- ``channelFlow { }`` — the escape hatch for emitting from multiple
  coroutines or from a callback-based API; ``flow { }`` only allows emission
  from the single coroutine that is running the builder.

Transformation operators
--------------------------

.. code-block:: kotlin

    val numbers = (1..5).asFlow()
    numbers.map { it * 2 }.collect { print("$it ") }
    // 2 4 6 8 10

.. code-block:: kotlin

    val numbers = (1..5).asFlow()
    numbers.filter { it % 2 == 0 }.collect { print("$it ") }
    // 2 4

.. code-block:: kotlin

    val numbers = (1..5).asFlow()
    numbers.transform { value ->
        emit("A$value")
        emit("B$value")
    }.collect { print("$it ") }
    // A1 B1 A2 B2 A3 B3 A4 B4 A5 B5

``transform`` is the general case of ``map``/``filter``: the lambda can call
``emit`` any number of times (including zero), so it can map, filter, and
fan one value out into several, all in one operator.

.. code-block:: kotlin

    val a = (1..5).asFlow()
    val b = (6..10).asFlow()
    a.zip(b) { x, y -> x + y }.collect { print("$it ") }
    // 7 9 11 13 15

``zip`` pairs up the *n*-th value of each flow; it completes as soon as the
shorter of the two flows completes.

Flattening flows
------------------

A flow of flows — one upstream value that is itself transformed into another
flow — needs to be flattened into a single flow before it can be collected
normally. Kotlin offers three flattening operators that differ only in how
they handle concurrency between the inner flows.

``flatMapConcat`` — collects each inner flow to completion before starting
the next one. Output order is fully deterministic: every value of the first
inner flow, then every value of the second, and so on.

.. code-block:: kotlin

    val flow1 = flowOf("A", "B", "C")
    val flow2 = flowOf("D", "E", "F")
    val flow3 = flowOf("G", "H", "I")

    flowOf(flow1, flow2, flow3).flatMapConcat { it }.collect { print("$it ") }
    // A B C D E F G H I

``flatMapMerge`` — collects all inner flows concurrently and emits values as
they arrive. This is the one to reach for when the inner flows do independent
work (e.g. one network request per item) and don't need to wait on each
other — but the interleaving is **not guaranteed**; it depends on timing.
``concurrency`` is a parameter on ``flatMapMerge`` (default 16) that caps how
many inner flows run at once.

.. code-block:: kotlin

    flowOf(flow1, flow2, flow3).flatMapMerge { it }.collect { print("$it ") }
    // one possible order: A D G B E H C F I

``flatMapLatest`` — as soon as a new value arrives from the outer flow, the
inner flow currently being collected is cancelled, and collection restarts on
the new one. Only the most recently started inner flow ever gets to finish.
This is the operator behind "search-as-you-type": each keystroke should
cancel the in-flight request for the previous keystroke.

.. code-block:: kotlin

    val flow1 = flowOf("A", "B", "C")
    val flow2 = flowOf("D", "E", "F").onEach { delay(100) }
    val flow3 = flowOf("G", "H", "I")

    flowOf(flow1, flow2, flow3)
        .flatMapLatest { it }
        .collect { print("$it ") }
    // A B C G H I

``flow2``'s values never appear: by the time its first (delayed) emission
would have fired, ``flow3`` has already arrived on the outer flow and
cancelled it.

Context switching with flowOn
-------------------------------

A flow builder runs in whatever coroutine context the collector is running
in, by default. ``flowOn`` changes the context for everything **upstream** of
it, while leaving the collector's own context untouched:

.. code-block:: kotlin

    fun fetchItems(): Flow<Item> = flow {
        emit(database.loadItems()) // runs on Dispatchers.IO
    }.flowOn(Dispatchers.IO)

    // collector stays on whatever dispatcher it was already on,
    // e.g. Dispatchers.Main for updating a view

This is also the sanctioned way to switch dispatchers inside a flow builder:
calling ``withContext`` directly inside ``flow { }`` to change dispatcher is
not allowed and throws at runtime, because it would break the flow's
emission guarantees.

Exception transparency
------------------------

A flow builder is not supposed to catch exceptions thrown by its own
collector — doing so would mean the collector's own error handling could be
silently swallowed by a producer it doesn't control. The ``catch`` operator
only ever sees exceptions from **upstream** of it, never from the
``collect { }`` block after it:

.. code-block:: kotlin

    flow {
        emit(1)
        throw RuntimeException("Oops!")
        emit(2) // never reached
    }.catch { e ->
        emit(-1) // catch can itself emit a fallback value
    }.collect { value ->
        println(value)
    }
    // 1
    // -1

For transient failures — a flaky network call, for instance — ``retry`` (and
the more flexible ``retryWhen``) re-run the upstream flow from scratch when
the given predicate returns ``true``:

.. code-block:: kotlin

    fetchItems()
        .retry(3) { e -> e is IOException }
        .catch { emit(emptyList()) }
        .collect { show(it) }

Buffering and backpressure
----------------------------

By default, a collector's work and the producer's work happen in lockstep:
the producer suspends after each ``emit`` until the collector is ready for
the next value. If the collector is slower than the producer, that lockstep
*is* the backpressure — the producer is held back automatically, with no
unbounded queue building up anywhere.

``buffer()`` decouples the two: the producer can run ahead and park up to
``capacity`` values (64, by default) in a buffer while the collector catches
up, and only suspends once that buffer is full.

.. code-block:: kotlin

    fun slowFlow(): Flow<Int> = flow {
        repeat(10) {
            delay(100)
            emit(it)
        }
    }.buffer() // producer and collector no longer wait on each other

    fun main() = runBlocking {
        val time = measureTimeMillis {
            slowFlow().collect {
                delay(100)
                println("Received $it")
            }
        }
        println("Collected in $time ms") // ~1000ms instead of ~2000ms
    }

``buffer(capacity, onBufferOverflow)`` also accepts an overflow strategy —
``SUSPEND`` (the default), ``DROP_OLDEST``, or ``DROP_LATEST`` — for when a
full buffer should drop values instead of blocking the producer. Two related,
narrower operators cover common cases directly: ``conflate()`` keeps only the
latest value when the collector falls behind, and ``collectLatest`` cancels
and restarts the collector block itself whenever a new value arrives before
the previous one finished processing.

StateFlow and SharedFlow
--------------------------

Both are hot and multicast; they differ in what they guarantee about the
current value.

**StateFlow** is a specialized ``SharedFlow`` that always holds exactly one
current value, readable synchronously through its ``.value`` property, and
only emits when a new value is **not equal** to the current one — assigning
the same value twice is conflated into a single emission, not two.

.. code-block:: kotlin

    class CounterModel {
        private val counter = MutableStateFlow(0)
        val counterValue: StateFlow<Int> = counter.asStateFlow()

        fun incrementAtomically() {
            // atomic read-modify-write; safe under concurrent callers
            counter.update { count -> count + 1 }
        }

        fun incrementCounter() {
            // fine for single-writer cases; racy if called concurrently
            counter.value += 1
        }
    }

**SharedFlow** has no required initial value and no ``.value`` property; it
emits every value, including repeats, which makes it the right tool for
one-off events (navigation, snackbars, analytics) rather than persistent
state. Its ``replay`` parameter controls how many past values a brand-new
subscriber immediately receives on subscribing (``0`` by default — a
subscriber only sees values emitted after it starts collecting).

.. code-block:: kotlin

    class EventBus {
        private val events = MutableSharedFlow<Event>()
        val eventsValue: SharedFlow<Event> = events.asSharedFlow()

        suspend fun produceEvent(event: Event) {
            events.emit(event) // suspends until every current subscriber has it
        }
    }

Both can be collected by any number of collectors at once. To turn a
*regular* (cold) flow into a hot one that is shared across collectors and
starts/stops based on whether anyone is actually listening, use
``stateIn``/``shareIn`` with a ``SharingStarted`` policy — most commonly
``SharingStarted.WhileSubscribed()``, which starts the upstream flow when the
first collector appears and cancels it once the last one goes away:

.. code-block:: kotlin

    val uiState: StateFlow<State> = repository.dataFlow()
        .map { State.from(it) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = State.Loading,
        )

Which one to reach for
------------------------

- Reach for a plain ``flow { }`` when each collector should get its own,
  independent run of the producing logic — a one-shot network call, a
  database query, anything without a notion of "current state".
- Reach for **StateFlow** to hold and distribute a single source of truth for
  UI state: every collector always converges on the latest value, and
  reading ``.value`` gives a synchronous snapshot at any point.
- Reach for **SharedFlow** to broadcast discrete events to any number of
  collectors, especially when late subscribers arriving and leaving is
  expected, or when a configurable replay cache matters more than always
  having a current value.

.. tip::
   Building an Android or Kotlin Multiplatform app around reactive state and
   want a second opinion on the Flow architecture, or help untangling a
   LiveData/RxJava codebase onto coroutines? Amarula Solutions provides
   Android and Kotlin Multiplatform development and architecture reviews.
   `Contact our mobile team <https://www.amarulasolutions.com/contact/>`_
