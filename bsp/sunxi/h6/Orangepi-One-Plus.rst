Orangepi One Plus
#################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

This tutorial will show the details of Orangepi One Plus board mainline support and other details like documentation, hardware schismatic and other needful information is available at `hardware <http://www.orangepi.org/OrangePiOneplus/>`_ and `linux-sunxi <http://linux-sunxi.org/Xunlong_Orange_Pi_One_Plus>`_

How do you access the hardware?
*******************************

.. image:: /images/opi-one-plus.jpg

Serial debug and Power connections

How do you build the BSP?
*************************
Manual Build
============
Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/found/host/tools.html>`_

How do you build ATF?
---------------------
::

        $ git clone https://github.com/ARM-software/arm-trusted-firmware
        $ cd arm-trusted-firmware
        $ sudo CROSS_COMPILE=/to/path/aarch64-linux-gnu- make PLAT=sun50i_h6
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50i_h6/release/bl31.bin
        
How do you build U-Boot?
------------------------
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make orangepi_one_plus_defconfig; $ make

How do you build the Linux kernel?
----------------------------------
::

        $ git clone https://github.com/amarula/linux-amarula
        $ cd linux-amarula
        $ git checkout -b wip-sun-h6 origin/wip-sun-h6
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs

How do you build with Buildroot?
================================
It's easy to build entire system using buildroot and mainline supported  orangepi one plus already.  See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/orangepi/orangepi-one-plus/readme.txt>`_ for more info.

::

        $ git clone https://github.com/amarula/buildroot-amarula
        $ cd buildroot-amarula
        $ git checkout -b wip-sun-h6 origin/wip-sun-h6
        $ make orangepi_one_plus_defconfig
        $ make

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
