FriendlyARM Nanopi A64
######################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

This tutorial will show the details of Nanopi A64 board mainline support and other needed details, for more information about `hardware <http://nanopi.io/nanopi-a64.html>`_ and `linux-sunxi <http://linux-sunxi.org/FriendlyARM_NanoPi_A64>`_

How do you access the hardware?
*******************************
Hardware Access
Serial debug:  4Pin, 2.54mm pitch pin-header 

Power cable: DC 5V/2A USB


.. image:: /images/nanopi_a64.jpeg




How do you build the BSP?
*************************

Manual Build
============
Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/found/host/tools.html#arm64>`_

Below are the details of Image build for Nanopi A64 board.

How do you build ATF?
---------------------
::

        git clone https://github.com/apritzel/arm-trusted-firmware.git
        cd arm-trusted-firmware
        make PLAT=sun50iw1p1 bl31
        export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin

How do you build U-Boot?
------------------------
::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make nanopi_a64_defconfig
        make 

How do you build the Linux kernel?
----------------------------------
::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm64 make defconfig
        ARCH=arm64 make -j 4 Image dtbs

How do you build with Buildroot?
================================
It's easy to build entire system using buildroot and mainline supported nanopi-a64 already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/friendlyarm/nanopi-a64/readme.txt>`_ for more info.

::

        git clone git://git.busybox.net/buildroot
        cd buildroot
        make friendlyarm_nanopi_a64_defconfig
        make

How do you boot the system?
***************************

How do you boot from SD card?
=============================
Partition the SD card in host with `Single Falcon partitionc <https://wiki.amarulasolutions.com/found/host/tools.html#falcon-partition>`_

::

        git clone https://github.com/openedev/rootfs-sun64
        cp -rf rootfs-sun64/* /media/jagan/rootfs/
        cp /to/linux-next/arch/arm64/boot/Image /media/jagan/rootfs/boot
        cp /to/linux-next/arch/arm64/boot/dts/allwinner/sun50i-a64-nanopi-a64.dtb /media/jagan/rootfs/boot
        [Update boot/extlinux/extlinux.conf]
        cd /to/u-boot
        cat spl/sunxi-spl.bin u-boot.itb > u-boot-sunxi-with-spl.bin
        dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1;
        sync

Insert the SD card and power-on the board. See the Linux boot start from SPL

How do you build the Linux kernel?
**********************************
RTL8189ES Wifi
==============
EMAC
====

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
