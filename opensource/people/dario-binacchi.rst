.. ============================================================================
   Dario Binacchi — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from amarulasolutions.com/team/dario-binacchi and
   the monthly contribution reports in opensource/reports/.
   ============================================================================

==============
Dario Binacchi
==============

.. image:: /images/people/dario-binacchi.jpg
   :align: right
   :width: 220

**Role:** Senior Embedded Linux Developer

**At Amarula since:** 2017

**Location:** Italy

|

Dario is an embedded developer with a strong passion for open source
software. He completed a thesis on Digital Signal Processors and earned
his degree in Software Engineering in 2000. His career began in the
embedded domain, first working on bare-metal systems before
transitioning to Linux-based architectures.

He joined Amarula Solutions around 2017, brought in by CEO Michael
Trimarchi, and has since become one of the most active contributors to
Buildroot, U-Boot, and the Linux kernel — work he describes as a source
of "great inspiration and satisfaction."

|

----

Open Source Focus
=================

**Buildroot**
  Dario is the single most prolific contributor in Amarula's Buildroot
  activity. Since 2025 he has maintained and bumped Linux and U-Boot
  versions across a wide range of boards:
  STM32MP1/MP2, STM32F4/F7/H7 Discovery kits, BeagleBone, TI AM62x,
  i.MX6ULZ, and i.MX8MN BSH boards. He has also introduced new
  packages (``cmocka``, ``uuu``, ``armadillo``, ``libgphoto2``,
  ``embiggen-disk``, ``ufs-utils``, ``pocketpy``) and maintained
  the Qt6 and Python package ecosystems.

**Linux Kernel**
  Contributions span the STM32 platform (device trees, clock drivers,
  CAN controller fixes), the i.MX family, and DRM panel drivers
  including Ampire and Rocktech display panels. He actively works on
  ARM architecture improvements and CAN networking.

**U-Boot**
  Board maintenance for STM32MP1/MP2, i.MX, and TI platforms, plus
  upstream version bumps. He authored patches for the STM32F4 clock
  driver and contributed to the release cycle documentation.

**CAN Bus Networking**
  Dario maintains the Linux kernel's CAN subsystem components and has
  upstreamed fixes for STM32 CAN controllers used in industrial
  applications.

**Additional Projects**
  He contributes to the Zephyr RTOS (ESP32 support) and has worked on
  Yocto/OpenEmbedded BSP layers.

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

----

Beyond the Code
===============

When not writing kernel patches or bumping Buildroot packages, Dario
enjoys jogging, watching movies, reading, and fishing on the banks of
the Po River.

|

.. note::
   This profile is part of the :doc:`Amarula Solutions Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Dario is one of the many open source engineers at Amarula Solutions.
   Interested in collaborating? Amarula funds upstream development across
   Buildroot, U-Boot, and the Linux kernel.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
