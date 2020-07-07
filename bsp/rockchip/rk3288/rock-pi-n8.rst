ROCKPI-N8
==========

This tutorial will show the details of Radxa ROCKPI-N8 board with VMARC RK3288 SOM.

Hardware details and wiki `ROCKPI-N8 <https://wiki.radxa.com/RockpiN8>`_


Hardware Access
---------------

.. image:: /images/rock-pi-n8.jpg

BSP Building
------------

Host require few tools/packages to build BSP, install them from `host <https://wiki.amarulasolutions.com/found/host/tools.html#host>`_

U-Boot
::

        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rock-pi origin/rock-pi
        $ make rock-pi-n8-rk3288_defconfig
        $ make

Linux
::

        $ git clone https://github.com/amarula/linux-amarula.git
        $ cd linux-amarula
	$ git checkout -b rockpi origin/rockpi
        $ make mrproper
        $ ARCH=arm make multi_v7_defconfig
        $ ARCH=arm make LOADADDR=0x02000000 uImage dtbs -j 4


Buildroot
::

	$ git clone git://git.buildroot.net/buildroot
	$ cd buildroot
	$ make rock_pi_n8_defconfig
	$ make


SD Boot

In the output/images directory, flash sdcard.img on to micro sd

::

	$ sudo dd if=output/images/sdcard.img of=/dev/sdX status=progress (X - find it from fdisk -l)
	$ sync

VMARC RK3288 SOM used on this board looks for images on EMMC and then SD(EMMC is the first in boot order).
If EMMC has a valid image then it boots from EMMC. To make SD boot, follow the below link to erase EMMC.
It is also valid for RK3288.

EMMC erase notes `RK3288 EMMC <https://wiki.amarulasolutions.com/bsp/setup/rockchip/rk3399_emmc.html>`_

Put the micro-SD card onto your board in the slot and power the board. You should see something like:

