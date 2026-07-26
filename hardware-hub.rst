======================
Hardware Development
======================

.. note:: **TL;DR**
   Amarula Solutions provides end-to-end hardware engineering services covering the full product lifecycle, from concept and schematic design through PCB layout, FPGA development, mechanical integration, and pre-compliance testing, with seamless handoff to embedded Linux BSP teams.

Amarula's hardware development team handles everything from initial
conceptualization through to small-scale production. Whether you need a
custom SoM carrier board, a battery-powered IoT sensor, or a
high-speed FPGA-based signal processing platform, the team covers the
complete hardware lifecycle — and integrates directly with the software
teams building your U-Boot, Linux kernel, and Yocto/Buildroot BSPs.

|

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Circuit Design
==============

Every project starts at the schematic. Amarula's circuit design
workflow includes:

- **Schematic capture** in Altium Designer — industry-standard PCB
  design tool for complex multi-layer boards.
- **Spice-based simulation** to validate circuit behavior before
  committing to fabrication, catching analog and power issues early.
- **Bill of Materials (BOM) generation** with manufacturer pricing,
  component availability checks, and end-of-life (EOL) risk assessment.
- **Rapid prototyping** on off-the-shelf platforms — Raspberry Pi,
  Raspberry Pi Pico, Arduino, STM32 Nucleus, and ESP32 — to prove
  concepts before custom PCB design begins.

**Key capabilities:**

- System-on-Module (SoM) and embedded processor-based designs
- Power supply design (switch-mode and linear regulation)
- Battery-operated and power-optimized circuits
- High-speed digital interfaces
- Small-footprint, space-constrained designs

|

PCB Design
===========

Custom PCB layout is delivered as a complete manufacturing package:

- **Multi-layer PCB routing** with Design Rule Checking (DRC)
  enforced from the start — no last-minute surprises.
- **Signal integrity** consideration for high-speed interfaces.
- **Thermal management** for power-dense designs.

**Deliverables you receive:**

- Schematics (PDF and native Altium format)
- Bill of Materials with manufacturer part numbers and pricing
- Simulation reports
- PCB layout documents and fabrication drawings
- Gerber and NC Drill files (ready for any PCB fab house)
- Assembly documents and drawings
- Mechanical 3D CAD models (optional)

|

CAD/CAE — Mechanical Design
================================

Hardware doesn't end at the PCB edge. Amarula provides:

- **3D modeling** of the PCB assembly for enclosure fit-checking.
- **Custom enclosure design** tailored to your product's mechanical
  constraints and environmental requirements, or **off-the-shelf
  enclosure selection** for faster time to market.
- **Photorealistic concept renderings** for client approval before
  tooling begins.
- **3D printing** of prototype mechanical parts for hands-on
  evaluation.

The mechanical team uses **SolidWorks** for parametric 3D CAD modeling.

|

FPGA and Custom Digital Design
===============================

When an off-the-shelf processor or MCU isn't enough — or when you need
custom digital signal processing — Amarula's FPGA team delivers:

- **VHDL and Verilog** development for multi-vendor FPGAs.
- **Custom DSP pipelines** where off-the-shelf DSP processors fall
  short in throughput, latency, or power.
- **Low-level device driver development** bridging the
  hardware-software interface — critical for FPGA-based accelerators
  integrated into embedded Linux systems.

|

PCB Assembly and Production
============================

For prototypes and small-to-medium production runs:

- **Small-scale production** — tens to hundreds of boards produced
  through partner assembly facilities.
- **Functional testing** of every board before it ships.
- **Quality control** with documented test results.

This bridges the gap between one-off lab prototypes and full contract
manufacturing, giving you confidence that your design is production-ready.

|

Testing and Pre-Compliance
============================

Amarula tests at every stage of development, not just at the end:

- **Functional testing** of individual features and board-level
  components.
- **Performance and reliability testing** under varied operating
  conditions (temperature, voltage, load).
- **Pre-compliance testing** at accredited laboratories covering:

  - **EMC** — electromagnetic compatibility (emissions and immunity)
  - **Electrical safety** — insulation, creepage, clearance
  - **Environmental** — temperature, humidity, vibration

Pre-compliance testing identifies issues before formal certification,
saving time and money in the final compliance phase.

|

The Hardware-Software Advantage
=================================

What sets Amarula apart is the tight integration between hardware
engineering and embedded Linux BSP development under one roof:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Stage
     - Hardware Team
     - Software Team
   * - Concept
     - Feasibility, component selection
     - Kernel/driver availability check
   * - Schematic
     - Circuit design, BOM
     - Pin muxing, device tree planning
   * - PCB Layout
     - DRC, signal integrity
     - Boot media, debug interfaces
   * - Prototype
     - Assembly, bring-up
     - U-Boot, kernel boot, BSP integration
   * - Testing
     - Functional, pre-compliance
     - Driver validation, CI integration
   * - Production
     - Assembly support
     - Yocto/Buildroot image generation

This parallel workflow means the BSP is often ready by the time the
first prototype boards arrive — no waiting for software to catch up
with hardware.

|

Related Wiki Pages
==================

- :doc:`BSP Index <bsp/index>` — mainline U-Boot and Linux kernel
  guides for our supported hardware platforms.
- :doc:`Build Systems Hub <build-systems-hub>` — Yocto and Buildroot
  integration for production firmware images.
- :doc:`CI/CD Hub <cicd-hub>` — Jenkins pipelines for automated
  hardware testing and firmware delivery.
- :doc:`Getting Started <getting-started-hub>` — host setup,
  cross-compilation, and board bring-up.

|

.. tip::
   Need hardware design, PCB layout, or FPGA development for your
   embedded Linux product? Amarula Solutions provides end-to-end
   hardware engineering from concept to production, fully integrated
   with our embedded Linux and open source software expertise.
   `Contact our hardware team <https://www.amarulasolutions.com/contact/>`_
