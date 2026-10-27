==========================================================================
Building a Custom I2C Peripheral for Embedded Linux: From VHDL to Yocto
==========================================================================

.. note:: **TL;DR**

   - We built the full hardware/software stack for a custom peripheral on a
     **Xilinx Zynq** target: an **I2C slave** designed in VHDL, verified with
     **VUnit/GHDL** and GTKWave, and exposed to userspace through a
     **Linux kernel driver**.
   - Everything is integrated into a **Yocto BSP** built with the
     **System Device Tree (SDT)** flow and ``kas``.
   - This article covers the general shape of the FSM design, the
     AXI/interrupt interface between hardware and software, the driver's
     event model, and the Yocto build pipeline.

|

Project Scope
-------------

A customer needed to test their master product, which normally interfaces
with a variety of sensors over I2C, across many different scenarios. That
meant building a custom I2C slave peripheral able to accept *any* address
and forward whatever the master sent to a CPU, plus a Linux kernel driver
to turn that raw traffic into something a userspace test application could
read and respond to.

The custom I2C slave didn't fit any off-the-shelf IP core, so this turned
into a full embedded systems effort: an I2C slave state machine in VHDL, an
AXI4-Lite register interface to make it addressable from software, a Vivado
block design wiring it into a Zynq PL alongside supporting peripherals, a
Linux kernel driver exposing it as a character device, and a Yocto BSP to
build and boot the whole thing:

#. Design a custom AXI4-Lite IP core in VHDL implementing an I2C slave
   state machine.
#. Verify the core with a VUnit/GHDL testbench suite, using GTKWave for
   waveform-level debugging.
#. Instantiate it in a Zynq PL block design alongside supporting
   peripherals, and export the hardware platform from Vivado.
#. Write a Linux kernel driver exposing the IP as a character device.
#. Integrate the whole stack into a custom Yocto BSP using the System
   Device Tree workflow and ``kas``.
#. Validate end-to-end on real hardware, both by hand and with automated
   hardware tests.

The reference platform is the AMD/Xilinx **ZC702** evaluation board
(Zynq-7000 XC7Z020), with the PL I/O routed to its FMC connectors through
LPC breakout boards for wiring and probing.

|

Why Build Custom Hardware Instead of Using a Standard Peripheral Core?
----------------------------------------------------------------------

A conventional I2C slave only has limited applications. It can have
features not needed for a specific project, or not accept transactions
which the customer would want to accept instead. It can have a different
way of managing signals or states and not fully represent the decisions of
the customer.

An example could be having a slave able to accept all addresses from the
master without any filter, letting userspace decide what to do with them.
Another example related to our project is the decision to do clock
stretching at specific moments of the transaction, always keeping the
protocol rules in mind, to let userspace craft a proper answer to give back
or make use of the data before starting a new transaction.

|

What Challenges Does a Project Like This Present?
-------------------------------------------------

**Bus timing is very important and strict.**
  I2C ``START``/``STOP`` conditions are defined purely by ``SDA``
  transitioning while ``SCL`` is high. A state machine that changes ``SDA``
  at the wrong moment generates a spurious ``START`` or ``STOP`` and
  desyncs the whole bus. Every state transition has to be reasoned about in
  terms of *which* clock edge it's safe to act on. Also, the sampling of
  these two lines was made on the system clock, so we needed a way to
  coordinate between the two and make sure the ``SDA`` and ``SCL`` signals
  were properly sampled.

**Clock stretching has to be bridged into a Linux interrupt model without creating any misalignment.**
  The hardware can pause indefinitely; the kernel driver has to represent
  "I need software's decision right now" as a single, unambiguous
  interrupt-driven event, and userspace has to be able to answer it
  asynchronously.

**The driver has to serve several independent hardware instances.**
  A single board can carry multiple instances of the core, each with its
  own interrupt line and its own userspace consumer, so the driver has to
  keep those instances fully independent by exposing each one as a
  character device.

**Everything has to stay in sync.**
  The register map in the VHDL, the register offsets used by the kernel
  driver, and the properties in the generated device tree all describe the
  same hardware instance and must agree on the communication model.

|

Designing the Core in VHDL
--------------------------

The IP core splits cleanly into two parts: an AXI4-Lite register interface
and the I2C state machine itself.

.. code-block:: text

   ┌───────────────────────── Custom I2C Slave Core ──────────────────────────┐
   │                                                                          │
   │   ┌──────────┐   ┌──────────┐   ┌──────────┐                             │
   │   │   ISR    │   │   CTL    │   │   DATA   │   Registers                 │
   │   └────┬─────┘   └────┬─────┘   └────┬─────┘                             │
   │        │              │              │                                   │
   │  AXI4-Lite ◄──────────┴──────────────┴────► State Machine ◄──► Debounce  ├── i2c_scl
   │        │                                         │             Debounce  ├── i2c_sda
   │        └─────────────────────────────────────────┴─────────────────► irq │
   │                                                                          │
   └──────────────────────────────────────────────────────────────────────────┘

