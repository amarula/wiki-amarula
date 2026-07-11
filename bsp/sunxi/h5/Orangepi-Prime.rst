Orangepi Prime
##############

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

This tutorial will show the details of Orangepi Prime board mainline support and other needed details, for more information about `hardware <http://www.orangepi.org/OrangePiPrime/>`_

How do you access the hardware?
*******************************
.. image:: /images/opi_prime.jpeg

Serial debug and Power connections

How do you build the BSP?
*************************
Manual Build
============
For manual building refer here for all necessary information.

Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Orangepi Prime board.

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
        $ make orangepi_prime_defconfig
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
It's easy to build entire system using buildroot and mainline supported orangepi prime already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/orangepi/orangepi-prime/readme.txt>`_ for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make orangepi_prime_defconfig
        $ make

How do you boot the system?
***************************
How do you boot from SD card?
=============================
How do you build with Buildroot?
================================

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
