NanoPI M4
=========

About this
----------

This tutorial will show the details of `NanoPI M4 <http://wiki.friendlyarm.com/wiki/index.php/NanoPi_M4>`_ board mainline support.

Hardware Access
---------------

.. image:: /images/nanopi_m4.jpg


        UART:   RS232 PL2303 Serial Port
        Power:  USB C-Type

BSP Building
------------

ATF::

        $ git clone https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git
        $ cd /path/to/trusted-firmware-a
        $ make distcleanclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf 

U-Boot::

        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rockchip origin/rockchip
        $ make nanopc-t4-rk3399_defconfig
        $ make

Linux::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make Image dtbs -j 4

Buildroot::

Booting from
-----------

SD::

        $ cd /path/to/u-boot
        $ sudo dd if=u-boot-rockchip.bin of=/dev/mmcblk0 seek=64
        $ sync

Put this SD (or micro-SD) card into your board and reset it. You should see
something like on minicom(1500000 8N1):

Boot log
--------

::

        U-Boot TPL 2020.01-00648-gd87aa5008a-dirty (Jan 23 2020 - 17:22:13)
        Channel 0: LPDDR3, 933MHz
        BW=32 Col=10 Bk=8 CS0 Row=15 CS1 Row=15 CS=2 Die BW=16 Size=2048MB
        Channel 1: LPDDR3, 933MHz
        BW=32 Col=10 Bk=8 CS0 Row=15 CS1 Row=15 CS=2 Die BW=16 Size=2048MB
        256B stride
        256B stride
        Trying to boot from BOOTROM
        Returning to boot ROM...

        U-Boot SPL 2020.01-00648-gd87aa5008a-dirty (Jan 23 2020 - 17:22:13 +0530)
        Trying to boot from MMC1


        U-Boot 2020.01-00648-gd87aa5008a-dirty (Jan 23 2020 - 17:22:13 +0530)

        SoC: Rockchip rk3399
        Reset cause: RST
        Model: FriendlyElec NanoPC-T4
        DRAM:  3.9 GiB
        PMIC:  RK808 
        MMC:   dwmmc@fe310000: 2, dwmmc@fe320000: 1, sdhci@fe330000: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial
        Out:   vidconsole
        Err:   vidconsole
        Model: FriendlyElec NanoPC-T4
        rockchip_dnl_key_pressed: adc_channel_single_shot fail!
        Net:   
        Error: ethernet@fe300000 address not set.
        No ethernet found.

        Hit any key to stop autoboot:  0 
        Invalid bus 0 (err=-19)
        Failed to initialize SPI flash at 0:0 (error -19)
        switch to partitions #0, OK
        mmc0(part 0) is current device
        ** No partition table - mmc 0 **
        switch to partitions #0, OK
        mmc1 is current device
        Scanning mmc 1:1...
        Found /boot/extlinux/extlinux.conf
        Retrieving file: /boot/extlinux/extlinux.conf
        158 bytes read in 6 ms (25.4 KiB/s)
        1:      linux-4.17.0-rc3
        Retrieving file: /boot/Image
        27736576 bytes read in 1185 ms (22.3 MiB/s)
        append: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk0p1 rootwait rw
        Retrieving file: /boot/rk3399-nanopc-t4.dtb
        55886 bytes read in 8 ms (6.7 MiB/s)
        ## Flattened Device Tree blob at 01f00000
           Booting using the fdt blob at 0x1f00000
           Loading Device Tree to 00000000f4f19000, end 00000000f4f29a4d ... OK

        Starting kernel ...
