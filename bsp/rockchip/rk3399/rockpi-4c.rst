ROCKPI-4C
==========

This tutorial will show the details of Radxa ROCKPI-4C board mainline support.

Hardware details and wiki `ROCKPI-4C <https://rockpi.org/rockpi4>`_

If incase the board is not displayed on there website, here are the quick specs:

Single HDMI 2.0 port is replaced with a micro HDMI port and a mini DisplayPort, meaning
two external displays can be connected.
4GB RAM and a WiFi/Bluetooth module.
Rest of the specs are same as its predecessor ROCKPI-4B.

Hardware Access
---------------

.. image:: /images/rockpi_4c.jpg

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
        $ make rock-pi-4-rk3399_defconfig
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
	$ make rockpi_4c_defconfig
	$ make


SD Boot

In the output/images directory, flash sdcard.img on to micro sd

::

	$ sudo dd if=output/images/sdcard.img of=/dev/sdX status=progress (X - find it from fdisk -l)
	$ sync

Put this micro-SD card onto your board in the slot and power the board. You should see something like:


::

	U-Boot TPL 2020.07-rc4 (Jun 16 2020 - 22:29:04)
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

	U-Boot SPL 2020.07-rc4 (Jun 16 2020 - 22:29:04 +0530)
	Trying to boot from MMC1


	U-Boot 2020.07-rc4 (Jun 16 2020 - 22:29:04 +0530)

	SoC: Rockchip rk3399
	Reset cause: POR
	Model: Radxa ROCK Pi 4
	DRAM:  3.9 GiB
	PMIC:  RK808
	MMC:   mmc@fe310000: 2, mmc@fe320000: 1, sdhci@fe330000: 0
	Loading Environment from MMC... Card did not respond to voltage select!
	*** Warning - No block device, using default environment

	In:    serial
	Out:   serial
	Err:   serial
	Model: Radxa ROCK Pi 4
	Net:   eth0: ethernet@fe300000
	Hit any key to stop autoboot:  0
	Card did not respond to voltage select!
	switch to partitions #0, OK
	mmc1 is current device
	Scanning mmc 1:3...
	Found /extlinux/extlinux.conf
	Retrieving file: /extlinux/extlinux.conf
	156 bytes read in 5 ms (30.3 KiB/s)
	1:      RK3399_ROCKPI4C linux
	Retrieving file: /Image
	26288640 bytes read in 1122 ms (22.3 MiB/s)
	append: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk1p4 rw rootwait
	Retrieving file: /rk3399-rock-pi-4.dtb
	54196 bytes read in 7 ms (7.4 MiB/s)
	## Flattened Device Tree blob at 01f00000
	   Booting using the fdt blob at 0x1f00000
	   Loading Device Tree to 00000000f2503000, end 00000000f25133b3 ... OK

	Starting kernel ...

	[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
	[    0.000000] Linux version 5.4.46 (suniel@suniel-P5WE0) (gcc version 8.4.0 (Buildroot 2020.08-git-00273-g8f70124)) #1 SMP PREEMPT Tue Jun 16 22:32:16 IST 2020
	[    0.000000] Machine model: Radxa ROCK Pi 4
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
	[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=6, Nodes=1
	[    0.000000] rcu: Preemptible hierarchical RCU implementation.
	[    0.000000] rcu:     RCU restricting CPUs from NR_CPUS=256 to nr_cpu_ids=6.
	[    0.000000]  Tasks RCU enabled.
	[    0.000000] rcu: RCU calculated value of scheduler-enlistment delay is 25 jiffies.
	[    0.000000] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=6
	[    0.000000] NR_IRQS: 64, nr_irqs: 64, preallocated irqs: 0
	[    0.000000] GICv3: GIC: Using split EOI/Deactivate mode
	[    0.000000] GICv3: 256 SPIs implemented
	[    0.000000] GICv3: 0 Extended SPIs implemented
	[    0.000000] GICv3: Distributor has no Range Selector support
	[    0.000000] GICv3: 16 PPIs implemented
	[    0.000000] GICv3: no VLPI support, no direct LPI support
	[    0.000000] GICv3: CPU0: found redistributor 0 region 0:0x00000000fef00000
	[    0.000000] ITS [mem 0xfee20000-0xfee3ffff]
	[    0.000000] ITS@0x00000000fee20000: allocated 65536 Devices @f4880000 (flat, esz 8, psz 64K, shr 0)
	[    0.000000] ITS: using cache flushing for cmd queue
	[    0.000000] GICv3: using LPI property table @0x00000000f4840000
	[    0.000000] GIC: using cache flushing for LPI property table
	[    0.000000] GICv3: CPU0: using allocated LPI pending table @0x00000000f4850000
	[    0.000000] GICv3: GIC: PPI partition interrupt-partition-0[0] { /cpus/cpu@0[0] /cpus/cpu@1[1] /cpus/cpu@2[2] /cpus/cpu@3[3] }
	[    0.000000] GICv3: GIC: PPI partition interrupt-partition-1[1] { /cpus/cpu@100[4] /cpus/cpu@101[5] }
	[    0.000000] random: get_random_bytes called from start_kernel+0x2b8/0x44c with crng_init=0
	[    0.000000] arch_timer: cp15 timer(s) running at 24.00MHz (phys).
	[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x588fe9dc0, max_idle_ns: 440795202592 ns
	[    0.000006] sched_clock: 56 bits at 24MHz, resolution 41ns, wraps every 4398046511097ns
	[    0.003236] Console: colour dummy device 80x25
	[    0.003659] printk: console [tty0] enabled
	[    0.004065] printk: bootconsole [uart8250] disabled
	[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
	[    0.000000] Linux version 5.4.46 (suniel@suniel-P5WE0) (gcc version 8.4.0 (Buildroot 2020.08-git-00273-g8f70124)) #1 SMP PREEMPT Tue Jun 16 22:32:16 IST 2020
	[    0.000000] Machine model: Radxa ROCK Pi 4
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
	[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=6, Nodes=1
	[    0.000000] rcu: Preemptible hierarchical RCU implementation.
	[    0.000000] rcu:     RCU restricting CPUs from NR_CPUS=256 to nr_cpu_ids=6.
	[    0.000000]  Tasks RCU enabled.
	[    0.000000] rcu: RCU calculated value of scheduler-enlistment delay is 25 jiffies.
	[    0.000000] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=6
	[    0.000000] NR_IRQS: 64, nr_irqs: 64, preallocated irqs: 0
	[    0.000000] GICv3: GIC: Using split EOI/Deactivate mode
	[    0.000000] GICv3: 256 SPIs implemented
	[    0.000000] GICv3: 0 Extended SPIs implemented
	[    0.000000] GICv3: Distributor has no Range Selector support
	[    0.000000] GICv3: 16 PPIs implemented
	[    0.000000] GICv3: no VLPI support, no direct LPI support
	[    0.000000] GICv3: CPU0: found redistributor 0 region 0:0x00000000fef00000
	[    0.000000] ITS [mem 0xfee20000-0xfee3ffff]
	[    0.000000] ITS@0x00000000fee20000: allocated 65536 Devices @f4880000 (flat, esz 8, psz 64K, shr 0)
	[    0.000000] ITS: using cache flushing for cmd queue
	[    0.000000] GICv3: using LPI property table @0x00000000f4840000
	[    0.000000] GIC: using cache flushing for LPI property table
	[    0.000000] GICv3: CPU0: using allocated LPI pending table @0x00000000f4850000
	[    0.000000] GICv3: GIC: PPI partition interrupt-partition-0[0] { /cpus/cpu@0[0] /cpus/cpu@1[1] /cpus/cpu@2[2] /cpus/cpu@3[3] }
	[    0.000000] GICv3: GIC: PPI partition interrupt-partition-1[1] { /cpus/cpu@100[4] /cpus/cpu@101[5] }
	[    0.000000] random: get_random_bytes called from start_kernel+0x2b8/0x44c with crng_init=0
	[    0.000000] arch_timer: cp15 timer(s) running at 24.00MHz (phys).
	[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x588fe9dc0, max_idle_ns: 440795202592 ns
	[    0.000006] sched_clock: 56 bits at 24MHz, resolution 41ns, wraps every 4398046511097ns
	[    0.003236] Console: colour dummy device 80x25
	[    0.003659] printk: console [tty0] enabled
	[    0.004065] printk: bootconsole [uart8250] disabled
	[    0.004647] Calibrating delay loop (skipped), value calculated using timer frequency.. 48.00 BogoMIPS (lpj=96000)
	[    0.004684] pid_max: default: 32768 minimum: 301
	[    0.004828] LSM: Security Framework initializing
	[    0.004943] Mount-cache hash table entries: 8192 (order: 4, 65536 bytes, linear)
	[    0.004990] Mountpoint-cache hash table entries: 8192 (order: 4, 65536 bytes, linear)
	[    0.027292] ASID allocator initialised with 32768 entries
	[    0.035290] rcu: Hierarchical SRCU implementation.
	[    0.043437] Platform MSI: interrupt-controller@fee20000 domain created
	[    0.043839] PCI/MSI: /interrupt-controller@fee00000/interrupt-controller@fee20000 domain created
	[    0.048826] EFI services will not be available.
	[    0.055777] smp: Bringing up secondary CPUs ...
	[    0.088008] Detected VIPT I-cache on CPU1
	[    0.088045] GICv3: CPU1: found redistributor 1 region 0:0x00000000fef20000
	[    0.088062] GICv3: CPU1: using allocated LPI pending table @0x00000000f4860000
	[    0.088111] CPU1: Booted secondary processor 0x0000000001 [0x410fd034]
	[    0.120082] Detected VIPT I-cache on CPU2
	[    0.120111] GICv3: CPU2: found redistributor 2 region 0:0x00000000fef40000
	[    0.120124] GICv3: CPU2: using allocated LPI pending table @0x00000000f4870000
	[    0.120157] CPU2: Booted secondary processor 0x0000000002 [0x410fd034]
	[    0.152186] Detected VIPT I-cache on CPU3
	[    0.152214] GICv3: CPU3: found redistributor 3 region 0:0x00000000fef60000
	[    0.152227] GICv3: CPU3: using allocated LPI pending table @0x00000000f4900000
	[    0.152258] CPU3: Booted secondary processor 0x0000000003 [0x410fd034]
	[    0.184301] CPU features: detected: EL2 vector hardening
	[    0.184311] ARM_SMCCC_ARCH_WORKAROUND_1 missing from firmware
	[    0.184320] Detected PIPT I-cache on CPU4
	[    0.184352] GICv3: CPU4: found redistributor 100 region 0:0x00000000fef80000
	[    0.184365] GICv3: CPU4: using allocated LPI pending table @0x00000000f4910000
	[    0.184401] CPU4: Booted secondary processor 0x0000000100 [0x410fd082]
	[    0.216408] Detected PIPT I-cache on CPU5
	[    0.216433] GICv3: CPU5: found redistributor 101 region 0:0x00000000fefa0000
	[    0.216445] GICv3: CPU5: using allocated LPI pending table @0x00000000f4920000
	[    0.216474] CPU5: Booted secondary processor 0x0000000101 [0x410fd082]
	[    0.216582] smp: Brought up 1 node, 6 CPUs
	[    0.216951] SMP: Total of 6 processors activated.
	[    0.216972] CPU features: detected: 32-bit EL0 Support
	[    0.216993] CPU features: detected: CRC32 instructions
	[    0.231543] CPU: All CPU(s) started at EL2
	[    0.231606] alternatives: patching kernel code
	[    0.234771] devtmpfs: initialized
	[    0.250740] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645041785100000 ns
	[    0.250799] futex hash table entries: 2048 (order: 5, 131072 bytes, linear)
	[    0.252698] pinctrl core: initialized pinctrl subsystem
	[    0.254983] DMI not present or invalid.
	[    0.255511] NET: Registered protocol family 16
	[    0.262003] DMA: preallocated 256 KiB pool for atomic allocations
	[    0.262050] audit: initializing netlink subsys (disabled)
	[    0.262230] audit: type=2000 audit(0.260:1): state=initialized audit_enabled=0 res=1
	[    0.264280] cpuidle: using governor menu
	[    0.264695] hw-breakpoint: found 6 breakpoint and 4 watchpoint registers.
	[    0.267468] Serial: AMBA PL011 UART driver
	[    0.316915] HugeTLB registered 1.00 GiB page size, pre-allocated 0 pages
	[    0.316943] HugeTLB registered 32.0 MiB page size, pre-allocated 0 pages
	[    0.316960] HugeTLB registered 2.00 MiB page size, pre-allocated 0 pages
	[    0.316975] HugeTLB registered 64.0 KiB page size, pre-allocated 0 pages
	[    0.320124] cryptd: max_cpu_qlen set to 1000
	[    0.325939] ACPI: Interpreter disabled.
	[    0.327937] vcc5v0_sys: supplied by vcc12v_dcin
	[    0.328326] vcc3v3_pcie: supplied by vcc5v0_sys
	[    0.328611] vcc3v3_sys: supplied by vcc5v0_sys
	[    0.328982] vcc5v0_host: supplied by vcc5v0_sys
	[    0.329305] vcc5v0_typec: supplied by vcc5v0_sys
	[    0.330379] iommu: Default domain type: Translated
	[    0.332313] vgaarb: loaded
	[    0.332695] SCSI subsystem initialized
	[    0.333176] usbcore: registered new interface driver usbfs
	[    0.333235] usbcore: registered new interface driver hub
	[    0.333320] usbcore: registered new device driver usb
	[    0.334506] pps_core: LinuxPPS API ver. 1 registered
	[    0.334521] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
	[    0.334549] PTP clock support registered
	[    0.334752] EDAC MC: Ver: 3.0.0
	[    0.336413] FPGA manager framework
	[    0.336498] Advanced Linux Sound Architecture Driver Initialized.
	[    0.337252] clocksource: Switched to clocksource arch_sys_counter
	[    0.337425] VFS: Disk quotas dquot_6.6.0
	[    0.337494] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
	[    0.337677] pnp: PnP ACPI: disabled
	[    0.345214] thermal_sys: Registered thermal governor 'step_wise'
	[    0.345218] thermal_sys: Registered thermal governor 'power_allocator'
	[    0.345770] NET: Registered protocol family 2
	[    0.346183] tcp_listen_portaddr_hash hash table entries: 2048 (order: 3, 32768 bytes, linear)
	[    0.346278] TCP established hash table entries: 32768 (order: 6, 262144 bytes, linear)
	[    0.346637] TCP bind hash table entries: 32768 (order: 7, 524288 bytes, linear)
	[    0.347312] TCP: Hash tables configured (established 32768 bind 32768)
	[    0.347443] UDP hash table entries: 2048 (order: 4, 65536 bytes, linear)
	[    0.347587] UDP-Lite hash table entries: 2048 (order: 4, 65536 bytes, linear)
	[    0.347963] NET: Registered protocol family 1
	[    0.348479] RPC: Registered named UNIX socket transport module.
	[    0.348497] RPC: Registered udp transport module.
	[    0.348509] RPC: Registered tcp transport module.
	[    0.348521] RPC: Registered tcp NFSv4.1 backchannel transport module.
	[    0.348540] PCI: CLS 0 bytes, default 64
	[    0.349503] hw perfevents: enabled with armv8_cortex_a53 PMU driver, 7 counters available
	[    0.349804] hw perfevents: enabled with armv8_cortex_a72 PMU driver, 7 counters available
	[    0.350201] kvm [1]: IPA Size Limit: 40bits
	[    0.350986] kvm [1]: vgic-v2@fff20000
	[    0.351025] kvm [1]: GIC system register CPU interface enabled
	[    0.351202] kvm [1]: vgic interrupt IRQ10
	[    0.351410] kvm [1]: Hyp mode initialized successfully
	[    0.360749] Initialise system trusted keyrings
	[    0.360927] workingset: timestamp_bits=44 max_order=20 bucket_order=0
	[    0.367710] squashfs: version 4.0 (2009/01/31) Phillip Lougher
	[    0.368471] NFS: Registering the id_resolver key type
	[    0.368501] Key type id_resolver registered
	[    0.368515] Key type id_legacy registered
	[    0.368535] nfs4filelayout_init: NFSv4 File Layout Driver Registering...
	[    0.368698] 9p: Installing v9fs 9p2000 file system support
	[    0.392693] Key type asymmetric registered
	[    0.392712] Asymmetric key parser 'x509' registered
	[    0.392758] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 245)
	[    0.392776] io scheduler mq-deadline registered
	[    0.392789] io scheduler kyber registered
	[    0.415450] EINJ: ACPI disabled.
	[    0.424421] dma-pl330 ff6d0000.dma-controller: Loaded driver for PL330 DMAC-241330
	[    0.424448] dma-pl330 ff6d0000.dma-controller:       DBUFF-32x8bytes Num_Chans-6 Num_Peri-12 Num_Events-12
	[    0.425633] dma-pl330 ff6e0000.dma-controller: Loaded driver for PL330 DMAC-241330
	[    0.425659] dma-pl330 ff6e0000.dma-controller:       DBUFF-128x8bytes Num_Chans-8 Num_Peri-20 Num_Events-16
	[    0.432096] pwm-regulator: supplied by regulator-dummy
	[    0.437801] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
	[    0.440050] ff180000.serial: ttyS0 at MMIO 0xff180000 (irq = 35, base_baud = 1500000) is a 16550A
	[    0.440204] serial serial0: tty port ttyS0 registered
	[    0.440692] ff1a0000.serial: ttyS2 at MMIO 0xff1a0000 (irq = 36, base_baud = 1500000) is a 16550A
	[    0.535582] printk: console [ttyS2] enabled
	[    0.537685] SuperH (H)SCI(F) driver initialized
	[    0.539008] msm_serial: driver initialized
	[    0.541548] cacheinfo: Unable to detect cache hierarchy for CPU 0
	[    0.550525] loop: module loaded
	[    0.557833] libphy: Fixed MDIO Bus: probed
	[    0.558475] tun: Universal TUN/TAP device driver, 1.6
	[    0.560115] thunder_xcv, ver 1.0
	[    0.560442] thunder_bgx, ver 1.0
	[    0.560766] nicpf, ver 1.0
	[    0.562037] hclge is initializing
	[    0.562343] hns3: Hisilicon Ethernet Network Driver for Hip08 Family - version
	[    0.562983] hns3: Copyright (c) 2017 Huawei Corporation.
	[    0.563512] e1000e: Intel(R) PRO/1000 Network Driver - 3.2.6-k
	[    0.564032] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
	[    0.564596] igb: Intel(R) Gigabit Ethernet Network Driver - version 5.6.0-k
	[    0.565214] igb: Copyright (c) 2007-2014 Intel Corporation.
	[    0.565761] igbvf: Intel(R) Gigabit Virtual Function Network Driver - version 2.4.0-k
	[    0.566456] igbvf: Copyright (c) 2009 - 2012 Intel Corporation.
	[    0.567537] sky2: driver version 1.30
	[    0.568992] VFIO - User Level meta-driver version: 0.3
	[    0.576132] OF: graph: no port node found in /syscon@ff770000/usb2-phy@e450/otg-port
	[    0.585017] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
	[    0.585633] ehci-pci: EHCI PCI platform driver
	[    0.586067] ehci-platform: EHCI generic platform driver
	[    0.588770] ehci-platform fe380000.usb: EHCI Host Controller
	[    0.589322] ehci-platform fe380000.usb: new USB bus registered, assigned bus number 1
	[    0.590120] ehci-platform fe380000.usb: irq 28, io mem 0xfe380000
	[    0.605282] ehci-platform fe380000.usb: USB 2.0 started, EHCI 1.00
	[    0.606414] hub 1-0:1.0: USB hub found
	[    0.606788] hub 1-0:1.0: 1 port detected
	[    0.609600] ehci-platform fe3c0000.usb: EHCI Host Controller
	[    0.610124] ehci-platform fe3c0000.usb: new USB bus registered, assigned bus number 2
	[    0.610928] ehci-platform fe3c0000.usb: irq 30, io mem 0xfe3c0000
	[    0.625277] ehci-platform fe3c0000.usb: USB 2.0 started, EHCI 1.00
	[    0.626347] hub 2-0:1.0: USB hub found
	[    0.626713] hub 2-0:1.0: 1 port detected
	[    0.627557] ehci-orion: EHCI orion driver
	[    0.628134] ehci-exynos: EHCI EXYNOS driver
	[    0.628673] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
	[    0.629266] ohci-pci: OHCI PCI platform driver
	[    0.629716] ohci-platform: OHCI generic platform driver
	[    0.630383] ohci-platform fe3a0000.usb: Generic Platform OHCI controller
	[    0.630996] ohci-platform fe3a0000.usb: new USB bus registered, assigned bus number 3
	[    0.631783] ohci-platform fe3a0000.usb: irq 29, io mem 0xfe3a0000
	[    0.693832] hub 3-0:1.0: USB hub found
	[    0.694204] hub 3-0:1.0: 1 port detected
	[    0.694964] ohci-platform fe3e0000.usb: Generic Platform OHCI controller
	[    0.695576] ohci-platform fe3e0000.usb: new USB bus registered, assigned bus number 4
	[    0.696372] ohci-platform fe3e0000.usb: irq 31, io mem 0xfe3e0000
	[    0.757840] hub 4-0:1.0: USB hub found
	[    0.758208] hub 4-0:1.0: 1 port detected
	[    0.759041] ohci-exynos: OHCI EXYNOS driver
	[    0.760154] xhci-hcd xhci-hcd.0.auto: xHCI Host Controller
	[    0.760664] xhci-hcd xhci-hcd.0.auto: new USB bus registered, assigned bus number 5
	[    0.761500] xhci-hcd xhci-hcd.0.auto: hcc params 0x0220fe64 hci version 0x110 quirks 0x0000000002010010
	[    0.762350] xhci-hcd xhci-hcd.0.auto: irq 224, io mem 0xfe800000
	[    0.763560] hub 5-0:1.0: USB hub found
	[    0.763929] hub 5-0:1.0: 1 port detected
	[    0.764549] xhci-hcd xhci-hcd.0.auto: xHCI Host Controller
	[    0.765053] xhci-hcd xhci-hcd.0.auto: new USB bus registered, assigned bus number 6
	[    0.765765] xhci-hcd xhci-hcd.0.auto: Host supports USB 3.0 SuperSpeed
	[    0.766398] usb usb6: We don't know the algorithms for LPM for this host, disabling LPM.
	[    0.767599] hub 6-0:1.0: USB hub found
	[    0.767965] hub 6-0:1.0: 1 port detected
	[    0.768723] xhci-hcd xhci-hcd.1.auto: xHCI Host Controller
	[    0.769227] xhci-hcd xhci-hcd.1.auto: new USB bus registered, assigned bus number 7
	[    0.770060] xhci-hcd xhci-hcd.1.auto: hcc params 0x0220fe64 hci version 0x110 quirks 0x0000000002010010
	[    0.770933] xhci-hcd xhci-hcd.1.auto: irq 225, io mem 0xfe900000
	[    0.772125] hub 7-0:1.0: USB hub found
	[    0.772499] hub 7-0:1.0: 1 port detected
	[    0.773106] xhci-hcd xhci-hcd.1.auto: xHCI Host Controller
	[    0.773628] xhci-hcd xhci-hcd.1.auto: new USB bus registered, assigned bus number 8
	[    0.774318] xhci-hcd xhci-hcd.1.auto: Host supports USB 3.0 SuperSpeed
	[    0.774952] usb usb8: We don't know the algorithms for LPM for this host, disabling LPM.
	[    0.776170] hub 8-0:1.0: USB hub found
	[    0.776536] hub 8-0:1.0: 1 port detected
	[    0.777633] usbcore: registered new interface driver usb-storage
	[    0.782995] i2c /dev entries driver
	[    0.786758] rk808 0-001b: chip id: 0x0
	[    0.791352] rk808-regulator rk808-regulator: there is no dvs0 gpio
	[    0.791928] rk808-regulator rk808-regulator: there is no dvs1 gpio
	[    0.792536] DCDC_REG1: supplied by vcc5v0_sys
	[    0.793737] DCDC_REG2: supplied by vcc5v0_sys
	[    0.794591] DCDC_REG3: supplied by vcc5v0_sys
	[    0.795193] DCDC_REG4: supplied by vcc5v0_sys
	[    0.796079] LDO_REG1: supplied by vcc5v0_sys
	[    0.797633] LDO_REG2: supplied by vcc5v0_sys
	[    0.798913] LDO_REG3: supplied by vcc5v0_sys
	[    0.800323] LDO_REG4: supplied by vcc5v0_sys
	[    0.801724] LDO_REG5: supplied by vcc5v0_sys
	[    0.803005] LDO_REG6: supplied by vcc5v0_sys
	[    0.804414] LDO_REG7: supplied by vcc5v0_sys
	[    0.805679] LDO_REG8: supplied by vcc5v0_sys
	[    0.807115] SWITCH_REG1: supplied by vcc3v3_sys
	[    0.807744] SWITCH_REG2: supplied by vcc3v3_sys
	[    0.809405] fan53555-regulator 0-0040: FAN53555 Option[8] Rev[1] Detected!
	[    0.810038] fan53555-reg: supplied by vcc5v0_sys
	[    0.812286] fan53555-regulator 0-0041: FAN53555 Option[8] Rev[1] Detected!
	[    0.812912] fan53555-reg: supplied by vcc5v0_sys
	[    0.828166] sdhci: Secure Digital Host Controller Interface driver
	[    0.828712] sdhci: Copyright(c) Pierre Ossman
	[    0.829384] Synopsys Designware Multimedia Card Interface Driver
	[    0.830475] dwmmc_rockchip fe310000.dwmmc: IDMAC supports 32-bit address mode.
	[    0.831120] dwmmc_rockchip fe310000.dwmmc: Using internal DMA controller.
	[    0.831722] dwmmc_rockchip fe310000.dwmmc: Version ID is 270a
	[    0.832248] dwmmc_rockchip fe310000.dwmmc: DW MMC controller at irq 25,32 bit host data width,256 deep fifo
	[    0.833161] dwmmc_rockchip fe310000.dwmmc: allocated mmc-pwrseq
	[    0.833691] mmc_host mmc0: card is non-removable.
	[    0.847262] mmc_host mmc0: Bus speed (slot 0) = 400000Hz (slot req 400000Hz, actual 400000HZ div = 0)
	[    0.861120] dwmmc_rockchip fe320000.dwmmc: IDMAC supports 32-bit address mode.
	[    0.861796] dwmmc_rockchip fe320000.dwmmc: Using internal DMA controller.
	[    0.862398] dwmmc_rockchip fe320000.dwmmc: Version ID is 270a
	[    0.862934] dwmmc_rockchip fe320000.dwmmc: DW MMC controller at irq 26,32 bit host data width,256 deep fifo
	[    0.863851] dwmmc_rockchip fe320000.dwmmc: Got CD GPIO
	[    0.877038] mmc_host mmc1: Bus speed (slot 0) = 400000Hz (slot req 400000Hz, actual 400000HZ div = 0)
	[    0.890080] sdhci-pltfm: SDHCI platform and OF driver helper
	[    0.891313] mmc2: CQHCI version 5.10
	[    0.891489] random: fast init done
	[    0.894687] mmc0: queuing unknown CIS tuple 0x80 (2 bytes)
	[    0.896990] mmc0: queuing unknown CIS tuple 0x80 (3 bytes)
	[    0.899208] mmc0: queuing unknown CIS tuple 0x80 (3 bytes)
	[    0.902773] mmc0: queuing unknown CIS tuple 0x80 (7 bytes)
	[    0.907370] mmc0: queuing unknown CIS tuple 0x81 (9 bytes)
	[    0.917555] mmc2: SDHCI controller on fe330000.sdhci [fe330000.sdhci] using ADMA
	[    0.919501] ledtrig-cpu: registered to indicate activity on CPUs
	[    0.920781] usbcore: registered new interface driver usbhid
	[    0.921294] usbhid: USB HID core driver
	[    0.924344] NET: Registered protocol family 17
	[    0.924849] 9pnet: Installing 9P2000 support
	[    0.925262] Key type dns_resolver registered
	[    0.926287] registered taskstats version 1
	[    0.926681] Loading compiled-in X.509 certificates
	[    0.928419] mmc_host mmc1: Bus speed (slot 0) = 50000000Hz (slot req 50000000Hz, actual 50000000HZ div = 0)
	[    0.929348] mmc1: new high speed SDHC card at address 0001
	[    0.930440] mmcblk1: mmc1:0001 EB1QT 29.8 GiB
	[    0.936620] GPT:Primary header thinks Alt. header is not at the end of the disk.
	[    0.937297] GPT:458784 != 62521343
	[    0.937597] GPT:Alternate GPT header not at the end of the disk.
	[    0.938122] GPT:458784 != 62521343
	[    0.938421] GPT: Use GNU Parted to correct GPT errors.
	[    0.938889]  mmcblk1: p1 p2 p3 p4
	[    0.948584] hctosys: unable to open rtc device (rtc0)
	[    0.949590] ALSA device list:
	[    0.949857]   No soundcards found.
	[    0.950313] ttyS2 - failed to request DMA
	[    0.957332] EXT4-fs (mmcblk1p4): mounted filesystem with ordered data mode. Opts: (null)
	[    0.958069] VFS: Mounted root (ext4 filesystem) on device 179:4.
	[    0.959236] devtmpfs: mounted
	[    0.962344] Freeing unused kernel memory: 5056K
	[    0.970418] mmc_host mmc0: Bus speed (slot 0) = 148500000Hz (slot req 150000000Hz, actual 148500000HZ div = 0)
	[    0.985367] Run /sbin/init as init process
	[    1.054540] EXT4-fs (mmcblk1p4): re-mounted. Opts: (null)
	Starting syslogd: OK
	Starting klogd: OK
	Running sysctl: OK
	Initializing random number generator: OK
	Saving random seed: [    1.102980] random: dd: uninitialized urandom read (512 bytes read)
	OK
	Starting network: [    1.121410] dwmmc_rockchip fe310000.dwmmc: Successfully tuned phase to 171
	[    1.124495] mmc0: new ultra high speed SDR104 SDIO card at address 0001
	[    1.181357] NET: Registered protocol family 10
	[    1.182515] Segment Routing with IPv6
	OK

	Welcome to ROCKPI4C..!!
	rockpi4c login:

use root for login.
