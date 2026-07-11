Olimex A33 OlinuXino
####################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

This tutorial will show the details of Olimex A33-OLinuXino board mainline support
and other details like hardware, documentation, schematics are available at `hardware <https://www.olimex.com/Products/OLinuXino/A33/A33-OLinuXino/open-source-hardware>`_ and linux-sunxi

How do you access the hardware?
*******************************
Power supply: External 5V Jack
USB OTG Cable, USB to TTL for debug

How do you build the BSP?
*************************
Image building need host to ready with all necessary tools ready, refer here

How do you build U-Boot?
========================
::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make A33-OLinuXino_defconfig && make

How do you build the Linux kernel?
==================================
::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm sunxi_defconfig
        ARCH=arm make -j 4 zImage dtbs

How do you boot the system?
***************************

How do you boot from SD card?
=============================
Write Boot image

::

   dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1

Now insert the card into A33-OlinuXino board, power on.

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
