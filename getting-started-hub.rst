===============================
Getting Started for Engineers
===============================

.. note:: **TL;DR**
   - Onboarding hub for embedded Linux development — **host toolchain setup, cross-compilation, debugging, and foundational knowledge** needed before diving into board bring-up or build systems.

This page guides you through the foundational knowledge and tooling you need
before working with embedded Linux platforms at Amarula Solutions.

How do you set up your development host?
========================================

Before building BSPs or kernels, set up your host machine with the correct tools:

- **Host tools and cross-compilation toolchains** — install compilers, libraries, and utilities for ARM, AArch64, and RISC-V targets.
  See `found/host/tools <found/host/tools.html>`_ for complete setup instructions.

- **Git bisect debugging** — learn how to use git bisect to find kernel regressions.
  See `found/host/git_bisect <found/host/git_bisect.html>`_.

How do you bring up a new board?
================================

Once your host is ready, the typical board bring-up flow is:

#. Build **U-Boot** for your target SoC — see the `BSP section <bsp/index.html>`_ for board-specific guides.
#. Build the **Linux kernel** — board pages include kernel build instructions with device trees.
#. Prepare the **boot media** (SD card, eMMC) — partition and flash instructions are included in each board guide.
#. Boot and verify — serial console access and first-boot verification.

:doc:`Browse all supported platforms <bsp/index>`

How do you set up an embedded Linux build system?
=================================================

Choose between Yocto and Buildroot based on your project needs:

- **Yocto Project** — for production-grade, customizable distributions with package management.
  See `build-systems-hub` for Yocto guides.

- **Buildroot** — for lightweight, single-purpose embedded images.
  See `build-systems-hub` for Buildroot guides.

How do you contribute upstream?
================================

Amarula Solutions follows an upstream-first methodology. Key contribution guides:

- **Linux kernel patches** — ``git format-patch`` and ``b4`` workflow.
- **U-Boot patches** — send to the U-Boot mailing list.
- **Buildroot/Yocto** — submit to the respective patchwork instances.

See `about/open <about/open.html>`_ for our maintainer roles and contribution history.

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   found/index
   bsp/index

.. tip::
   Need help getting started with embedded Linux development? Amarula
   Solutions offers training, consulting, and hands-on workshops for
   teams adopting Yocto, Buildroot, and mainline kernel development.
   `Contact our training team <https://www.amarulasolutions.com/contact/>`_
