====================
Embedded Security
====================

.. note:: **TL;DR**
   - Hub aggregating all **embedded security documentation** — covering **secure boot** (UEFI, i.MX HABv4, SPL), **OP-TEE trusted execution**, **Mend SCA vulnerability scanning**, **verified boot**, and platform-specific security hardening for embedded Linux and Android.

Secure Boot Implementation
==========================

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Platform / Guide
     - What it covers
   * - **UEFI Secureboot with Yocto and GRUB**
     - x64 UEFI Secureboot, TPM/LUKS auto-decryption, SELinux, Mender A/B updates. See `article <articles/yocto/implementing-secureboot-with-yocto-wrynose-and-grub.html>`_.
   * - **i.MX6 HABv4 Signed Boot**
     - PKI tree generation, SRK fusing, signed U-Boot, signed uImage, encrypted boot with DEK blob. See the `i.MX6 HABv4 guide <opensource/thirdparty/uboot/secure_boot/imx6_habv4.html>`_.
   * - **i.MX8MM HABv4 Secure Boot**
     - Extension of i.MX6 HABv4 for i.MX8M Mini platforms. See the `i.MX8MM HABv4 guide <opensource/thirdparty/uboot/secure_boot/imx8mm_habv4.html>`_.
   * - **SPL HABv4**
     - Secure Boot for U-Boot SPL (Secondary Program Loader). See the `SPL HABv4 guide <opensource/thirdparty/uboot/secure_boot/spl_habv4.html>`_.
   * - **Verified Boot on i.MX6**
     - Authenticated kernel boot flow. See the `verified boot on i.MX6 guide <opensource/thirdparty/uboot/image_boot/verified_boot_on_imx6.html>`_.
   * - **Verified Boot on Allwinner A64**
     - Authenticated kernel boot on 64-bit Allwinner. See the `verified boot on Sunxi64 guide <opensource/thirdparty/uboot/image_boot/verified_boot_on_sunxi64.html>`_.
   * - **Redundant Boot with U-Boot**
     - Multi-partition failover for high-availability boot. See `guide <opensource/thirdparty/uboot/image_boot/redundant.html>`_.

Trusted Execution Environment
=============================

- **OP-TEE on i.MX6** — trusted application development, secure storage, hardware-backed isolation.
  See `opensource/thirdparty/optee/index <opensource/thirdparty/optee/index.html>`_.

Vulnerability Scanning
======================

- **meta-mend** — Mend SCA integration in Yocto for CRA compliance.
  See `opensource/products/meta-mend <opensource/products/meta-mend.html>`_.

- **MendReport Jenkins library** — automated vulnerability analysis in CI/CD.
  See `ci/sharedlibs/whitesource_jenkinslib <ci/sharedlibs/whitesource_jenkinslib.html>`_.

- **warning-ng Yocto vulnerability scanner** — CVE tracking in Jenkins pipelines.
  See `news/warning-ng-jenkins-scanner <news/warning-ng-jenkins-scanner.html>`_.

Application Security
====================

- **React Native vulnerability fixing** — `security/react_native/solving_vulnerabilities/solving_vulnerabilities <security/react_native/solving_vulnerabilities/solving_vulnerabilities.html>`_.

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   security/index
   opensource/thirdparty/uboot/secure_boot/index
   opensource/thirdparty/uboot/image_boot/verified_boot_on_imx6
   opensource/thirdparty/uboot/image_boot/verified_boot_on_sunxi64
   opensource/thirdparty/uboot/image_boot/redundant
   opensource/thirdparty/optee/index
   opensource/products/meta-mend
   articles/yocto/implementing-secureboot-with-yocto-wrynose-and-grub

.. tip::
   Need help securing your embedded product? Amarula Solutions offers
   secure boot implementation, TEE integration, vulnerability assessment,
   and CRA compliance consulting for embedded Linux and Android.
   `Contact our security team <https://www.amarulasolutions.com/contact/>`_
