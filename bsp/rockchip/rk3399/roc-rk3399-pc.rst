ROC-RK3399-PC
=============

About this
----------

This tutorial will show the details of `ROC-RK3399-PC <http://en.t-firefly.com/product/rocrk3399pc>`_ board mainline support.

Hardware Access
---------------

.. image:: /images/roc-rk3399-pc.jpg

BSP Building
------------

ATF
::

        $ git clone https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git
        $ cd /path/to/trusted-firmware-a
        $ make distcleanclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399 bl31
        $ cp /path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf /path/to/u-boot

U-Boot
::
        
        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rockdev origin/rockdev
        $ make rockpro64-rk3399_defconfig
        $ make

Linux
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make Image dtbs -j 4

Buildroot
::


Booting from
-----------

SPI Flash
::

SD
::

eMMC
::

EFI boot
--------
