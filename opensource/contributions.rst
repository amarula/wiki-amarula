==============================
Open Source Contributions
==============================

.. note:: **TL;DR**
   - Amarula Solutions is an **active maintainer and upstream contributor** to **Linux Kernel, U-Boot, Buildroot, Yocto, Zephyr, and Jenkins plugins** — with maintainer roles in Allwinner sunXi, SPI, MTD/SPI-NOR, and DSI subsystems.
   - This page aggregates our **maintainer activity, monthly contribution reports, and upstream statistics** — updated continuously as patches are merged.

Maintainer Roles
================

Amarula Solutions engineers serve as official maintainers in the following subsystems:

**Linux Kernel:**
- DSI Vendor driver — `drivers/gpu/drm/panel/`
- DSI bridge drivers
- Linux Kernel Memory Consistency Model (LKMM)

**U-Boot:**
- `Allwinner sunXi custodian <https://gitlab.denx.de/u-boot/custodians/u-boot-sunxi>`_
- `SPI subsystem custodian <https://gitlab.denx.de/u-boot/custodians/u-boot-spi>`_
- `MTD/SPI-NOR custodian <https://gitlab.denx.de/u-boot/custodians/u-boot-spi>`_

**Buildroot:**
- Board configurations for i.MX, Allwinner, Rockchip
- Package maintainership: python-*, Mender, Flutter
- See `DEVELOPERS file <https://git.buildroot.net/buildroot/tree/DEVELOPERS#n1019>`_

**Yocto:**
- `meta-amarula-engicam <https://layers.openembedded.org/layerindex/branch/master/layer/meta-amarula-engicam>`_ (Engicam i.CoreM6 BSP)
- `Vyasa RK3288 machine config <http://git.yoctoproject.org/cgit/cgit.cgi/meta-rockchip/tree/conf/machine/vyasa-rk3288.conf>`_

For a full list with links, see :doc:`../about/open`.

Monthly Contribution Reports
============================

We publish monthly reports tracking all upstream commits across our repositories:

.. toctree::
   :maxdepth: 1
   :caption: 2026 Reports

   reports/report-03-2026
   reports/report-02-2026
   reports/report-01-2026

.. toctree::
   :maxdepth: 1
   :caption: 2025 Reports

   reports/report-12-2025
   reports/report-11-2025
   reports/report-10-2025
   reports/report-09-2025
   reports/report-08-2025
   reports/tail

Projects We Contribute To
=========================

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Project
     - Our Focus
   * - **Linux Kernel**
     - Display panels/bridges, CAN bus, STM32, i.MX, memory model, device trees
   * - **U-Boot**
     - Allwinner, Rockchip, i.MX, RISC-V, SPI/MTD, Falcon Mode, secure boot
   * - **Buildroot**
     - Board configs, Flutter, Mender, package updates, STM32, i.MX, Allwinner
   * - **Yocto / OpenEmbedded**
     - BSP layers, CVE scanning, meta-mend, meta-qt (CuteKeyboard)
   * - **Zephyr**
     - Sensor drivers (apds9253, si7006), STM32 boards, CAN, ESP32
   * - **Jenkins**
     - Gerrit Checks plugin, warning-ng (Yocto/Valgrind/CodeChecker scanners), pipeline-graph-view, bitbucket-plugin

Conference Talks
================

We regularly present our open source work at conferences — see :doc:`../about/conf` for a full list including FOSDEM, Embedded Linux Conference, Linux Plumbers, Buildroot Developer Days, and PyCon Italy.

.. tip::
   Want to collaborate on open source? Amarula Solutions funds upstream
   development and welcomes co-engineering on Linux Kernel, U-Boot,
   Buildroot, Yocto, and Zephyr.
   `Contact our open source team <https://www.amarulasolutions.com/contact/>`_
