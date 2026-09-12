=========================================================================
Upstreaming Legacy Systems: A Practical Guide to PX30 & Yocto Integration
=========================================================================

.. note:: **TL;DR**

   - Practical guide to booting a **mainline Linux kernel with a Yocto-built
     root filesystem on a legacy PX30 device** without overwriting the stock
     bootloader — only the rootfs partition is flashed, so the device stays
     revertible to its original firmware.
   - Covers the **non-destructive upstreaming workflow**: decompiling the
     vendor ``.dtb`` to map the hardware, converting Yocto ``ext4`` images
     into **Android sparse images** for Fastboot, and packaging the kernel
     and DTB into an **uncompressed FIT image** to avoid legacy U-Boot
     relocation crashes.
   - Includes a reusable **U-Boot boot macro** (``yoctobootcmd``) that
     relocates the staged payload out of the Fastboot RAM buffer and boots
     it with ``bootm``.

|

Transitioning a legacy embedded system to an upstream Linux kernel and a
modern Yocto Project environment is a balancing act: the vendor bootloader
stays in place, while the kernel, the devicetree, and the root filesystem
are replaced underneath it. This guide combines the strategic principles of
non-destructive upstreaming with the concrete procedures required to flash
a custom root filesystem and boot a mainline kernel on a PX30 device through
U-Boot and Fastboot, while retaining the ability to restore the stock
firmware.

What is the strategy for upstreaming a legacy embedded system?
--------------------------------------------------------------

When bridging the gap between legacy vendor code and mainline Linux,
preserving a known-good working state is critical.

* **Retain stock fallbacks:** Never overwrite the stock bootloader or
  partition tables until the new system is fully validated. Only flash the
  rootfs partition to keep the device revertible to its original firmware.
* **Bridge the devicetree gap:** Decompile the original ``.dtb`` from the
  running legacy system to accurately map the hardware, and iteratively
  enable peripherals — starting with the UART console.
* **Isolate Yocto layers:** Build the project using reproducible
  environments, keeping custom BSP layers separate from core Yocto layers.
  For example:

  .. code-block:: bash

     kas-container build kas-px30.yml

  Build commands should be generalized for your specific hardware target.

How do you flash a Yocto rootfs over Fastboot on legacy U-Boot?
---------------------------------------------------------------

Legacy U-Boot environments impose constraints that must be navigated
carefully during deployment. Yocto outputs raw ``ext4`` images that must be
converted to **Android sparse images** before flashing: this strips
unallocated storage blocks so the transfer fits within the Fastboot size
limit.

How do you convert a Yocto ext4 image to a sparse image?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On your host workstation, convert the raw ``.ext4`` image using
``img2simg``:

.. code-block:: bash

   img2simg build/tmp/deploy/images/px30/core-image-px30.rootfs.ext4 rootfs_sparse.img

How do you flash the rootfs partition over Fastboot?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Access the U-Boot serial console on the device and start the Fastboot
   service:

   .. code-block:: bash

      fastboot usb 0

2. On your host workstation, flash the sparse rootfs image to the target
   partition:

   .. code-block:: bash

      fastboot flash rootfs rootfs_sparse.img

How do you package a mainline kernel as a FIT image?
----------------------------------------------------

You do not need an upstream bootloader to boot an upstream kernel, provided
the kernel is packaged correctly for the legacy environment. The kernel
image and the devicetree blob (``.dtb``) must be bundled together into a
Flattened Image Tree (FIT) image.

**Bypass compression limits:** Older bootloaders frequently crash during
kernel decompression. For this specific U-Boot build, FIT images with
gzip-compressed kernels trigger relocation crashes. An uncompressed raw
kernel (``Image``) with ``compression = "none"`` must be used.

How do you write the FIT image source (px30.its)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure your ``px30.its`` file points to your uncompressed Yocto kernel build
artifacts:

.. code-block:: dts

   /dts-v1/;

   / {
       description = "PX30 Buildroot/Yocto FIT Image";
       #address-cells = <1>;

       images {
           kernel-1 {
               description = "Linux Kernel Raw";
               data = /incbin/("build/tmp/deploy/images/px30/Image");
               type = "kernel";
               arch = "arm64";
               os = "linux";
               compression = "none";
               load = <0x09000000>;
               entry = <0x09000000>;
               hash-1 {
                   algo = "sha1";
               };
           };

           fdt-1 {
               description = "PX30 DTB";
               data = /incbin/("build/tmp/deploy/images/px30/px30.dtb");
               type = "flat_dt";
               arch = "arm64";
               compression = "none";
               load = <0x08300000>;
               hash-1 {
                   algo = "sha1";
               };
           };
       };

       configurations {
           default = "config-1";
           config-1 {
               description = "Default Boot Configuration";
               kernel = "kernel-1";
               fdt = "fdt-1";
           };
       };
   };

How do you compile the FIT image?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate the ``.itb`` binary on your host workstation:

.. code-block:: bash

   mkimage -f px30.its px30_boot.itb

How do you stage and boot the kernel from RAM in U-Boot?
--------------------------------------------------------

U-Boot receives Fastboot transfers into a limited RAM buffer at address
``0x00800800``. To prevent memory corruption and overlap errors, staged
files must be copied out of this buffer to a high memory address
(``0x10000000``) before execution.

How do you stage the FIT image into target RAM?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With ``fastboot usb 0`` active in U-Boot, send the FIT image from your host
PC:

.. code-block:: bash

   fastboot stage px30_boot.itb

How do you boot the staged kernel?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After staging, interrupt Fastboot in the U-Boot console (Ctrl+C), relocate
the staged payload in RAM, set the kernel arguments, and launch ``bootm``:

.. code-block:: bash

   cp.b 0x00800800 0x10000000 0x03D00000
   setenv bootargs "console=ttyS2,115200n8 earlycon=uart8250,mmio32,0xff160000 root=/dev/mmcblk1p2 rootfstype=ext4 rw rootwait"
   bootm 0x10000000:kernel-1 - 0x10000000:fdt-1

How do you automate the boot process with a U-Boot macro?
---------------------------------------------------------

To streamline future boots, save the relocation and boot sequence as a
custom U-Boot environment variable (``yoctobootcmd``).

.. warning::
   **Serial overrun.** Do not copy and paste the entire command string at
   once over the serial terminal: high baud rate input without flow control
   causes dropped characters. Type or paste the variables in smaller
   individual fragments.

.. code-block:: bash

   setenv yoctobootcmd 'cp.b 0x00800800 0x10000000 0x03D00000; setenv bootargs "console=ttyS2,115200n8 earlycon=uart8250,mmio32,0xff160000 root=/dev/mmcblk1p2 rootfstype=ext4 rw rootwait"; bootm 0x10000000:kernel-1 - 0x10000000:fdt-1'
   saveenv

What is the routine for subsequent deployments?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Interrupt the bootloader during power-on to reach the U-Boot prompt
   (``=>``).
2. Start the Fastboot server: ``fastboot usb 0``.
3. Upload the FIT image from the host PC: ``fastboot stage px30_boot.itb``.
4. Interrupt Fastboot (Ctrl+C) and run the macro command:
   ``run yoctobootcmd``.

.. tip::
   Bringing a legacy product onto a mainline kernel and a modern Yocto
   environment? Amarula Solutions handles U-Boot board bring-up, kernel
   upstreaming, and long-term BSP maintenance for Rockchip, i.MX, STM32MP,
   and Allwinner platforms.
   `Contact our embedded team <https://www.amarulasolutions.com/contact/>`_
