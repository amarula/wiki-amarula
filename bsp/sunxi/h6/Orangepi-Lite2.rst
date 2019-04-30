Orangepi Lite2
##############

This tutorial will show the details of Orangepi One Plus board mainline support and other details like documentation, hardware schismatic and other needful information is available at `hardware <http://www.orangepi.org/Orange%20Pi%20Lite%202/>`_ and `linux-sunxi <http://linux-sunxi.org/Xunlong_Orange_Pi_Lite_2>`_ 

BSP Build
*********
Manual Build
============
Image building need host to ready with all necessary tools ready, refer here

ATF
---
::

        $ git clone https://github.com/ARM-software/arm-trusted-firmware
        $ cd arm-trusted-firmware
        $ sudo CROSS_COMPILE=/to/path/aarch64-linux-gnu- make PLAT=sun50i_h6
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50i_h6/release/bl31.bin
       
U-Boot
------
 ::

        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b h6-v1.0a h6-v1.0a
        $ make orangepi_lite_defconfig
        $ make
        
Linux
-----
::

        $ git clone https://github.com/amarula/linux-amarula
        $ cd linux-amarula
        $ git checkout -b h6-v1.0b h6-v1.0b
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs
        
Buildroot
=========
It's easy to build entire system using buildroot and mainline supported  orangepi one plus already.  See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/orangepi/orangepi-lite2/readme.txt>`_ for more info.

::

        $ git clone https://github.com/amarula/buildroot-amarula
        $ cd buildroot-amarula
        $ git checkout -b WIP-H6 origin/WIP-H6
        $ make orangepi_lite2_defconfig
        $ make
