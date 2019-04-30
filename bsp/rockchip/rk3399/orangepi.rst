Orangepi RK3399
###############

This tutorial will show the details of OrangePI RK3399 board mainline support.

Hardware details and wiki `OrangePI RK3399 <http://www.orangepi.org/Orange%20Pi%20RK3399>`_

Hardware Access
***************
.. image:: /images/opi_rk3399.jpg

BSP Build
*********

Manual Build
============

ATF
---
::
        $ git clone https://github.com/ARM-software/arm-trusted-firmware.git
        $ cd /path/to/arm-trusted-firmware
        $ make realclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399
        $ cp /path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf /path/to/u-boot

U-Boot
------
::     
        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rockdev origin/rockdev
        $ make orangepi-rk3399_defconfig
        $ make
        $ make u-boot.itb

Linux
-----
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make Image dtbs -j 4

Buildroot
=========
::
        $ git clone https://github.com/amarula/buildroot-amarula
        $ cd buildroot-amarula
        $ git checkout -b rockdev origin/rockdev
        $ make orangepi_rk3399_defconfig

SD Boot
*******
Create Single partition and Insert the SD on host or use sdcard.img from buildroot.

::

        $ cd /path/to/u-boot
        $ ./tools/mkimage  -n rk3399 -T rksd -d spl/u-boot-spl-dtb.bin out 
        $ sudo dd if=out of=/dev/sdc seek=64
        $ sudo dd if=u-boot.itb of=/dev/sdc seek=16384
        $ sync

If board is always boot from eMMC, refer to
`RK3399 SD Boot Setup <https://wiki.amarulasolutions.com/found/target/rk3399_sd.html>`_

Put this SD (or micro-SD) card into your board and reset it. You should see
something like:

::

        U-Boot SPL board init
        Trying to boot from MMC1

        U-Boot 2019.04-rc4 (Apr 22 2019 - 13:38:40 +0530)

        Model: Orange Pi RK3399 Board
        DRAM:  2 GiB
        MMC:   dwmmc@fe310000: 2, dwmmc@fe320000: 1, sdhci@fe330000: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial@ff1a0000
        Out:   serial@ff1a0000
        Err:   serial@ff1a0000
        Model: Orange Pi RK3399 Board
        Net:   eth0: ethernet@fe300000
        Hit any key to stop autoboot:  0
        switch to partitions #0, OK
        mmc0(part 0) is current device
        ** No partition table - mmc 0 **
        switch to partitions #0, OK
        mmc1 is current device
        Scanning mmc 1:1...
        Found /boot/extlinux/extlinux.conf
        Retrieving file: /boot/extlinux/extlinux.conf
        157 bytes read in 2 ms (76.2 KiB/s)
        1:      OrangePi RK3399
        Retrieving file: /boot/Image
        20886016 bytes read in 943 ms (21.1 MiB/s)
        append: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk1p1 rootwait
        Retrieving file: /boot/rk3399-orangepi.dtb
        55460 bytes read in 5 ms (10.6 MiB/s)
        ## Flattened Device Tree blob at 01f00000
           Booting using the fdt blob at 0x1f00000
           Loading Device Tree to 000000007df18000, end 000000007df288a3 ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
        [    0.000000] Linux version 5.1.0-rc1 (shyam@debian) (gcc version 7.4.0 (Buildroot 2019.05-git-00362-gcd58f3609b-dirty)) #2 SMP PREEMPT Mon Apr 22 13:39
        :32 IST 2019
        [    0.000000] Machine model: Orange Pi RK3399 Board
        [    0.000000] earlycon: uart8250 at MMIO32 0x00000000ff1a0000 (options '')
        [    0.000000] printk: bootconsole [uart8250] enabled
        [    0.000000] efi: Getting EFI parameters from FDT:
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 32 MiB at 0x000000007e000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000200000-0x000000007fffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0x7dba0840-0x7dba1fff]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA32    [mem 0x0000000000200000-0x000000007fffffff]
        [    0.000000]   Normal   empty
        [    0.000000] Movable zone start for each node
        [    0.000000] Early memory node ranges
        [    0.000000]   node   0: [mem 0x0000000000200000-0x000000007fffffff]
        [    0.000000] Initmem setup node 0 [mem 0x0000000000200000-0x000000007fffffff]
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv1.1 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: MIGRATE_INFO_TYPE not supported.
        [    0.000000] psci: SMC Calling Convention v1.1
        [    0.000000] random: get_random_bytes called from start_kernel+0xa8/0x46c with crng_init=0
        [    0.000000] percpu: Embedded 23 pages/cpu @(____ptrval____) s56664 r8192 d29352 u94208
        [    0.000000] Detected VIPT I-cache on CPU0
        [    0.000000] CPU features: detected: ARM erratum 845719
        [    0.000000] CPU features: detected: GIC system register CPU interface
        [    0.000000] Speculative Store Bypass Disable mitigation not required
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 515592
        [    0.000000] Policy zone: DMA32
        [    0.000000] Kernel command line: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk1p1 rootwait
