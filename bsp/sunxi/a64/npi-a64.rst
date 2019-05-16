FriendlyARM Nanopi A64
######################

This tutorial will show the details of Nanopi A64 board mainline support and other needed details, for more information about `hardware <http://nanopi.io/nanopi-a64.html>`_ and `linux-sunxi <http://linux-sunxi.org/FriendlyARM_NanoPi_A64>`_

Hardware Access
***************
Hardware Access
Serial debug:  4Pin, 2.54mm pitch pin-header 

Power cable: DC 5V/2A USB


.. image:: /images/nanopi_a64.jpeg




BSP Build
*********

Manual Build
============
Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/found/host/tools.html#arm64>`_

Below are the details of Image build for Nanopi A64 board.

ATF
---
::

        git clone https://github.com/apritzel/arm-trusted-firmware.git
        cd arm-trusted-firmware
        make PLAT=sun50iw1p1 bl31
        export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin

U-Boot
------
::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make nanopi_a64_defconfig
        make 

Linux
-----
::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm64 make defconfig
        ARCH=arm64 make -j 4 Image dtbs

Buildroot
=========
It's easy to build entire system using buildroot and mainline supported nanopi-a64 already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/friendlyarm/nanopi-a64/readme.txt>`_ for more info.

::

        git clone git://git.busybox.net/buildroot
        cd buildroot
        make friendlyarm_nanopi_a64_defconfig
        make

Booting
*******

SD Boot
=======
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

Linux
*****
RTL8189ES Wifi
==============
EMAC
====
