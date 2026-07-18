=================================
Embedded Linux Build Systems
=================================

.. note:: **TL;DR**
   - Hub aggregating all **Yocto Project and Buildroot** documentation — covering build system setup, custom layer/distro creation, security integration (secure boot, Mend SCA), and CI/CD pipeline integration for production embedded Linux images.

Yocto Project
=============

The Yocto Project is our primary build system for production-grade embedded Linux distributions.

**Step-by-step guides:**

- **Implementing Secureboot with Yocto Wrynose and GRUB** — UEFI Secureboot, TPM/LUKS, SELinux, A/B updates with Mender.
  See `articles/yocto/implementing-secureboot-with-yocto-wrynose-and-grub <articles/yocto/implementing-secureboot-with-yocto-wrynose-and-grub.html>`_.

**Yocto in CI/CD:**

- **Optimizing Yocto Builds with Jenkins and Resource Throttling** — kas-container, SSTATE caching, multi-configuration.
  See `articles/jenkins/jenkins-yocto-kas-pipeline <articles/jenkins/jenkins-yocto-kas-pipeline.html>`_.

- **Building Secure Yocto Images with Mend SCA Integration** — vulnerability scanning during build.
  See `articles/jenkins/jenkins-mend-pipeline <articles/jenkins/jenkins-mend-pipeline.html>`_.

**Security integration:**

- **meta-mend** — Mend SCA vulnerability analysis integrated into BitBake.
  See `opensource/products/meta-mend <opensource/products/meta-mend.html>`_.

Buildroot
=========

Buildroot is used for lightweight, single-purpose embedded Linux images.

**Guides:**

- **Flutter on Buildroot** — running Flutter apps on Buildroot-built systems.
  See `opensource/thirdparty/buildroot/flutter-buildroot <opensource/thirdparty/buildroot/flutter-buildroot.html>`_.

- **CuteKeyboard in Buildroot** — Qt virtual keyboard integration.
  See `opensource/products/cutekeyboard <opensource/products/cutekeyboard.html>`_.

- **Buildroot Shared State Cache (sstate-cache)** — Yocto-style shared state caching for faster incremental builds.
  See `articles/buildroot/buildroot-sstate-cache <articles/buildroot/buildroot-sstate-cache.html>`_.

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   articles/yocto/index
   opensource/thirdparty/buildroot/index
   articles/buildroot/index
   articles/buildroot/buildroot-sstate-cache
   opensource/products/meta-mend
   articles/jenkins/jenkins-yocto-kas-pipeline
   articles/jenkins/jenkins-mend-pipeline

.. tip::
   Need a custom embedded Linux distribution for your product? Amarula
   Solutions provides Yocto layer development, Buildroot integration,
   and long-term BSP maintenance for ARM, RISC-V, and x86 platforms.
   `Contact our build systems team <https://www.amarulasolutions.com/contact/>`_
