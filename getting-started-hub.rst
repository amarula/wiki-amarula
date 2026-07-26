=============================================
Getting Started for Embedded Linux Engineers
=============================================

This hub is the entry point for engineers working on embedded Linux platforms at
Amarula Solutions. Whether you are bringing up a new board, setting up a build
system, or contributing to the upstream kernel, the content here will guide you
through the full development lifecycle — from your first cross-compilation
toolchain to production-grade CI/CD pipelines.

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Who Is This For?
================

:New to embedded Linux:
   You'll find step-by-step host setup, toolchain installation, and board
   bring-up guides that take you from zero to a booting system.

:Experienced BSP developer:
   Deep-dive references for U-Boot, kernel configuration, OP-TEE secure boot,
   and upstream contribution workflows.

:DevOps / CI engineer:
   Jenkins pipeline libraries, Gerrit integration, build throttling, and
   containerized build infrastructure.

:Engineering manager:
   Overviews of our build-system strategy (Yocto vs Buildroot), security
   integration, and open-source compliance practices.

:Curious who wrote this?:
   Every guide on this wiki is written by Amarula Solutions engineers
   actively contributing upstream. Browse our :doc:`open source team
   directory <opensource/people/index>` to see the people behind the
   patches.

----

The Embedded Linux Learning Path
================================

Embedded Linux development follows a natural progression. The sections below
are ordered to match the workflow you'll encounter in a real project.

.. _path-architecture:

1. Understand the System Architecture
--------------------------------------

Before writing code, understand what you're building:

- **Embedded Linux stack overview** — boot ROM → SPL → U-Boot → Linux kernel →
  root filesystem → user-space applications.
- **Cross-compilation model** — why you can't compile on the target, and how
  the host/target split works in practice.
- **Upstream-first philosophy** — why Amarula mainlines everything, and how
  that benefits both your project and the community.

See the :doc:`About page <about/about>` for context on how we work and the
:doc:`open source contributions <opensource/contributions>` that back our expertise.

.. _path-host:

2. Set Up Your Development Host
---------------------------------

Your host machine is your primary development tool. Get it right first.

- **Essential host packages** — compilers, build tools, libraries, and
  debugging utilities for Ubuntu and Debian-based systems.
- **Cross-compilation toolchains** — Linaro GCC for ARM, AArch64, and RISC-V
  targets, including installation and `PATH` setup.
- **Board communication tools** — serial console (minicom), TFTP server,
  USB boot tools (rkdeveloptool, sunxi-fel), and fastboot/adb for Android.
- **Git bisect for kernel debugging** — systematically find regressions in the
  Linux kernel with bisection.

:doc:`Complete host setup guide → <found/host/tools>`

:doc:`Git bisect debugging → <found/host/git_bisect>`

.. _path-bootloader:

3. Master the Bootloader: U-Boot
----------------------------------

U-Boot is the gatekeeper before the kernel starts. Understanding it deeply is
essential for board bring-up and production boot configuration.

- **Building U-Boot from mainline** — per-platform build instructions for
  Allwinner, Rockchip, NXP i.MX, and RISC-V.
- **Boot methods** — SD card, eMMC, USB (FEL mode for Allwinner, rkdeveloptool
  for Rockchip), and network (TFTP/NFS).
- **Falcon mode** — skip U-Boot's full initialization for sub-second boot times.
- **Verified boot** — chain-of-trust from SPL through U-Boot to kernel using
  HABv4 (NXP i.MX) and other secure boot mechanisms.
- **Redundant boot** — watchdog-triggered fallback images for production
  reliability.
- **U-Boot sandbox** — test and debug U-Boot on your host without hardware.

See :doc:`U-Boot section → <opensource/thirdparty/uboot/index>` for all bootloader topics.

.. _path-kernel:

4. Build and Configure the Linux Kernel
-----------------------------------------

The Linux kernel is where most customisation happens. You'll need to configure,
build, and debug it for your target SoC.

- **Kernel source and branches** — working with linux-next, stable trees, and
  vendor trees.
- **Device Tree configuration** — enabling and configuring peripherals (I2C,
  SPI, display, camera, networking) through device trees.
- **Driver development and debugging** — DRM display pipelines, MIPI DSI
  bridges, camera sensors (CSI), and USB Type-C/DisplayPort alt-mode.
- **Performance and boot-time optimization** — profiling, tracing, and
  reducing kernel boot time.

Each :doc:`BSP page <bsp/index>` includes kernel build instructions specific to
that platform. For kernel-space development articles, browse the
:doc:`news section <news/index>` and :doc:`articles <articles/index>`.

.. _path-rootfs:

