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

Host require few tools to build BSP, those are

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
        $ git checkout -b rockchip origin/rockchip
        $ make roc-pc-rk3399_defconfig
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

Distro installer
----------------

There are several ways to build and flash the distributions to external storage devices
like SD, eMMC, USB, SATA. Since the ROC-RK3399-PC has inbuilt SPI Flash, we use this
flash boot with minimal rootfs and install distributions on supported external storage
devices on board.

Prerequisites::

        Power off the board.
        Remove any bootable storage media like SD, eMMC module.
        (Or plug it and make sure it doesn't have bootable images)
        Plug the USB Type-C cable to Type-C 1 port on ROC-RK3399-PC.
        Plug the Debug port with board
        Open minicom with 1500000 8N1
        Power on the board.

Mask ROM mode::

        lsusb command on host pc should show
        Bus 001 Device 020: ID 2207:330c Fuzhou Rockchip Electronics Company RK3399 in Mask ROM mode

If mask rom mode doesn't appear, then::

        Check Prerequisites steps or
        Close SPI CLK and GND pins of J16.

Program SPI Flash::

        rkdeveloptool ld
        rkdeveloptool db rk3399_loader_spinor_v1.15.114.bin
        rkdeveloptool wl 0 roc-rk3399-pc-initramfs-spi.img
        rkdeveloptool rd
