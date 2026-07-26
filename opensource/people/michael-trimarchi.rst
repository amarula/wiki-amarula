.. ============================================================================
   Michael Trimarchi — Profile page for Amarula Solutions' open source
   contributor directory. Data sourced from amarulasolutions.com/team/michael-trimarchi
   and the monthly contribution reports in opensource/reports/.
   ============================================================================

==================
Michael Trimarchi
==================

.. image:: /images/people/michael-trimarchi.jpg
   :align: right
   :width: 220

**Role:** Co-Founder & Chief Executive Officer

**Location:** Amsterdam, The Netherlands

**Education:** Master Degree in Software Engineering, Pisa University (2000)

|

Michael is the co-founder and CEO of Amarula Solutions, leading a team
of embedded Linux engineers while remaining hands-on as a Linux Software
Engineer. With over 20 years of experience spanning all fields of Linux
embedded systems, he has built Amarula into one of the most active
upstream-first consultancies in the open source embedded ecosystem.

His technical roots run deep: he co-authored the first version of the
**EDF (Earliest Deadline First) scheduling patches** — the Linux deadline
scheduling class — submitted to mainline Linux. Prior to founding
Amarula, he worked as a research consultant at the Sant'Anna School of
Advanced Studies (SSSA) in Pisa and as a consultant on nautical
navigation systems. He has published in the fields of **real-time
scheduling, hierarchical scheduling, and component-based systems**.

|

----

Open Source Focus
=================

**U-Boot**
  Michael serves as the **SPI subsystem custodian** and **MTD/SPI-NOR
  custodian** in the upstream U-Boot project, reviewing and merging
  patches from contributors worldwide. He actively works on Allwinner
  sunXi, Rockchip, i.MX, and RISC-V platform support, as well as
  Falcon Mode fast boot and secure boot (HABv4) implementations.

**Linux Kernel**
  Contributor to the Linux Kernel Memory Consistency Model (LKMM),
  display panel and bridge drivers (DSI), STM32 and i.MX device trees,
  and CAN controller fixes. His earlier kernel work established the
  deadline scheduling class used in real-time Linux deployments.

**Jenkins & CI/CD**
  The most prolific contributor to Amarula's Jenkins ecosystem: lead
  developer of the **ReviewAI Gerrit Code Review plugin**, the **Gitea
  Artifact Manager plugin**, and the **warning-ng scanner suite**
  (Yocto, Valgrind, CodeChecker). He maintains Gerrit Checks integration
  and the shared Jenkins pipeline libraries that power Amarula's CI
  infrastructure.

**Zephyr RTOS**
  Co-author of the **apds9253 ambient light sensor driver**, with
  contributions to ESP32 and STM32 board support.

**Other Projects**
  Maintains **meta-mend** (Yocto layer for Mend SCA vulnerability
  scanning), **ldap-passwd-webui**, and contributes to Buildroot
  package and board maintenance.

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project / Area
   * - Gitea Artifact Manager Jenkins plugin (new)
     - Jenkins
   * - ReviewAI Gerrit plugin version 4.0 with ``--mode`` flag
     - Jenkins
   * - Static analysis + code coverage pipeline for Gerrit Checks plugin
     - Jenkins
   * - mend.bbclass async API integration for Yocto CVE scanning
     - meta-mend / Yocto
   * - U-Boot SPI/MTD maintainer — reviewed hundreds of patches
     - U-Boot
   * - ldap-passwd-webui fork and development
     - Infrastructure
   * - apds9253 sensor driver for Zephyr RTOS
     - Zephyr
   * - Gerrit Checks plugin HTTP/HTTPS pipeline support
     - Jenkins
   * - Axelera AI BSP kernel module and Yocto layer maintenance
     - Yocto / BSP
   * - EDF deadline scheduling class (original author, ongoing relevance)
     - Linux Kernel

|

Beyond the Code
===============

Michael enjoys cooking in his free time and credits his family's support
as the foundation of Amarula Solutions' success: *"Without them, my
family, I wouldn't be here with this great company Amarula Solutions."*

He values talking to his parents regularly and finds balance between
running a growing company and staying hands-on with kernel patches and
Jenkins pipelines.

|

.. note::
   This profile is part of the :doc:`Amarula Solutions Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Michael leads Amarula Solutions' open source strategy. Interested in
   collaborating on U-Boot, embedded Linux, or CI/CD infrastructure?
   `Contact our team <https://www.amarulasolutions.com/contact/>`_
