.. ============================================================================
   Andrea Ricchi — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from amarulasolutions.com/team/andrea-ricchi and
   the monthly contribution reports in opensource/reports/.
   ============================================================================

=============
Andrea Ricchi
=============

.. image:: /images/people/andrea-ricchi.png
   :align: right
   :width: 220

**Role:** Senior Embedded Software Developer & Team Lead

**Location:** Carpi, Italy

**At Amarula since:** 2020

**Portfolio:** `andrearicchi.github.io <https://andrearicchi.github.io/>`__

|

Andrea is a passionate embedded software developer with deep expertise
in **C/C++**, **Rust**, and **Dart**, and a strong focus on safety and
performance. For application-layer work he builds user interfaces with
**Qt** and **Flutter**, while managing the underlying systems through
custom Linux distributions built with **Yocto** and **Buildroot**.

A committed open source advocate, Andrea actively contributes to
**ConnMan**, **Buildroot**, and **Yocto**. He is also the upstream
maintainer of **CuteKeyboard** (a Qt virtual keyboard, now part of
Yocto's meta-qt layer) and **FluteKeyboard** (a Flutter virtual
keyboard for embedded displays). He has presented at **FOSDEM 2024**
and **ELCE 2025**.

|

----

Open Source Focus
=================

**CuteKeyboard**
  Upstream maintainer of CuteKeyboard, an open-source Qt virtual
  keyboard adopted into Yocto's meta-qt layer. Andrea drives feature
  development, manages Buildroot package integration, adds multi-layout
  support (including Danish and Finnish keyboard layouts), and
  coordinates GitHub CI workflows.

**FluteKeyboard**
  Creator and maintainer of FluteKeyboard, a Flutter-based virtual
  keyboard designed for embedded touchscreen devices. He added
  persistent shift/uppercase mode, visibility toggles, null-safety
  checks, and local development tooling.

**ConnMan**
  Contributor to ConnMan, the lightweight network manager used in
  embedded Linux distributions, with improvements to timezone handling
  and file comparison logic.

**Buildroot**
  Maintainer of the ``cutekeyboard``, ``flutekeyboard``, and
  ``libcppconnman`` packages, registered as their developer in the
  upstream ``DEVELOPERS`` file. ``libcppconnman`` is a C++ library that
  exposes an easy-to-use API for communicating with ConnMan over D-Bus
  via GDBus. He has also contributed fixes to the ``timezone`` package.

**Yocto**
  Builds and maintains Yocto BSP layers, integrating custom embedded
  Linux distributions with Qt and Flutter UI stacks.

**Conference Speaking**
  - **FOSDEM 2024** — presented on embedded UI and open source tools
  - **ELCE 2025** — Embedded Linux Conference Europe speaker

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project / Area
   * - CuteKeyboard: Danish and Finnish layout support
     - CuteKeyboard
   * - FluteKeyboard: persistent shift/uppercase mode + null safety
     - FluteKeyboard
   * - CuteKeyboard Buildroot package bumps and maintenance
     - Buildroot
   * - libcppconnman package (C++ ConnMan D-Bus API)
     - Buildroot
   * - Registered as Buildroot DEVELOPERS entry for cutekeyboard
     - Buildroot
   * - FluteKeyboard: hide-system-bars option and local dev paths
     - FluteKeyboard
   * - CuteKeyboard: .github/CODEOWNERS and CI workflow integration
     - CuteKeyboard
   * - ConnMan timezone file comparison and symlink handling
     - ConnMan
   * - FOSDEM 2024: Embedded UI tools in open source
     - Conference
   * - ELCE 2025: Embedded Linux and UI development
     - Conference

|

Beyond the Code
===============

Based in Carpi, Italy, Andrea combines his technical work with a team
lead role, mentoring junior engineers and coordinating embedded
software projects across Amarula's Italian office. He enjoys balancing
low-level C/C++ and Rust system work with modern UI development,
bridging kernel-space robustness and user-facing polish.

|

.. note::
   This profile is part of the :doc:`Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Need an embedded UI for your Qt or Flutter-based product? Amarula
   Solutions provides custom virtual keyboard development, Buildroot
   package integration, and Yocto layer support.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
