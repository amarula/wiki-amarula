ROCKPI-N10
==========

This tutorial will show the details of Radxa ROCKPI-N10 board with VMARC RK3399pro SOM mainline support.

Hardware details and wiki `ROCKPI-N10 <https://wiki.radxa.com/RockpiN10>`_


Hardware Access
---------------

.. image:: /images/rk3399pro-rock-pi-n10.jpg

BSP Building
------------

Host require few tools/packages to build BSP, install them from `host <https://wiki.amarulasolutions.com/found/host/tools.html#host>`_

ATF
::

        $ git clone https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git
        $ cd /path/to/trusted-firmware-a
        $ make distclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399 bl31

U-Boot
::

        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rock-pi origin/rock-pi
        $ export BL31=/path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf
        $ make rock-pi-n10-rk3399pro_defconfig
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

	$ git clone git://git.buildroot.net/buildroot
	$ cd buildroot
	$ make rockpi_n10_defconfig
	$ make


SD Boot

In the output/images directory, flash sdcard.img on to micro sd

::

	$ sudo dd if=output/images/sdcard.img of=/dev/sdX status=progress (X - find it from fdisk -l)
	$ sync

Put this micro-SD card onto your board in the slot and power the board. You should see something like:


::

	U-Boot TPL 2020.07-rc4 (Jun 16 2020 - 19:29:04)
	Channel 0: LPDDR4, 50MHz
	BW=32 Col=10 Bk=8 CS0 Row=15 CS1 Row=15 CS=2 Die BW=16 Size=2048MB
	Channel 1: LPDDR4, 50MHz
	BW=32 Col=10 Bk=8 CS0 Row=15 CS1 Row=15 CS=2 Die BW=16 Size=2048MB
	256B stride
	256B stride
	lpddr4_set_rate: change freq to 400000000 mhz 0, 1
	lpddr4_set_rate: change freq to 800000000 mhz 1, 0
	Trying to boot from BOOTROM
	Returning to boot ROM...

	U-Boot SPL 2020.07-rc4 (Jun 16 2020 - 19:29:04 +0530)
	Trying to boot from MMC1


	U-Boot 2020.07-rc4 (Jun 16 2020 - 19:29:04 +0530)

	SoC: Rockchip rk3399
	Reset cause: POR
	Model: Radxa ROCK Pi N10
	DRAM:  3.9 GiB
	PMIC:  RK808
	MMC:   mmc@fe310000: 2, mmc@fe320000: 1, sdhci@fe330000: 0
	Loading Environment from MMC... Card did not respond to voltage select!
	*** Warning - No block device, using default environment

	In:    serial
	Out:   serial
	Err:   serial
	Model: Radxa ROCK Pi N10
	Net:   eth0: ethernet@fe300000
	Hit any key to stop autoboot:  0
	Card did not respond to voltage select!
	switch to partitions #0, OK
	mmc1 is current device
	Scanning mmc 1:3...
	Found /extlinux/extlinux.conf
	Retrieving file: /extlinux/extlinux.conf
	156 bytes read in 5 ms (30.3 KiB/s)
	1:      RK3399_ROCKPI_N10 linux
	Retrieving file: /Image
	26288640 bytes read in 1122 ms (22.3 MiB/s)
	append: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk1p4 rw rootwait
	Retrieving file: /rk3399pro-rock-pi-n10.dtb
	54196 bytes read in 7 ms (7.4 MiB/s)
	## Flattened Device Tree blob at 01f00000
	   Booting using the fdt blob at 0x1f00000
	   Loading Device Tree to 00000000f2503000, end 00000000f25133b3 ... OK

	Starting kernel ...

	[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
	[    0.000000] Linux version 5.7.2 (suniel@suniel-P5WE0) (gcc version 8.4.0 (Buildroot 2020.08-git-00273-g8f70124)) #1 SMP PREEMPT Tue Jun 16 19:32:16 IST 2020
	[    0.000000] Machine model: Radxa ROCK Pi N10
	[    0.000000] earlycon: uart8250 at MMIO32 0x00000000ff1a0000 (options '')
	[    0.000000] printk: bootconsole [uart8250] enabled
	[    0.000000] efi: Getting EFI parameters from FDT:
	[    0.000000] efi: UEFI not found.
	[    0.000000] cma: Reserved 32 MiB at 0x00000000f6000000
	[    0.000000] NUMA: No NUMA configuration found
	[    0.000000] NUMA: Faking a node at [mem 0x0000000000200000-0x00000000f7ffffff]
	[    0.000000] NUMA: NODE_DATA [mem 0xf57ef800-0xf57f0fff]
	[    0.000000] Zone ranges:
	[    0.000000]   DMA32    [mem 0x0000000000200000-0x00000000f7ffffff]
	[    0.000000]   Normal   empty
	[    0.000000] Movable zone start for each node
	[    0.000000] Early memory node ranges
	[    0.000000]   node   0: [mem 0x0000000000200000-0x00000000f7ffffff]
	[    0.000000] Initmem setup node 0 [mem 0x0000000000200000-0x00000000f7ffffff]
	[    0.000000] psci: probing for conduit method from DT.
	[    0.000000] psci: PSCIv1.1 detected in firmware.
	[    0.000000] psci: Using standard PSCI v0.2 function IDs
	[    0.000000] psci: MIGRATE_INFO_TYPE not supported.
	[    0.000000] psci: SMC Calling Convention v1.0
	[    0.000000] percpu: Embedded 22 pages/cpu s52952 r8192 d28968 u90112
	[    0.000000] Detected VIPT I-cache on CPU0
	[    0.000000] CPU features: detected: ARM erratum 845719
	[    0.000000] CPU features: detected: GIC system register CPU interface
	[    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 999432
	[    0.000000] Policy zone: DMA32
	[    0.000000] Kernel command line: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk1p4 rw rootwait
	[    0.000000] Dentry cache hash table entries: 524288 (order: 10, 4194304 bytes, linear)
	[    0.000000] Inode-cache hash table entries: 262144 (order: 9, 2097152 bytes, linear)
	[    0.000000] mem auto-init: stack:off, heap alloc:off, heap free:off
	[    0.000000] Memory: 3921744K/4061184K available (12220K kernel code, 1864K rwdata, 6448K rodata, 5056K init, 450K bss, 106672K reserved, 32768K cma-reserved)

use root for login.
