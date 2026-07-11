SoPine A64
##########

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

This tutorial will show the details of SoPine board mainline support and other needed details, for more information about `hardware <https://www.pine64.org/?page_id=1491>`_ and `linux-sunxi <http://linux-sunxi.org/Pine64>`_

How do you access the hardware?
*******************************
Serial debug:  4Pin, 2.54mm pitch pin-header 

Power cable: DC 5V @ 2A JACK

.. image:: /images/sopine.jpeg

How do you build the BSP?
*************************
Manual Build
============
Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/found/host/tools.html#arm64>`_

Below are the details of Image build for SoPine board.

How do you build ATF?
---------------------
::

        $ git clone https://github.com/apritzel/arm-trusted-firmware.git
        $ cd arm-trusted-firmware
        $ make PLAT=sun50iw1p1 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin
        
How do you build U-Boot?
------------------------
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make sopine_baseboard_defconfig
        $ make 
        
How do you build the Linux kernel?
----------------------------------
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs

How do you build with Buildroot?
================================
It's easy to build entire system using buildroot and mainline supported sopine already. See read this readme.txt for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make pine64_sopine_defconfig
        $ make

How do you write the image to SD?
=================================
Create `Dual partition <https://wiki.amarulasolutions.com/found/host/tools.html#dual-partition>`_ and Insert the SD on host

::

        $ cp /to/linux-next/arch/arm64/boot/Image /media/jagan/BOOT
        $ cp /to/linux-next/arch/arm64/boot/dts/allwinner/sun50i-a64-sopine-baseboard.dtb /media/jagan/BOOT
        $ git clone https://github.com/openedev/rootfs-sun64
        $ cp -rf rootfs-sun64/* /media/jagan/rootfs/
        $ cd /to/u-boot
        $ cat spl/sunxi-spl.bin u-boot.itb > u-boot-sunxi-with-spl.bin
        $ dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1
        $ sync

Insert the SD card and power-on the board. Once U-Boot booted set these and boot Linux

::

        # setenv bootargs console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p2 rootwait
        # fatload mmc 0 $kernel_addr_r Image
        # fatload mmc 0 $fdt_addr_r sun50i-a64-sopine-baseboard.dtb
        # booti $kernel_addr_r - $fdt_addr_r

How do you build with Buildroot?
********************************

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