5. Create the Root Filesystem
-------------------------------

The root filesystem is everything userspace: init, shells, libraries, and
applications.

- **From-scratch rootfs** — directory structure, BusyBox, device nodes, init
  scripts.
- **Filesystem choices** — ext4, squashfs, UBIFS — when to use each.
- **Partition layout** — single-partition, dual-partition (A/B updates), and
  Falcon-mode layouts.
- **Storage media** — SD card, eMMC, and raw NAND flash provisioning.

:doc:`SD card and partition setup → <found/host/tools>` (see SD Setup section)

.. _path-buildsystems:

6. Choose an Embedded Linux Build System
------------------------------------------

Manual builds give understanding; build systems give reproducibility and scale.

**Yocto Project** — for production-grade, customizable distributions:
  - :doc:`Implementing Secure Boot with Yocto, Wrynose, and GRUB <articles/yocto/implementing-secureboot-with-yocto-wrynose-and-grub>` — UEFI Secure Boot, TPM/LUKS, SELinux, A/B updates
  - :doc:`Yocto + Jenkins CI/CD with kas-container <articles/jenkins/jenkins-yocto-kas-pipeline>` — shared-state caching, multi-configuration builds
  - :doc:`Mend SCA integration in Yocto <articles/jenkins/jenkins-mend-pipeline>` — vulnerability scanning at build time

**Buildroot** — for lightweight, single-purpose images:
  - :doc:`Buildroot sstate-cache <articles/buildroot/buildroot-sstate-cache>` — Yocto-style shared state for incremental Buildroot builds
  - :doc:`Flutter on Buildroot <opensource/thirdparty/buildroot/flutter-buildroot>` — running Flutter embedded apps
  - :doc:`CuteKeyboard in Buildroot <opensource/products/cutekeyboard>` — Qt virtual keyboard integration

:doc:`Build systems hub → <build-systems-hub>` for the complete index.

.. _path-security:

7. Integrate Security
-----------------------

Security is not a bolt-on — it must be designed in from the start.

- **Secure boot chain** — HABv4 on i.MX6/i.MX8M, OP-TEE trusted applications.
- **Filesystem encryption** — TPM-backed LUKS, dm-verity for integrity.
- **A/B firmware updates** — :doc:`STM32MP A/B update with U-Boot and Mender <articles/yocto/stm32mp-ab-firmware-update>`.
- **Vulnerability scanning** — Mend SCA (now Mend) in CI, SonarQube for
  code quality.

:doc:`Security hub → <security-hub>` | :doc:`OP-TEE guides → <opensource/thirdparty/optee/index>`

.. _path-ci:

8. Automate with CI/CD
-----------------------

Amarula runs a Jenkins-based CI infrastructure integrated with Gerrit for code
review. All BSP work flows through this pipeline.

- **Gerrit integration** — :doc:`Gerrit trigger <ci/gerrit_trigger>`, :doc:`repo trigger <ci/gerrit_repo_trigger>`, and :doc:`HTTPS pipeline <articles/jenkins/jenkins-gerrit-https-pipeline>`.
- **Shared libraries** — reusable Jenkins pipeline functions for Android
  builds, SFTP deployments, repository management, and code checking.
- **Build optimization** — :doc:`throttling <ci/build_throttling>`,
  :doc:`shared-state caching <articles/buildroot/buildroot-sstate-cache>`, and
  :doc:`Docker containers <ci/docker>`.
- **Code quality** — :doc:`SonarQube <ci/sonarqube>`,
  :doc:`Warnings Next Generation <articles/jenkins/warning-ng-jenkins-codechecker>`,
  and :doc:`Valgrind integration <articles/jenkins/warning-ng-jenkins-valgrind>`.
- **Testing** — :doc:`Labgrid-based board testing <articles/jenkins/how-validate-os-build-labgrid-testing>`.

:doc:`CI/CD hub → <cicd-hub>` | :doc:`Shared libraries → <ci/sharedlibs/index>`

.. _path-upstream:

9. Contribute Upstream
------------------------

Every project at Amarula follows an upstream-first approach. Contributions go
to the mainline projects, not internal forks.

- **Linux kernel** — `git format-patch`, `checkpatch.pl`, and `b4` tool for
  mailing-list-based submission.
- **U-Boot** — patches to the U-Boot mailing list (`u-boot@lists.denx.de`).
- **Buildroot** — patches to the Buildroot mailing list and Patchwork.
- **Yocto / OpenEmbedded** — layers submitted to the Yocto Project mailing list.

Amarula engineers serve as **maintainers** and **regular contributors** to all
of these projects. See :doc:`opensource/contributions` for our track record,
and :doc:`about/open` for our maintainer roles.

