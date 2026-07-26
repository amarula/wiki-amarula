====================================================================
Bianchina Test Board — An Open Hardware Debugging Platform
====================================================================

.. note:: **TL;DR**
   - **Bianchina** is an open hardware test and debugging board by Amarula Solutions, combining a logic analyzer, pattern generator, JTAG programmer, programmable power supply, and bus protocol analyzers in a single USB-connected platform.
   - We are actively seeking funding partners and manufacturing collaborators to bring Bianchina to mass production.

`Download the specifications (PDF) <../../../_static/bianchina-test-board-specs-v1.0.pdf>`__

.. raw:: html

    <br>

.. figure:: /images/bianchina-board-hero.png

    Bianchina Test Board — concept and front panel layout

What Is Bianchina?
===================

Bianchina is a **multi-function embedded development and debugging
platform** that consolidates the tools every embedded engineer needs
at their bench into a single USB-connected board. Instead of juggling a
separate logic analyzer, JTAG debugger, pattern generator, SD card
programmer, and lab power supply, Bianchina puts them all in one place
with a unified control interface.

The board is built around an **ARM9-based Cypress FX3 controller**
connected to the host PC over SuperSpeed USB 3.0, providing
375 MBps direct DMA data transfer for high-speed logic capture and
protocol analysis.

|

Board Architecture
====================

.. figure:: /images/bianchina-board-architecture.png

    Board architecture — Power & Control, Core Logic, and Analysis blocks

Bianchina is organized into three functional blocks:

**Power & Control**
  - DUT power supply with variable output (1.2V–3.3V, I²C controlled)
    plus a fixed +5V terminal block output
  - USB Type-C input with PD/QC 3.0 support — powered from a standard
    phone quick charger
  - Virtual switches: four DSTP relays for remote configuration of
    jumpers and reset lines
  - Integrated AC/DC measurement (up to 250VAC / 350VDC) via the FX3

**Core Logic**
  - **Cypress FX3 controller** (ARM926EJ-S, 32-bit, 512/256 KB SRAM) as
    the central brain, managing all board functions over USB 3.0/2.0
  - **FT2232H-based JTAG programmer** — compatible with OpenOCD and
    urJTAG, supports ARM SWD, FPGA, CPLD, and Flash programming;
    functions as I²C, SPI, or bit-bang interface at 1.5V–5V target
    voltage
  - **SD-Card Loader & Swap** — dual SD sockets with high-speed
    multiplexing for seamless data exchange to the DUT

**Analysis**
  - **Logic Analyzer**: 10 channels @ 100 MSps input, 100 MHz bandwidth
  - **Pattern Generator**: 8 channels @ 50 MSps, user-programmable
    LVCMOS (1.2V–3.3V), 5V-tolerant
  - **Protocol Analyzers**: built-in digital bus analyzers for SPI,
    I²C, UART, I²S, CAN, and parallel buses
  - Multiple trigger options including pin change and bus pattern
    detection

|

.. raw:: html

    <br>

Technical Specifications
==========================

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Feature
     - Specification
     - Notes
   * - Power Input
     - USB Type-C (PD/QC 3.0)
     - No data on input
   * - Logic Analyzer
     - 10 ch @ 100 MSps in, 8 ch @ 50 MSps I/O
     - 100 MHz bandwidth
   * - Processor
     - ARM926EJ-S (Cypress FX3)
     - 512/256 KB SRAM
   * - JTAG
     - FT2232H-based
     - OpenOCD/urJTAG compatible
   * - Voltage Levels
     - 1.2V–3.3V variable
     - 5V tolerant inputs
   * - USB
     - SuperSpeed USB 3.0 hub
     - 2 user ports + 2 internal
   * - SD Card
     - Dual socket with swap mux
     - SD 3.0 / eMMC 4.41
   * - Relays
     - 4x DSTP virtual switches
     - FX3-controlled via I²C
   * - Measurement
     - AC/DC up to 250VAC / 350VDC
     - Via FX3
   * - Protocols
     - SPI, I²C, UART, I²S, CAN, Parallel
     - Built-in bus analyzers

|

Why Bianchina?
================

Every embedded Linux developer knows the pain: you arrive at the lab and
need a logic analyzer to debug an SPI timing issue, a JTAG probe to
reflash a bricked board, an SD card writer to prepare a boot image, and
a programmable power supply to test brown-out behavior. Four different
tools, four different USB cables, four different software stacks —
and none of them talk to each other.

Bianchina consolidates all of these into a **single open hardware
design** with a unified interface. The FX3 controller orchestrates
everything, allowing automated test sequences that combine power
cycling, logic capture, protocol decoding, and firmware programming.

|

Open Hardware Design
=====================

Bianchina is an **open hardware project** by Amarula Solutions.
The board design, schematics, and firmware are intended for public
release, allowing:

- **Community contributions** to firmware and tooling
- **Custom derivatives** for specific test environments
- **Integration** with open-source tools like OpenOCD, urJTAG,
  PulseView/sigrok, and Labgrid

|

Call for Partners — Help Us Bring Bianchina to Production
===========================================================

Amarula Solutions has designed and prototyped Bianchina, and we believe
it fills a real gap in the embedded development tool ecosystem. We are
now seeking:

:Funding partners:
   Help cover tooling, component sourcing, and initial production run
   costs.

:Manufacturing collaborators:
   PCB assembly and test partners who can support small-to-medium volume
   production with the quality standards embedded engineers expect.

:Early adopters:
   Teams and organizations willing to test pre-production units and
   provide feedback that shapes the final product.

:Distributors:
   Partners interested in bringing Bianchina to the embedded tools
   market through established channels.

If your organization is interested in any of these roles, we want to
talk.

`Contact us about Bianchina → <https://www.amarulasolutions.com/contact/>`_

|

.. tip::
   Amarula Solutions provides custom hardware design, embedded Linux BSP
   development, and open hardware engineering services. Interested in
   collaborating on Bianchina or other embedded hardware projects?
   `Contact our hardware team <https://www.amarulasolutions.com/contact/>`_
