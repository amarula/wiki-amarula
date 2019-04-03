Pine A64
========

Skip to end of metadata
Created by Jagan Teki, last modified on 2017-12-31 Go to start of metadata
This tutorial will show the details of Pine64 board mainline support and other needed details, for more information about hardware and linux-sunxi

Hardware Access

.. image:: /images/pine64.jpeg


BSP Build
Manual Build
ATF
U-Boot
Linux
Buildroot
Booting
SD Write
Buildroot
Hardware Access
Serial debug:  4Pin, 2.54mm pitch pin-header 

Power cable: DC 5V @ 2A USB



BSP Build
Manual Build
Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Pine64 board.

ATF

::

        $ git clone https://github.com/apritzel/arm-trusted-firmware.git
        $ cd arm-trusted-firmware
        $ make PLAT=sun50iw1p1 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin
        
U-Boot

::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make pine64_plus_defconfig
        $ make 

Linux

::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs

Buildroot
It's easy to build entire system using buildroot and mainline supported pine64 already. See read this readme.txt for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make pine64_defconfig
        $ make

Booting
SD Write
Create Dual partition and Insert the SD on host

::

        $ cp /to/linux-next/arch/arm64/boot/Image /media/jagan/BOOT
        $ cp /to/linux-next/arch/arm64/boot/dts/allwinner/sun50i-a64-pine64.dtb /media/jagan/BOOT
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
        # fatload mmc 0 $fdt_addr_r sun50i-a64-pine64.dtb
        # booti $kernel_addr_r - $fdt_addr_r

Buildroot
