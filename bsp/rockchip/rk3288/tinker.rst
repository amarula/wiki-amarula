Tinker RK3288
#############

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, **Buildroot/Yocto** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation.

This tutorial will show the details of Tinker board mainline support and other needed details, for more information about `hardware <https://www.asus.com/in/Single-Board-Computer/Tinker-Board/>`_

How do you access the hardware?
*******************************
.. image:: /images/tinker.jpg

Serial debug and Power connections

How do you build the BSP?
*************************

Manual Build
============
Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Tinker RK3288 board.
Manual Build

How do you build U-Boot?
------------------------
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make tinker-rk3288_defconfig
        $ make 

How do you build the Linux kernel?
----------------------------------
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm make multi_v7_defconfig
        $ ARCH=arm make -j 4 LOADADDR=0x02000000 uImage dtbs
        $ ARCH=arm make modules -j 4
        $ ARCH=arm make modules_install -j 4

How do you build with Buildroot?
================================
It's easy to build entire system using buildroot and mainline supported Tinker board already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/asus/tinker/readme.txt>`_ for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make asus_tinker_rk3288_defconfig && make

How do you boot from SD card?
*****************************
Create Single partition and Insert the SD on host

::

        $ git clone https://github.com/openedev/rfs-rk3288
        $ cp rfs-rk3288/* /media/jagan/rootfs
        $ cd /path/to/u-boot
        $ ./tools/mkimage -n rk3288 -T rksd -d ./tpl/u-boot-tpl.bin out
        $ cat ./spl/u-boot-spl-dtb.bin >> out
        $ dd if=out of=/dev/mmcblk0 seek=64
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 seek=16384
        $ cp /path/to/linux-next/arch/arm/boot/uImage /media/jagan/rootfs/boot
        $ cp /path/to/linux-next/arch/arm/boot/dts/rk3288-tinker.dtb /media/jagan/rootfs/boot
        $ sync && $ umount /dev/mmcblk0

Falcon Boot
***********
Build U-Boot, Linux manually from above steps, and create falcon mode partition from, here

Once the partitioning done, copy all images like SD Boot.
Configure falcon

::

        U-Boot TPL 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:04:00)
        Trying to boot from BOOTROM
        Returning to boot ROM...

        U-Boot SPL 2018.03-rc2-00018-g339b842-dirty (Feb 18 2018 - 19:57:13 +0530)
        Trying to boot from MMC1
        Expected Linux image is not found. Trying to start U-boot

        U-Boot 2018.03-rc2-00018-g339b842-dirty (Feb 18 2018 - 19:57:13 +0530)

        Model: Tinker-RK3288
        DRAM:  2 GiB
        MMC:   dwmmc@ff0c0000: 1
        Loading Environment from MMC... *** Warning - bad CRC, using default environment


        Failed (-5)
        In:    serial
        Out:   serial
        Err:   serial
        Model: Tinker-RK3288
        Net:   failed to enable clock 0
        No ethernet found.
        Hit any key to stop autoboot:  0

.. tip::
   Need mainline BSP support for Rockchip platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Yocto/Buildroot integration,
   and upstream-first development for RK3288, RK3399, PX30, and RK3568 SoCs.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