:doc:`Monthly contribution reports → <opensource/contributions>` for the latest activity.

----

Quick-Start Per Domain
========================

Pick the path that matches what you're working on right now.

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Domain
     - What You'll Learn
     - Start Here
   * - **Board Bring-Up**
     - U-Boot build, kernel config, device tree, boot media setup
     - :doc:`bsp/index`
   * - **Yocto Development**
     - Layer creation, image recipes, secure boot, CI integration
     - :doc:`build-systems-hub`
   * - **Buildroot**
     - Minimal images, Flutter apps, sstate caching
     - :doc:`build-systems-hub`
   * - **Kernel / Drivers**
     - DRM, MIPI DSI, CSI camera, device trees
     - :doc:`news/index`
   * - **Android AOSP**
     - Board bring-up, CI pipelines, app signing, emulator testing
     - :doc:`ci/android/android`
   * - **CI/CD Pipelines**
     - Jenkins job DSL, Gerrit triggers, shared libraries
     - :doc:`cicd-hub`
   * - **Security**
     - Secure boot, OP-TEE, HABv4, dm-verity, vulnerability scanning
     - :doc:`security-hub`
   * - **IoT & RTOS**
     - Zephyr on ESP32 and TI CC3220, ESP32 camera projects
     - :doc:`iot-and-rtos-hub`
   * - **AI / ML Tools**
     - ReviewAI Gerrit plugin, Jelliphy framework
     - :doc:`products-and-tools`

----

Supported Hardware Platforms
==============================

Amarula maintains mainline Linux and U-Boot support across multiple SoC
families:

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Vendor
     - SoC Families
     - Featured Boards
     - Guide
   * - **Allwinner**
     - A13, A20, A33, A64, H3, H5, H6
     - Olimex, Orange Pi, Pine64, Banana Pi
     - :doc:`bsp/sunxi/index`
   * - **Rockchip**
     - RK3288, RK3399, RK3399Pro, PX30
     - Vyasa, Rock Pi 4/N10, NanoPi M4, Tinker Board
     - :doc:`bsp/rockchip/index`
   * - **NXP i.MX**
     - i.MX6Q/DL, i.MX8M
     - Engicam i.CoreM6, i.CoreMX8M Mini
     - :doc:`bsp/imx/index`
   * - **RISC-V**
     - SiFive FU540
     - HiFive Unleashed, QEMU
     - :doc:`bsp/riscv/index`
   * - **Amarula Custom**
     - Vyasa (RK3288), Giotto
     - Custom engineering platforms
     - :doc:`bsp/amarula-boards/index`

----

Tools & Products
==================

We maintain several open-source tools developed in-house:

- :doc:`ReviewAI Gerrit Plugin <opensource/products/reviewai-gerrit-plugin>` — AI-powered code review directly in Gerrit.
- :doc:`CuteKeyboard <opensource/products/cutekeyboard>` — Qt virtual keyboard, now upstream in Yocto's meta-qt.
- :doc:`Flutekeyboard <opensource/products/flutekeyboard>` — Flutter virtual keyboard for embedded displays.
- :doc:`meta-mend <opensource/products/meta-mend>` — Yocto layer for Mend SCA vulnerability analysis.
- :doc:`DynDesign <opensource/products/dyndesign/index>` — Python dynamic class decoration and builder patterns.
- :doc:`libcppconnman <opensource/products/libcppconnman>` — C++ wrapper for ConnMan network management.
- :doc:`git-collect-plugin <opensource/products/git-collect-plugin>` — Jenkins plugin for Git statistics.

:doc:`Full products overview → <products-and-tools>`

----

Training and Consulting
=========================

Amarula Solutions offers professional training, hands-on workshops, and
engineering consulting across all embedded Linux domains:

- :doc:`Past workshops <news/workshop>` — Linux, Yocto, and mainline kernel
  workshops delivered at client sites and conferences like
  :doc:`Embedded World <news/embeddedworld-2026>`.
- **Custom on-site training** — tailored curriculum for your team's stack and
  hardware.
- **Consulting services** — board bring-up, BSP maintenance, mainline
  upstreaming, Yocto layer development, and CI infrastructure.

`Contact us <https://www.amarulasolutions.com/contact/>`_ to discuss your
project needs.

----

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   found/index
   bsp/index
   opensource/thirdparty/uboot/index
   build-systems-hub
   cicd-hub
   security-hub
   iot-and-rtos-hub
   opensource/people/index
   about/about
   opensource/contributions
   products-and-tools
   news/index
   articles/index
