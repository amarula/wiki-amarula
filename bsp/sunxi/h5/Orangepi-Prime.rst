Orangepi Prime
==============

This tutorial will show the details of Orangepi Prime board mainline support and other needed details, for more information about `hardware <http://www.orangepi.org/OrangePiPrime/>`_

Hardware Access

.. image:: /images/opi_prime.jpeg


BSP Build
Manual Build
ATF
U-Boot
Linux
Buildroot
Booting
SD Boot
Buildroot
Hardware Access
Serial debug and Power connections



BSP Build
Manual Build
For manual building refer here for all necessary information.

Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Orangepi Prime board.

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
        $ make orangepi_prime_defconfig
        $ make

Linux

::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs

Buildroot
It's easy to build entire system using buildroot and mainline supported orangepi prime already. See read this readme.txt for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make orangepi_prime_defconfig
        $ make

Booting
SD Boot
Buildroot
