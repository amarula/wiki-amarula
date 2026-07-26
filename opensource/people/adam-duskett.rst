.. ============================================================================
   Adam Duskett — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from amarulasolutions.com/team/adam-duskett and
   the monthly contribution reports in opensource/reports/.
   ============================================================================

============
Adam Duskett
============

.. image:: /images/people/adam-duskett.jpg
   :align: right
   :width: 220

**Role:** Business Development Manager & Embedded Linux Systems Engineer

**Location:** Amsterdam, The Netherlands (from Los Angeles, California)

**At Amarula since:** 2024

|

Adam is an embedded Linux systems engineer with extensive experience
managing build systems such as **Buildroot** and **Yocto**. Originally
from Los Angeles, California, he moved to Amsterdam in July 2024 to
join Amarula Solutions, bringing deep domain expertise from the
electric vehicle charging industry.

His career spans product development across **VoIP phones, multimedia
streaming cameras, and electric vehicle service equipment**. Most of
his embedded experience comes from the EV charging sector, where he
served as the **lead systems engineer** for electric vehicle chargers
at **Shell Recharge** and **Rivian Automotive**.

|

----

Open Source Focus
=================

**OpenEmbedded / Yocto**
  Adam is one of Amarula's primary Yocto and OpenEmbedded contributors.
  He maintains and upgrades core infrastructure packages including
  **RPM**, **DNF**, **Tailscale**, and **libtoml11**, and added
  scarthgap compatibility to Amarula's meta-layers. His RPM selftest
  migration to SHA256 checksums improved build reproducibility, and
  his **RPM Sequioa** cryptography backend work modernized the package
  management stack.

**Buildroot**
  Contributor to Buildroot with a focus on Python packages (``pysocks``,
  ``depot-tools``), embedded terminal infrastructure (``kmscon``,
  ``libtsm``), and Flutter engine integration. He also maintains and
  contributes to the Mender OTA update framework in Buildroot.

**BSP & Meta-Layers**
  Maintains meta-axelera (Avahi/mDNS integration, kernel modules,
  Voyager image), meta-amarula BSP layers for i.MX and Rockchip
  platforms, and Rust/Yocto cross-compilation support.

**Flutter on Embedded**
  Core contributor to Flutter integration in Buildroot and Yocto,
  enabling Flutter-based embedded UIs on resource-constrained devices.

**Mender OTA**
  Maintains Mender OTA update framework integration in Buildroot,
  supporting A/B firmware update strategies for production embedded
  devices.

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project / Area
   * - RPM selftests: migration to SHA256 checksum verification
     - OpenEmbedded
   * - RPM Sequioa cryptography backend upgrade (1.10.0 → 1.10.1)
     - OpenEmbedded
   * - KMScon + libtsm terminal infrastructure in OpenEmbedded
     - OpenEmbedded
   * - libtoml11: comprehensive ptest, gitsm, and bugtracker support
     - OpenEmbedded
   * - Tailscale upgrade pipeline (1.94.2 → 1.98.0 across releases)
     - OpenEmbedded
   * - scarthgap compatibility for meta-amarula layers
     - Yocto
   * - meta-axelera: Avahi/mDNS service integration
     - BSP / Yocto
   * - Flutter engine and embedder maintenance in Buildroot
     - Buildroot
   * - Mender OTA integration and Buildroot package maintenance
     - Buildroot
   * - Python pysocks and depot-tools host package fixes
     - Buildroot

|

Beyond the Code
===============

Adam enjoys traveling, baking, and learning new languages and cultures —
interests that align well with his move from California to Amsterdam
and his work in a distributed, international team.

|

.. tip::
   Need Yocto/OE expertise for EV charging, Flutter embedded, or Mender
   OTA integration? Amarula Solutions provides BSP development, build
   system optimization, and long-term maintenance across i.MX, Rockchip,
   and STM32 platforms.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
