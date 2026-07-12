Amarual A64-Relic
#################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.
This tutorial will show the details of Amarula A64-Relic mainline support and other needed details


How do you build the BSP?
*************************

Manual Build
============
Image building need host to ready with all necessary tools ready, refer `to the host tools page <https://wiki.amarulasolutions.com/found/host/tools.html>`_ for Host and Crosstool

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
        make amarula_a64_relic_defconfig
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

It's easy to build entire system using buildroot and mainline supported bananapi-m64 already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/bananapi/bananapi-m64/readme.txt>`_ for more info.

::

        git clone git://git.busybox.net/buildroot
        cd buildroot
        make amarula_a64_relic_defconfig
        make

How do you boot the system?
***************************
Since the target doesn't support SD card, we need to boot the U-Boot from FEL and update the firmware images

How do you boot via FEL?
========================
Set FEL mode pins and power-on the board

::

        git clone https://github.com/amarula/bsp-a64-relic
        cd bsp-a64-relic/prebuilt
        bash run-u-boot.sh

Interrupt u-boot by pressing enter

How do you write to eMMC?
=========================
on target, create GPT partitions and trigger fastboot

::

        => mmc dev 1
        => gpt write mmc 1 $partitions
        => fastboot 0

on host, write images from host onto eMMC using fastboot

::

        buildroot/output/images
        fastboot -i 0x1f3a flash loader1 sunxi-spl.bin
        fastboot -i 0x1f3a flash loader2 u-boot.itb
        fastboot -i 0x1f3a flash esp boot.vfat
        fastboot -i 0x1f3a flash system rootfs.ext4

How do you configure WiFi?
**************************
System will automatically detect wifi if buildroot images were used, once done follow below steps

::

        # wpa_passphrase ACCESSPOINTNAME >> /etc/wpa_supplicant.conf
         (type password and enter)
        # wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf -B
        # udhcpc -i wlan0
        # ping google.com

How do you set up the GUI interface?
************************************
For Display, Touchscreen, Camera, Sensor see below buildroot from respective github sources

::

        git clone https://github.com/amarula/buildroot-amarula
        cd buildroot-amarula
        git checkout -b a64-relic origin/a64-relic
        make amarula_a64_relic_updated_defconfig
        make

follow flash instruction from board/amarula/a64-relic/readme.txt

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
