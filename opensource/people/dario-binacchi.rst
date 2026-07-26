.. ============================================================================
   Dario Binacchi — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from passgat.github.io and monthly contribution
   reports in opensource/reports/.
   ============================================================================

==============
Dario Binacchi
==============

.. image:: /images/people/dario-binacchi.jpg
   :align: right
   :width: 220

**Role:** Senior Embedded Linux Developer

**Location:** Suzzara, near Mantua, Italy

**GitHub:** `passgat <https://github.com/passgat>`__
**LinkedIn:** `dario-binacchi <https://www.linkedin.com/in/dario-binacchi-698a9734>`__
**Personal site:** `passgat.github.io <https://passgat.github.io>`__

|

Dario is an embedded developer with a strong passion for open source
software. He graduated in Software Engineering in 2000, completing a
thesis on Digital Signal Processors. He started his career working on
bare-metal embedded systems before transitioning to Linux-based
architectures.

He joined Amarula Solutions, brought in by CEO Michael Trimarchi, and
has since become one of the most active contributors to Buildroot,
U-Boot, and the Linux kernel — work he describes as "a source of great
inspiration and satisfaction."

He approaches programming as "learning while having fun."

|

----

Open Source Focus
=================

**Buildroot** (500+ patches)
  Buildroot is Dario's preferred build system and his most prolific
  project. He maintains and updates packages and boards from ST, TI,
  and BSH, covering STM32MP1/MP2, STM32F4/F7/H7 Discovery kits,
  BeagleBone, TI AM62x, i.MX6ULZ, and i.MX8MN platforms. He has
  introduced new packages and maintained the Qt6 and Python ecosystems.

**Linux Kernel** (200+ patches)
  Contributions target ARM and ARM64 platforms, spanning board
  bring-up, clock drivers, the CAN subsystem, DRM, and touchscreen
  drivers. Dario is the **maintainer of the slCAN and bxCAN drivers**
  within the Linux kernel CAN subsystem.

**U-Boot** (200+ patches)
  Started with video support for the BeagleBoard, later expanding
  into clocks, pinctrl, NAND, RTC, PWM, GPIO, and more. He serves as
  **co-custodian of the NAND subsystem** alongside Michael Trimarchi.

**CAN Bus Networking**
  Dario maintains the Linux kernel's slCAN and bxCAN drivers and has
  upstreamed CAN controller fixes for STM32 and other platforms used
  in industrial applications.

**Additional Projects**
  Contributions to Zephyr RTOS, Yocto/OpenEmbedded, and Xenomai.

|

----

Talks
=====

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Year
     - Event
     - Topic
   * - 2024
     - FOSDEM, Brussels
     - Linux CAN upstreaming on MMU-less systems
   * - 2024
     - Linux Day, Mantova
     - FOSS upstreaming: guidelines for contributing to open source
   * - 2024
     - ELCE, Vienna
     - Buildroot Developer Meeting
   * - 2025
     - ELCE, Amsterdam
     - Dual-board embedded system: Yocto & Zephyr integration
       (co-presented with Andrea Ricchi)

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project
   * - STM32MP2 board support in mainline Buildroot
     - Buildroot
   * - Ampire AM-800600P5TMQW-T01H DRM panel driver
     - Linux Kernel
   * - Rocktech JH057N00900 MIPI-DSI panel support
     - Linux Kernel
   * - STM32F4 clock driver fix for uninitialized variable
     - U-Boot / Linux
   * - FWU metadata support for STM32MP A/B firmware updates
     - Buildroot
   * - STM32MP157 DK2 IRQ edge configuration fix
     - Linux Kernel
   * - CAN controller fixes for STM32 platforms
     - Linux Kernel
   * - New board defconfigs: stm32h747_disco_sd, stm32f769_disco_sd
     - Buildroot
   * - UFS utils and mmc-utils package bumps and new package introductions
     - Buildroot
   * - TI AM62x and BeagleBone board maintenance
     - Buildroot

|

Beyond the Code
===============

When not writing kernel patches or bumping Buildroot packages, Dario
enjoys jogging, watching movies, reading, and fishing ("passgat too
:)" as he puts it) while sitting along the Po river.

|

.. note::
   This profile is part of the :doc:`Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Dario is one of the many open source engineers at Amarula Solutions.
   Interested in collaborating? Amarula funds upstream development across
   Buildroot, U-Boot, and the Linux kernel.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