::

	U-Boot TPL 2020.07-rc4 (Jul 06 2020 - 18:50:52)
	Trying to boot from BOOTROM
	Returning to boot ROM...
	Trying to boot from MMC1


	U-Boot 2020.07-rc4 (Jul 06 2020 - 18:50:52 +0530)

	SoC: Rockchip rk3288
	Reset cause: RST
	Model: Radxa ROCK Pi N8
	DRAM:  4 GiB
	PMIC:  RK808
	MMC:   dwmmc@ff0c0000: 1, dwmmc@ff0f0000: 0
	Loading Environment from MMC... *** Warning - bad CRC, using default environment

	In:    serial@ff690000
	Out:   serial@ff690000
	Err:   serial@ff690000
	Model: Radxa ROCK Pi N8
	Net:   No ethernet found.

	Hit any key to stop autoboot:  0
	switch to partitions #0, OK
	mmc1(part 1) is current device
	Scanning mmc 1:3...
	Found /extlinux/extlinux.conf
	Retrieving file: /extlinux/extlinux.conf
	146 bytes read in 5 ms (30.4 KiB/s)
	1:     RK3399_ROCKPI_N8
	Retrieving file: /uImage
	9396800 bytes read in 616 ms (14.5 MiB/s)
	append: console=ttyS2,115200n8 root=/dev/mmcblk0p4 rw rootwait
	Retrieving file: /rk3288-rock-pi-n8.dtb
	39356 bytes read in 18 ms (2.1 MiB/s)
	## Flattened Device Tree blob at 01f00000
	   Booting using the fdt blob at 0x1f00000
	Loading Device Tree to 0fff3000, end 0ffff9bb ... OK

	Starting kernel ...

	[    0.000000] Booting Linux on physical CPU 0x500
	[    0.000000] Linux version 5.7.0-rc1 (suniel@suniel-P5WE0) (gcc version 9.3.0 (Buildroot 2020.08-git-00494-g07339c7-dirty), GNU ld (GNU Binutils) 2.0
	[    0.000000] CPU: ARMv7 Processor [410fc0d1] revision 1 (ARMv7), cr=10c5387d
	[    0.000000] CPU: div instructions available: patching division code
	[    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
	[    0.000000] OF: fdt: Machine model: Radxa ROCK Pi N8
	[    0.000000] Memory policy: Data cache writealloc
	[    0.000000] efi: UEFI not found.
	[    0.000000] cma: Reserved 64 MiB at 0xfa000000
	[    0.000000] percpu: Embedded 20 pages/cpu s49356 r8192 d24372 u81920
	[    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 1038848
	[    0.000000] Kernel command line: console=ttyS2,115200n8 rw rootwait root=/dev/mmcblk0p4 rootfstype=ext4
	[    0.000000] Dentry cache hash table entries: 131072 (order: 7, 524288 bytes, linear)
	[    0.000000] Inode-cache hash table entries: 65536 (order: 6, 262144 bytes, linear)
	[    0.000000] mem auto-init: stack:off, heap alloc:off, heap free:off
	[    0.000000] Memory: 4038496K/4161536K available (13312K kernel code, 1792K rwdata, 5452K rodata, 2048K init, 403K bss, 57504K reserved, 65536K cma-)
	[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
	[    0.000000] rcu: Hierarchical RCU implementation.
	[    0.000000] rcu:     RCU event tracing is enabled.
	[    0.000000] rcu:     RCU restricting CPUs from NR_CPUS=16 to nr_cpu_ids=4.
	[    0.000000] rcu: RCU calculated value of scheduler-enlistment delay is 10 jiffies.
	[    0.000000] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=4
	[    0.000000] NR_IRQS: 16, nr_irqs: 16, preallocated irqs: 16
	[    0.000000] random: get_random_bytes called from start_kernel+0x300/0x4a4 with crng_init=0
	[    0.000000] arch_timer: cp15 timer(s) running at 24.00MHz (phys).
	[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x588fe9dc0, max_idle_ns: 440795202592 ns
	[    0.000006] sched_clock: 56 bits at 24MHz, resolution 41ns, wraps every 4398046511097ns
	[    0.000022] Switching to timer-based delay loop, resolution 41ns
	[    0.005949] Console: colour dummy device 80x30
	[    0.005997] Calibrating delay loop (skipped), value calculated using timer frequency.. 48.00 BogoMIPS (lpj=240000)
	[    0.006014] pid_max: default: 32768 minimum: 301
	[    0.006180] Mount-cache hash table entries: 2048 (order: 1, 8192 bytes, linear)
	[    0.006199] Mountpoint-cache hash table entries: 2048 (order: 1, 8192 bytes, linear)
	[    0.006915] CPU: Testing write buffer coherency: ok
	[    0.006950] CPU0: Spectre v2: using BPIALL workaround
	[    0.007167] CPU0: thread -1, cpu 0, socket 5, mpidr 80000500
	[    0.007920] Setting up static identity map for 0x300000 - 0x3000ac
	[    0.009927] rcu: Hierarchical SRCU implementation.
	[    0.014334] EFI services will not be available.
	[    0.014553] smp: Bringing up secondary CPUs ...
	[    0.016215] CPU1: thread -1, cpu 1, socket 5, mpidr 80000501
	[    0.016223] CPU1: Spectre v2: using BPIALL workaround
	[    0.018003] CPU2: thread -1, cpu 2, socket 5, mpidr 80000502
	[    0.018011] CPU2: Spectre v2: using BPIALL workaround
	[    0.019761] CPU3: thread -1, cpu 3, socket 5, mpidr 80000503
	[    0.019770] CPU3: Spectre v2: using BPIALL workaround
	[    0.019910] smp: Brought up 1 node, 4 CPUs
	[    0.019923] SMP: Total of 4 processors activated (192.00 BogoMIPS).
	[    0.019931] CPU: All CPU(s) started in SVC mode.
	[    0.020624] devtmpfs: initialized
	[    0.029817] VFP support v0.3: implementor 41 architecture 3 part 30 variant d rev 0
	[    0.030125] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
	[    0.030146] futex hash table entries: 1024 (order: 4, 65536 bytes, linear)
	[    0.032048] pinctrl core: initialized pinctrl subsystem
	[    0.034138] thermal_sys: Registered thermal governor 'step_wise'
	[    0.034814] DMI not present or invalid.
	[    0.035247] NET: Registered protocol family 16
	[    0.037639] DMA: preallocated 256 KiB pool for atomic coherent allocations
	[    0.040375] cpuidle: using governor menu
	[    0.041044] No ATAGs?
	[    0.041180] hw-breakpoint: found 5 (+1 reserved) breakpoint and 4 watchpoint registers.
	[    0.041194] hw-breakpoint: maximum watchpoint size is 4 bytes.
	[    0.044438] Serial: AMBA PL011 UART driver
	[    0.107102] AT91: Could not find identification node
	[    0.107815] vcc5v0_sys: supplied by vcc12v_dcin
	[    0.108269] vbus_host: supplied by vcc5v0_sys
	[    0.108709] vbus_typec: supplied by vcc5v0_sys
	[    0.112010] iommu: Default domain type: Translated
	[    0.113458] vgaarb: loaded
	[    0.114414] SCSI subsystem initialized
	[    0.114875] usbcore: registered new interface driver usbfs
	[    0.114929] usbcore: registered new interface driver hub
	[    0.114998] usbcore: registered new device driver usb
	[    0.116660] pps_core: LinuxPPS API ver. 1 registered
	[    0.116671] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
	[    0.116694] PTP clock support registered
	[    0.116905] EDAC MC: Ver: 3.0.0
	[    0.120011] clocksource: Switched to clocksource arch_sys_counter
	[    1.361978] NET: Registered protocol family 2
	[    1.362638] tcp_listen_portaddr_hash hash table entries: 512 (order: 0, 6144 bytes, linear)
	[    1.362677] TCP established hash table entries: 8192 (order: 3, 32768 bytes, linear)
	[    1.362759] TCP bind hash table entries: 8192 (order: 4, 65536 bytes, linear)
	[    1.362950] TCP: Hash tables configured (established 8192 bind 8192)
	[    1.363059] UDP hash table entries: 512 (order: 2, 16384 bytes, linear)
	[    1.363112] UDP-Lite hash table entries: 512 (order: 2, 16384 bytes, linear)
	[    1.363313] NET: Registered protocol family 1
	[    1.363779] RPC: Registered named UNIX socket transport module.
	[    1.363791] RPC: Registered udp transport module.
	[    1.363799] RPC: Registered tcp transport module.
	[    1.363806] RPC: Registered tcp NFSv4.1 backchannel transport module.
	[    1.363818] PCI: CLS 0 bytes, default 64
	[    1.364888] hw perfevents: enabled with armv7_cortex_a12 PMU driver, 7 counters available
	[    1.366309] Initialise system trusted keyrings
	[    1.366489] workingset: timestamp_bits=30 max_order=20 bucket_order=0
	[    1.374312] squashfs: version 4.0 (2009/01/31) Phillip Lougher
	[    1.375102] NFS: Registering the id_resolver key type
	[    1.375130] Key type id_resolver registered
	[    1.375139] Key type id_legacy registered
	[    1.375157] nfs4filelayout_init: NFSv4 File Layout Driver Registering...
	[    1.375192] ntfs: driver 2.1.32 [Flags: R/O].
	[    1.375649] Key type asymmetric registered
	[    1.375661] Asymmetric key parser 'x509' registered
	[    1.375719] bounce: pool size: 64 pages
	[    1.375761] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 247)
	[    1.375771] io scheduler mq-deadline registered
	[    1.375779] io scheduler kyber registered
	[    1.410568] dma-pl330 ff250000.dma-controller: Loaded driver for PL330 DMAC-241330
	[    1.410588] dma-pl330 ff250000.dma-controller:       DBUFF-128x8bytes Num_Chans-8 Num_Peri-20 Num_Events-16
	[    1.411318] dma-pl330 ffb20000.dma-controller: Loaded driver for PL330 DMAC-241330
	[    1.411336] dma-pl330 ffb20000.dma-controller:       DBUFF-64x8bytes Num_Chans-5 Num_Peri-6 Num_Events-10
	[    1.476400] Serial: 8250/16550 driver, 5 ports, IRQ sharing enabled
	[    1.479637] ff180000.serial: ttyS0 at MMIO 0xff180000 (irq = 34, base_baud = 1500000) is a 16550A
	[    1.480908] ff690000.serial: ttyS2 at MMIO 0xff690000 (irq = 35, base_baud = 1500000) is a 16550A
	[    2.243259] printk: console [ttyS2] enabled
	[    2.250329] SuperH (H)SCI(F) driver initialized
	[    2.256667] msm_serial: driver initialized
	[    2.261506] STMicroelectronics ASC driver initialized
	[    2.268898] STM32 USART driver initialized
	[    2.291052] brd: module loaded
	[    2.303028] loop: module loaded
	[    2.319631] libphy: Fixed MDIO Bus: probed
	[    2.325424] CAN device driver interface
	[    2.330915] bgmac_bcma: Broadcom 47xx GBit MAC driver loaded
	[    2.338665] e1000e: Intel(R) PRO/1000 Network Driver - 3.2.6-k
	[    2.345225] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
	[    2.351925] igb: Intel(R) Gigabit Ethernet Network Driver - version 5.6.0-k
	[    2.359706] igb: Copyright (c) 2007-2014 Intel Corporation.
	[    2.369300] clk: failed to reparent mac_clk to clkin_gmac: -22
	[    2.375909] rk_gmac-dwmac ff290000.ethernet: IRQ eth_lpi not found
	[    2.382960] rk_gmac-dwmac ff290000.ethernet: PTP uses main clock
	[    2.389706] rk_gmac-dwmac ff290000.ethernet: phy regulator is not available yet, deferred probing
	[    2.402427] pegasus: v0.9.3 (2013/04/25), Pegasus/Pegasus II USB Ethernet driver
	[    2.410763] usbcore: registered new interface driver pegasus
	[    2.417131] usbcore: registered new interface driver asix
	[    2.423226] usbcore: registered new interface driver ax88179_178a
	[    2.430100] usbcore: registered new interface driver cdc_ether
	[    2.436665] usbcore: registered new interface driver smsc75xx
	[    2.443159] usbcore: registered new interface driver smsc95xx
	[    2.449616] usbcore: registered new interface driver net1080
	[    2.455998] usbcore: registered new interface driver cdc_subset
	[    2.462673] usbcore: registered new interface driver zaurus
	[    2.468953] usbcore: registered new interface driver cdc_ncm
	[    2.477943] dwc2 ff540000.usb: supply vusb_d not found, using dummy regulator
	[    2.486027] dwc2 ff540000.usb: supply vusb_a not found, using dummy regulator
	[    2.560245] dwc2 ff540000.usb: DWC OTG Controller
	[    2.565532] dwc2 ff540000.usb: new USB bus registered, assigned bus number 1
	[    2.573477] dwc2 ff540000.usb: irq 40, io mem 0xff540000
	[    2.580259] hub 1-0:1.0: USB hub found
	[    2.584495] hub 1-0:1.0: 1 port detected
	[    2.589512] dwc2 ff580000.usb: supply vusb_d not found, using dummy regulator
	[    2.597607] dwc2 ff580000.usb: supply vusb_a not found, using dummy regulator
	[    2.740075] dwc2 ff580000.usb: EPs: 10, dedicated fifos, 972 entries in SPRAM
	[    2.748493] dwc2 ff580000.usb: DWC OTG Controller
	[    2.753810] dwc2 ff580000.usb: new USB bus registered, assigned bus number 2
	[    2.761741] dwc2 ff580000.usb: irq 41, io mem 0xff580000
	[    2.768445] hub 2-0:1.0: USB hub found
	[    2.772706] hub 2-0:1.0: 1 port detected
	[    2.778361] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
	[    2.785686] ehci-pci: EHCI PCI platform driver
	[    2.790723] ehci-platform: EHCI generic platform driver
	[    2.796796] ehci-platform ff500000.usb: EHCI Host Controller
	[    2.803172] ehci-platform ff500000.usb: new USB bus registered, assigned bus number 3
	[    2.812123] ehci-platform ff500000.usb: irq 38, io mem 0xff500000
	[    2.840039] ehci-platform ff500000.usb: USB 2.0 started, EHCI 1.00
	[    2.847692] hub 3-0:1.0: USB hub found
	[    2.851953] hub 3-0:1.0: 1 port detected
	[    2.856922] ehci-orion: EHCI orion driver
	[    2.861647] SPEAr-ehci: EHCI SPEAr driver
	[    2.866306] ehci-st: EHCI STMicroelectronics driver
	[    2.871956] ehci-exynos: EHCI Exynos driver
	[    2.876803] ehci-atmel: EHCI Atmel driver
	[    2.881485] tegra-ehci: Tegra EHCI driver
	[    2.886165] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
	[    2.893109] ohci-pci: OHCI PCI platform driver
	[    2.898126] ohci-platform: OHCI generic platform driver
	[    2.904228] ohci-platform ff520000.usb: Generic Platform OHCI controller
	[    2.911768] ohci-platform ff520000.usb: new USB bus registered, assigned bus number 4
	[    2.920775] ohci-platform ff520000.usb: irq 39, io mem 0xff520000
	[    2.994823] hub 4-0:1.0: USB hub found
	[    2.999060] hub 4-0:1.0: 1 port detected
	[    3.004063] SPEAr-ohci: OHCI SPEAr driver
	[    3.008740] ohci-st: OHCI STMicroelectronics driver
	[    3.014403] ohci-atmel: OHCI Atmel driver
	[    3.019874] usbcore: registered new interface driver usb-storage
	[    3.033736] i2c /dev entries driver
	[    3.041510] rtc-hym8563 1-0051: no valid clock/calendar values available
	[    3.049179] rtc-hym8563 1-0051: registered as rtc0
	[    3.054877] rtc-hym8563 1-0051: no valid clock/calendar values available
	[    3.062400] rtc-hym8563 1-0051: hctosys: unable to read the hardware clock
	[    3.073046] rk808 0-001b: chip id: 0x0
	[    3.081112] rk808-regulator rk808-regulator: there is no dvs0 gpio
	[    3.088053] rk808-regulator rk808-regulator: there is no dvs1 gpio
	[    3.095061] DCDC_REG1: supplied by vcc5v0_sys
	[    3.100702] DCDC_REG2: supplied by vcc5v0_sys
	[    3.106147] DCDC_REG3: supplied by vcc5v0_sys
	[    3.111304] DCDC_REG4: supplied by vcc5v0_sys
	[    3.116788] LDO_REG1: supplied by vcc5v0_sys
	[    3.122842] LDO_REG2: supplied by vcc5v0_sys
	[    3.127809] vcca_codec: Bringing 1800000uV into 3300000-3300000uV
	[    3.135696] LDO_REG3: supplied by vcc5v0_sys
	[    3.141635] LDO_REG4: supplied by vcc_io
	[    3.146994] LDO_REG5: supplied by vcc_io
	[    3.152555] LDO_REG6: supplied by vcc5v0_sys
	[    3.158297] LDO_REG7: supplied by vcc5v0_sys
	[    3.164258] LDO_REG8: supplied by vcc5v0_sys
	[    3.170045] SWITCH_REG1: supplied by vcc_io
	[    3.175010] SWITCH_REG2: supplied by vcc_io
	[    3.184612] vccio_flash: supplied by vcc_io
	[    3.202185] cpufreq: cpufreq_online: CPU0: Running at unlisted freq: 500000 KHz
	[    3.210703] cpufreq: cpufreq_online: CPU0: Unlisted initial frequency changed to: 600000 KHz
	[    3.222909] sdhci: Secure Digital Host Controller Interface driver
	[    3.229815] sdhci: Copyright(c) Pierre Ossman
	[    3.236600] Synopsys Designware Multimedia Card Interface Driver
	[    3.244558] dwmmc_rockchip ff0c0000.mmc: IDMAC supports 32-bit address mode.
	[    3.252480] dwmmc_rockchip ff0c0000.mmc: Using internal DMA controller.
	[    3.259869] dwmmc_rockchip ff0c0000.mmc: Version ID is 270a
	[    3.266124] dwmmc_rockchip ff0c0000.mmc: DW MMC controller at irq 30,32 bit host data width,256 deep fifo
	[    3.289946] mmc_host mmc0: Bus speed (slot 0) = 400000Hz (slot req 400000Hz, actual 400000HZ div = 0)
	[    3.314279] dwmmc_rockchip ff0f0000.mmc: IDMAC supports 32-bit address mode.
	[    3.322230] dwmmc_rockchip ff0f0000.mmc: Using internal DMA controller.
	[    3.329626] dwmmc_rockchip ff0f0000.mmc: Version ID is 270a
	[    3.335891] dwmmc_rockchip ff0f0000.mmc: DW MMC controller at irq 31,32 bit host data width,256 deep fifo
	[    3.346703] mmc_host mmc1: card is non-removable.
	[    3.360313] mmc_host mmc0: Bus speed (slot 0) = 50000000Hz (slot req 50000000Hz, actual 50000000HZ div = 0)
	[    3.364588] mmc_host mmc1: Bus speed (slot 0) = 400000Hz (slot req 400000Hz, actual 400000HZ div = 0)
	[    3.371238] mmc0: new high speed SD card at address 0002
	[    3.387742] mmcblk0: mmc0:0002 00000 1.87 GiB
	[    3.394650] sdhci-pltfm: SDHCI platform and OF driver helper
	[    3.402353] ledtrig-cpu: registered to indicate activity on CPUs
	[    3.409628] usbcore: registered new interface driver usbhid
	[    3.415868] usbhid: USB HID core driver
	[    3.422432] drop_monitor: Initializing network drop monitor service
	[    3.423601] GPT:Primary header thinks Alt. header is not at the end of the disk.
	[    3.429751] NET: Registered protocol family 10
	[    3.437705] GPT:524320 != 3911679
	[    3.437706] GPT:Alternate GPT header not at the end of the disk.
	[    3.437708] GPT:524320 != 3911679
	[    3.437709] GPT: Use GNU Parted to correct GPT errors.
	[    3.437727]  mmcblk0: p1 p2 p3 p4
	[    3.442984] Segment Routing with IPv6
	[    3.470324] sit: IPv6, IPv4 and MPLS over IPv4 tunneling driver
	[    3.477160] NET: Registered protocol family 17
	[    3.482131] can: controller area network core (rev 20170425 abi 9)
	[    3.484792] random: fast init done
	[    3.489056] NET: Registered protocol family 29
	[    3.497786] can: raw protocol (rev 20170425)
	[    3.502554] can: broadcast manager protocol (rev 20170425 t)
	[    3.506339] mmc_host mmc1: Bus speed (slot 0) = 50000000Hz (slot req 52000000Hz, actual 50000000HZ div = 0)
	[    3.508873] can: netlink gateway (rev 20190810) max_hops=1
	[    3.521025] mmc1: new high speed MMC card at address 0001
	[    3.526067] Key type dns_resolver registered
	[    3.532240] mmcblk1: mmc1:0001 SLD32G 28.9 GiB
	[    3.536763] ThumbEE CPU extension supported.
	[    3.541953] mmcblk1boot0: mmc1:0001 SLD32G partition 1 4.00 MiB
	[    3.546508] Registering SWP/SWPB emulation handler
	[    3.553368] mmcblk1boot1: mmc1:0001 SLD32G partition 2 4.00 MiB
	[    3.558599] Loading compiled-in X.509 certificates
	[    3.565141] mmcblk1rpmb: mmc1:0001 SLD32G partition 3 4.00 MiB, chardev (235:0)
	[    3.580223] clk: failed to reparent mac_clk to clkin_gmac: -22
	[    3.582322]  mmcblk1: p1 p2 p3 p4 p5
	[    3.586767] rk_gmac-dwmac ff290000.ethernet: IRQ eth_lpi not found
	[    3.597702] rk_gmac-dwmac ff290000.ethernet: PTP uses main clock
	[    3.604474] rk_gmac-dwmac ff290000.ethernet: clock input or output? (input).
	[    3.612356] rk_gmac-dwmac ff290000.ethernet: TX delay(0x28).
	[    3.618675] rk_gmac-dwmac ff290000.ethernet: RX delay(0x11).
	[    3.625001] rk_gmac-dwmac ff290000.ethernet: integrated PHY? (no).
	[    3.631924] rk_gmac-dwmac ff290000.ethernet: cannot get clock clk_mac_speed
	[    3.639698] rk_gmac-dwmac ff290000.ethernet: clock input from PHY
	[    3.651511] rk_gmac-dwmac ff290000.ethernet: init for RGMII
	[    3.657839] rk_gmac-dwmac ff290000.ethernet: User ID: 0x10, Synopsys ID: 0x35
	[    3.665826] rk_gmac-dwmac ff290000.ethernet:         DWMAC1000
	[    3.671668] rk_gmac-dwmac ff290000.ethernet: DMA HW capability register supported
	[    3.680031] rk_gmac-dwmac ff290000.ethernet: RX Checksum Offload Engine supported
	[    3.688389] rk_gmac-dwmac ff290000.ethernet: COE Type 2
	[    3.694226] rk_gmac-dwmac ff290000.ethernet: TX Checksum insertion supported
	[    3.702101] rk_gmac-dwmac ff290000.ethernet: Wake-Up On Lan supported
	[    3.709305] rk_gmac-dwmac ff290000.ethernet: Normal descriptors
	[    3.715919] rk_gmac-dwmac ff290000.ethernet: Ring mode enabled
	[    3.722435] rk_gmac-dwmac ff290000.ethernet: Enable RX Mitigation via HW Watchdog Timer
	[    3.731383] rk_gmac-dwmac ff290000.ethernet: device MAC address 76:ec:85:f3:b0:94
	[    3.843959] libphy: stmmac: probed
	[    3.847845] RTL8211E Gigabit Ethernet stmmac-0:00: attached PHY driver [RTL8211E Gigabit Ethernet] (mii_bus:phy_addr=stmmac-0:00, irq=POLL)
	[    3.861869] RTL8211E Gigabit Ethernet stmmac-0:01: attached PHY driver [RTL8211E Gigabit Ethernet] (mii_bus:phy_addr=stmmac-0:01, irq=POLL)
	[    3.877357] dw-apb-uart ff690000.serial: forbid DMA for kernel console
	[    3.904177] EXT4-fs (mmcblk0p4): mounted filesystem with ordered data mode. Opts: (null)
	[    3.913251] VFS: Mounted root (ext4 filesystem) on device 179:4.
	[    3.922533] devtmpfs: mounted
	[    3.927824] Freeing unused kernel memory: 2048K
	[    3.971529] Run /sbin/init as init process
	[    4.134971] EXT4-fs (mmcblk0p4): re-mounted. Opts: (null)
	Starting syslogd: OK
	Starting klogd: OK
	Running sysctl: OK
	Saving random seed: [    5.214934] random: dd: uninitialized urandom read (512 bytes read)
	OK
	Starting system message bus: [    5.269464] random: dbus-uuidgen: uninitialized urandom read (12 bytes read)
	[    5.277635] random: dbus-uuidgen: uninitialized urandom read (8 bytes read)
	dbus-daemon[177]: Failed to start message bus: Could not get UID and GID for username "dbus"
	done
	Starting network: OK

	Welcome to ROCKPI-N8..!!
	rockpi-n8 login:

use root for login.