AXI4-Lite is the standard ARM/Xilinx interface for this kind of peripheral,
where the hardware side and Linux must communicate. It allowed us to
integrate the VHDL and the Linux software side with ease, and to expose the
registers used to exchange data with the Linux driver and, consequently,
with userspace.

Software talks to the core through a small register file: an
interrupt-status register (``ISR``), a control register (``CTL``) the driver
writes its ACK/NACK/response decisions into, and a data register
(``DATA``) for the bytes actually being transmitted.

The State Machine
~~~~~~~~~~~~~~~~~

Internally, the core is built around a synchronous state machine that
tracks the phases of an I2C transaction: bus idle, address reception, a
wait state where the FSM clock-stretches until software has made a
decision, acknowledging, and data transfer. The exact number and naming of
states is an implementation detail that varies from project to project;
what matters is that every state acts according to the I2C protocol.

Verifying It Before Testing On The Hardware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The core is verified with `VUnit <https://vunit.github.io/>`__ driving
`GHDL <https://ghdl.github.io/ghdl/>`__, across three layers of testbenches:

- individual state-machine transitions;
- the standalone slave, end-to-end;
- the full AXI-wrapped IP.

Together they cover clock stretching, repeated starts, burst reads/writes,
mid-transaction soft resets, and rejected (NACK'd) transfers. When a
testbench fails, VUnit/GHDL can dump a waveform for the failing run, and
`GTKWave <https://gtkwave.sourceforge.net/>`__ is what we reach for to
actually see it: stepping signal-by-signal and edge-by-edge through
``SDA``/``SCL`` and the internal FSM state is a much faster way to find a
timing bug than staring at assertion failures alone.

Because functional simulation only gets you so far with bus timing bugs,
the core also carries a small ``DEBUG`` trace register that shifts in the
last few FSM state transitions — plus their ``ACK``/``NACK``/``START``/``STOP``
flags — on real hardware. More on why that matters
`below <#debugging-the-hardware-implementation>`__.

Thanks to this intensive testing, we were able to reach full coverage of
the VHDL code.

Why Simulation-First Pays Off Beyond Catching Bugs Early
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The register/interrupt handshake between hardware and software is a
*contract*, and once that contract is written down, it can be exercised in
simulation instead of waiting on the real hardware.

On this project, the same register operations the driver would eventually
issue — writing ``CTL`` to ACK or NACK, writing and reading ``DATA``,
reading ``ISR`` to pick up and clear an interrupt — were driven directly
over simulated AXI4-Lite transactions in the VUnit testbench, across the
same edge cases the driver has to handle: bursts, repeated starts, rejected
transfers, mid-transaction resets.

That gave the driver a contract that was already validated by the time it
was written, rather than one still being discovered on the fly against real
hardware. Its first real test was on the physical board, but against a
register interface whose behavior was no longer a moving target — one of
the main reasons we decided to adopt extensive simulation-based
verification from the very first days.

|

Writing the Linux Kernel Driver
-------------------------------

The Linux kernel driver turns hardware interrupts into well-defined events
for userspace, through the registers described above, and then turns
userspace's response back into register writes.

**Register access goes through** ``regmap``
  The registers are inspectable live at
  ``/sys/kernel/debug/regmap/<device>/registers`` without any other
  debugging tool.

**Interrupt handler**
  It reads the interrupt-status register, stashes the resulting event, and
  wakes anything waiting on it. Deciding *what to do* about that event —
  acknowledge or not, what data to send back — is left entirely to
  userspace. That keeps the driver small, keeps protocol policy out of
  kernel space, and means the response can be as complex or as slow as an
  application needs, since the hardware is already clock-stretching
  regardless.

**Userspace talks to it as a character device**
  One node per hardware instance: a board can carry several instances of
  the core, and each gets its own device, its own interrupt, and its own
  independent stream of events.

|

Integrating the Whole Stack into a Yocto Image
----------------------------------------------

This is where the modern Xilinx **System Device Tree (SDT)** flow comes in.
Vivado exports the PL design as a hardware description, which ``SDTGen``
turns into a System Device Tree archive; ``gen-machine-conf`` then consumes
that archive to generate a matching Yocto machine configuration and device
tree sources — the step that turns Vivado's address-editor decisions into a
Yocto ``MACHINE``. From there, building the image (and, separately, a
standalone cross-toolchain for application developers who just want to
compile against the driver's UAPI header) is a standard ``kas`` build.

The ``kas`` project layers upstream Yocto (``openembedded-core``,
``meta-openembedded``, ``meta-arm``, ``meta-openamp``,
``meta-virtualization``) and Xilinx's ``meta-xilinx`` on top of a
project-specific distro layer holding the board bits:

- kernel config fragments enabling the driver;
- the driver recipe itself;
- the target image recipe.

Keeping that layer separate from the generated machine configuration and
device tree means re-running the SDT flow after a hardware change never
clobbers project-specific policy — one of the sharper edges of this
toolchain if the two are allowed to mix.

|

Testing on Real Hardware
------------------------------------------

Once the board boots, the driver and IP core can be exercised by hand with
standard ``i2c-tools``, treating the character device as the "software
side" of the transaction and a second I2C tool as the bus master: a
transaction issued from the master side shows up as a readable event on the
character device, and writing a response back to it supplies the ACK/NACK
decision and any data byte, which the master then sees complete (or not) on
the bus. A single-byte read from address ``0x7f`` looks like this:

.. code-block:: console

   $ i2cget -y -a 2 0x7f &                              # master blocks, slave stretches SCL
   $ dd if=/dev/i2caa-0 bs=2 count=1 status=none | hexdump -n 2
   0000000 ff01                                         # type 0x01 = READ_REQUEST, data 0xff
   $ printf "\x01\x55" > /dev/i2caa-0                   # ACK, answer with 0x55
   0x55                                                 # printed by i2cget

The event carries ``0xff``, i.e. address ``0x7f`` shifted left with the
read bit set; writing the response releases the bus, and the master prints
the byte it received.

For regression testing, the same interaction is automated with ``pytest``
and `labgrid <https://labgrid.readthedocs.io/>`__ driving real hardware over
a ``CommandProtocol`` shell — checking that the driver loads, then walking
single-byte, multi-byte, and NACK'd transactions through the same tooling
used by hand during bring-up. Every scenario validated manually stays
covered on every subsequent change to the VHDL, the driver, or the BSP.

|

Debugging the Hardware Implementation
-------------------------------------

Simulation catches most logic bugs, but not every bus-timing issue shows up
in a testbench — some only appear against a real master's actual signal
characteristics. That's why we made use of the ``DEBUG`` trace register:
since it's exposed through the same ``regmap`` the driver already uses, it's
readable live at ``/sys/kernel/debug/regmap/<device>/registers`` with no
extra tooling.

When something on the physical bus doesn't behave, dumping it reconstructs
exactly which states the FSM passed through and which control flags were
set at each step — far more useful for root-causing a hardware issue than
reasoning from a raw logic-analyzer capture alone.

|

Checking Signals with an Oscilloscope
-------------------------------------

Once the tests were completed and the whole functionality was verified, we
also used an oscilloscope to check that the signals behaved as expected:
respecting all the timing requirements of the I2C standard, with no
unexpected spikes or glitches on the lines.

.. figure:: /images/i2c-fpga-oscilloscope-capture.png

    A single-byte write at 100 kHz, decoded by the oscilloscope

The capture shows the whole contract at work. The master sends ``START``
and the address byte (``0x55`` plus the write bit, decoded as ``0xaa``);
the slave then holds ``SCL`` low for about 176 µs while software decides,
and ``ACK``\ s. The data byte ``0x33`` follows, another ~130 µs of clock
stretching while userspace consumes it, a second ``ACK``, and finally
``STOP``. Those long flat stretches are the clock stretching from the I2C
slave. Time the request spends travelling through the interrupt,
the driver, and a userspace process — and the master waits for it
without ever seeing a protocol violation.

|

Conclusion
----------

That's the shape of the full path from an FPGA fabric state machine to a
byte arriving in a userspace application: a small register map, an
interrupt, a character device, and a Yocto machine, kept in sync from a
single source of truth in the hardware description — and verified in
simulation early enough that hardware and software work don't have to wait
on each other.

Further Reading
~~~~~~~~~~~~~~~

- `VUnit <https://vunit.github.io/>`__ and
  `GHDL <https://ghdl.github.io/ghdl/>`__ — open-source VHDL test framework
  and simulator
- `GTKWave <https://gtkwave.sourceforge.net/>`__ — waveform viewer
- `labgrid <https://labgrid.readthedocs.io/>`__ — embedded board control
  and testing library
- `kas <https://kas.readthedocs.io/>`__ — setup tool for BitBake-based
  projects
- `I2C-bus specification (NXP UM10204)
  <https://www.nxp.com/docs/en/user-guide/UM10204.pdf>`__

.. tip::
   Amarula Solutions designs custom FPGA IP cores, Linux kernel drivers,
   and Yocto BSPs for embedded products. Need a custom peripheral brought
   up end-to-end, from VHDL to userspace?
   `Contact our embedded team <https://www.amarulasolutions.com/contact/>`_
