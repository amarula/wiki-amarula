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

| **Role:** Senior Embedded Linux Developer
| **Location:** Suzzara, near Mantua, Italy

| **GitHub:** `passgat <https://github.com/passgat>`__
| **LinkedIn:** `dario-binacchi <https://www.linkedin.com/in/dario-binacchi-698a9734>`__
| **Personal site:** `passgat.github.io <https://passgat.github.io>`__

Dario is an embedded developer with a strong passion for open source
software. He graduated in Software Engineering in 2000, completing a
thesis on Digital Signal Processors. He started his career working on
bare-metal embedded systems before transitioning to Linux-based
architectures.

After joining Amarula Solutions through its CEO, Michael Trimarchi, he
began actively contributing to projects such as Buildroot, U-Boot, and
the Linux kernel — work he describes as a source of great inspiration
and satisfaction.

He approaches programming as "learning while having fun."

|

----

Open Source Focus
=================

**Buildroot** (500+ patches)
  Buildroot is Dario's preferred build system and his most prolific
  project. He maintains and updates packages and boards from ST, TI,
  and BSH, covering STM32MP1, STM32F4/F7/H7 Discovery kits, BeagleBone,
  TI AM62x, i.MX6ULZ, and i.MX8MN platforms.

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

Talks & Community
=================

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Year
     - Event
     - Topic
   * - 2024
     - FOSDEM, Brussels
     - `Linux CAN upstreaming on MMU-less systems <https://archive.fosdem.org/2024/schedule/event/fosdem-2024-2864-linux-can-upstreaming-on-mmu-less-systems/>`__
   * - 2024
     - Linux Day, Mantova
     - `FOSS upstreaming: guidelines for contributing to open source <https://lugman.org/Linux_day_2024>`__
   * - 2024
     - ELCE, Vienna
     - `Buildroot Developer Meeting <https://www.linkedin.com/posts/buildroot_this-weekend-there-was-a-buildroot-developer-activity-7241111186333732865-KEAg?utm_source=share&utm_medium=member_ios&rcm=ACoAAAdHhBQBlvNmMXKkxS1iNlLQ-Tql3GKU_fA>`__
   * - 2025
     - ELCE, Amsterdam
     - `Dual-board embedded system: Yocto & Zephyr integration <https://www.youtube.com/watch?v=4UfndcKtEno>`__

|

----

Notable Contributions
======================

.. list-table::
   :header-rows: 1
   :widths: 50 25 10

   * - Contribution
     - Project
     - Year
   * - `AM33xx spread spectrum clock support <https://lore.kernel.org/all/20210606202253.31649-1-dariobin@libero.it/>`__
     - Linux Kernel
     - 2021
   * - `Add Bosch C_CAN controller driver <https://lore.kernel.org/all/20211219093809.21765-1-dariobin@libero.it/>`__
     - Xenomai
     - 2021
   * - `slCAN: extended feature support (step 1) <https://lore.kernel.org/all/87b5a1e2-3587-ed41-b15b-0158493e0633@victronenergy.com/>`__, `(step 2) <https://lore.kernel.org/all/20220728072308.4nqpakfh4p7mqjmz@pengutronix.de/>`__
     - Linux Kernel
     - 2022
   * - `Add ST bxCAN controller driver <https://lore.kernel.org/all/20230328073328.3949796-1-dario.binacchi@amarulasolutions.com/>`__
     - Linux Kernel
     - 2023
   * - `CAN netlink support (ip link) <https://lists.busybox.net/pipermail/busybox/2024-February/090641.html>`__
     - BusyBox
     - 2024
   * - `Apply patches with fuzz factor 0 <https://lore.kernel.org/all/20240522070238.3282121-1-dario.binacchi@amarulasolutions.com/>`__
     - Buildroot
     - 2024
   * - `Support creating a bmap image <https://lore.kernel.org/all/20240421095353.208034-2-dario.binacchi@amarulasolutions.com/>`__
     - Buildroot
     - 2024
   * - `i.MX8M spread spectrum clock support <https://lore.kernel.org/all/20250118124044.157308-1-dario.binacchi@amarulasolutions.com/>`__
     - Linux Kernel
     - 2025
   * - `Metadata-driven A/B boot support for STM32MP <https://github.com/STMicroelectronics/meta-st-stm32mp/pull/110>`__
     - meta-st-stm32mp
     - 2026
   * - `Metadata-driven A/B boot support for STM32MP <https://review.trustedfirmware.org/c/TF-A/trusted-firmware-a/+/51367>`__
     - TF-A
     - 2026
   * - `Metadata-driven A/B boot support for STM32MP15 <https://lore.kernel.org/all/ae24c989-a1b0-442d-a3e9-49b73e06e76f@foss.st.com/>`__
     - U-Boot
     - 2026
   * - `Metadata-driven A/B boot support for STM32MP25 <https://lore.kernel.org/all/20260430080627.849636-1-dario.binacchi@amarulasolutions.com/>`__
     - U-Boot
     - 2026

|

Beyond the Code
===============

When not writing kernel patches or bumping Buildroot packages, Dario
enjoys jogging, watching movies, reading, and fishing (passgat too
:)) while sitting on the bank of the Po river.

|

.. note::
   This profile is part of the :doc:`Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Dario is one of the many open source engineers at Amarula Solutions.
   Interested in collaborating? Amarula funds upstream development across
   Buildroot, U-Boot, and the Linux kernel.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
