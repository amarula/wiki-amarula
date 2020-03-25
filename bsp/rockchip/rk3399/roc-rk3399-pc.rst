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

Host require few tools to build BSP, those are `host <https://wiki.amarulasolutions.com/found/host/tools.html#host>`_ and
`rockchip <https://wiki.amarulasolutions.com/found/host/tools.html#rockchip>`_

ATF
::

        $ git clone https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git
        $ cd /path/to/trusted-firmware-a
        $ make distcleanclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399 bl31

U-Boot
::
        
        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rockchip origin/rockchip
        $ export BL31=/path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf
        $ make roc-pc-rk3399_defconfig #sd
        (or)
        $ make roc-pc-rk3399-spi_defconfig #spi
        $ make

Linux
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make Image dtbs -j 4

Booting from
-----------

SPI Flash::

        load mmc 1:1 $kernel_addr_r idbloader.img
        sf probe
        sf erase 0 +$filesize
        sf write $kernel_addr_r 0 ${filesize}
        load mmc 1:1 ${kernel_addr_r} u-boot.itb
        sf erase 0x40000 +$filesize
        sf write $kernel_addr_r 0x40000 ${filesize}
SD::

        cd u-boot-amarula
        sudo dd if=u-boot-rockchip.bin of=/dev/mmcblk0 seek=64
        sudo sync
eMMC::

        connect USB-OTG cable.

        (target side)
        # mmc dev 0
        # gpt write mmc 0 $partitions
        # fastboot 0

        (host side)
        cd u-boot-amarula
        sudo fastboot -i 0x2207 flash loader1 idbloader.img
        sudo fastboot -i 0x2207 flash loader2 u-boot.itb

Distroot
--------

There are several ways to build and flash the distributions to external storage
devices like SD, eMMC, USB, SATA.

Since the ROC-RK3399-PC has in built SPI Flash, we use this flash to boot with
initramfs and program the distributions on supported external storage devices
on board using distroot.

All images are available at::

        git clone https://github.com/amarula/bsp-rockchip

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

        cd bsp-rockchip
        unxz roc-rk3399-pc-spinor.img.xz
        sha256sum roc-rk3399-pc-spinor.img
        (check the sha256 values with roc-rk3399-pc-spinor.img.xz.sha256sum)

        rkdeveloptool ld
        rkdeveloptool db rk3399_loader_spinor_v1.15.114.bin
        rkdeveloptool wl 0 roc-rk3399-pc-spinor.img
        rkdeveloptool rd

Program SD card/eMMC/USB/SSD::

        Once SPI booted with initramfs, then install the distroot on selected
        flash device.

        login with root
        # wget --no-check-certificate \
          > https://raw.githubusercontent.com/amarula/bsp-rockchip/master/distroot.sh
        # sh ./distroot.sh

        [distroot] try to program the flash...

        1 SD card
        2 eMMC
        3 USB disk

        Choose the flash [1-3]: 2

        Power off or reboot, the board will pickup the distro based
        on u-boot distboot order.

Buildroot
---------

Assume the disk connected via /dev/mmcblk0 in host::
 
        cd bsp-rockchip
        unxz roc-rk3399-pc-sdcard.img.xz
        sha256sum roc-rk3399-pc-sdcard.img
        (check the sha256 values with roc-rk3399-pc-sdcard.img.xz.sha256sum)
        sudo dd if=roc-rk3399-pc-sdcard.img of=/dev/mmcblk0
        sudo sync
