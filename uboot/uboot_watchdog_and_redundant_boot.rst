U-BOOT Watchdog and Redundant Boot
==================================
 
Watchdog Testing
################

Testing via Linux kernel crash
******************************

introduce a BUG() somewhere in kernel code path
Kernel Crash causing code

.. code-block:: sh

        --- a/arch/arm/mm/mmu.c
        +++ b/arch/arm/mm/mmu.c
        @@ -695,6 +695,8 @@ static void __init build_mem_type_table(void)
                pr_info("Memory policy: %sData cache %s\n",
                        ecc_mask ? "ECC enabled, " : "", cp->policy);
          
        +       BUG();
        +
                for (i = 0; i < ARRAY_SIZE(mem_types); i++) {
                        struct mem_type *t = &mem_types[i];
                        if (t->prot_l1)


Testing via invalid Rootfs device mounting
******************************************

Pass invalid rootfs device in kernel boot arguments from u-boot

::
        
        setenv bootargs console=${console},${baudrate} root=/dev/invalid_device rootwait rw


Testing via U-BOOT command prompt
*********************************

Use invalid load address

::
        ext4load mmc 0:1 0x400000000 zImage

Redundant Boot
##############
        
Steps
*****

::

        Step1. Enable hardware watchdog
        Step2. Enable Bootcount, bootlimit and related variables
        Step3. Add altbootcmd for recovery or redundant boot. Incase of failure of default boot altbootcmd
               would be used after bootcount exceeds configured value of bootlimit
        
        
        For Example see imx6qdl_icore_mmc_defconfig use.

Here is the demo log. See **altbootcmd** in the logs
****************************************************

::

        U-Boot SPL 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
        Trying to boot from MMC1
        Expected Linux image is not found. Trying to start U-boot
         
         
        U-Boot 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
         
        CPU:   Freescale i.MX6Q rev1.2 at 792MHz
        CPU:   Industrial temperature grade (-40C to 105C) at 23C
        Reset cause: POR
        Model: Engicam i.CoreM6 Quad/Dual Starter Kit
               Watchdog enabled
        DRAM:  512 MiB
        NAND:  512 MiB
        MMC:   FSL_SDHC: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment
         
        No panel detected: default to Amp-WD
        Display: Amp-WD (800x480)
        In:    serial
        Out:   serial
        Err:   serial
        switch to partitions #0, OK
        mmc0 is current device
        Net:  
        Error: ethernet@02188000 address not set.
        eth-1: ethernet@02188000
        Hit any key to stop autoboot:  0
        Booting from mmc ...
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        icorem6qdl> setenv mycmd 'run mmcargs; ext2load mmc 0:1 ${loadaddr} ${image} ; ext2load mmc 0:1 ${fdt_addr} ${fdt_file}; bootm ${loada'
        icorem6qdl> run mycmd
        8932424 bytes read in 463 ms (18.4 MiB/s)
        37834 bytes read in 10 ms (3.6 MiB/s)
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-5.0.0-rc3-00053-g333478a7e
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    8932360 Bytes = 8.5 MiB
           Load Address: 10008000
           Entry Point:  10008000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c3c9
         
        Starting kernel ...
         
         
        U-Boot SPL 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
        Trying to boot from MMC1
        Expected Linux image is not found. Trying to start U-boot
         
         
        U-Boot 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
         
        CPU:   Freescale i.MX6Q rev1.2 at 792MHz
        CPU:   Industrial temperature grade (-40C to 105C) at 44C
        Reset cause: WDOG
        Model: Engicam i.CoreM6 Quad/Dual Starter Kit
               Watchdog enabled
        DRAM:  512 MiB
        NAND:  512 MiB
        MMC:   FSL_SDHC: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment
         
        No panel detected: default to Amp-WD
        Display: Amp-WD (800x480)
        In:    serial
        Out:   serial
        Err:   serial
        switch to partitions #0, OK
        mmc0 is current device
        Net:  
        Error: ethernet@02188000 address not set.
        eth-1: ethernet@02188000
        Hit any key to stop autoboot:  0
        Booting from mmc ...
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        icorem6qdl> setenv mycmd 'run mmcargs; ext2load mmc 0:1 ${loadaddr} ${image} ; ext2load mmc 0:1 ${fdt_addr} ${fdt_file}; bootm ${loada'
        icorem6qdl> saveenv
        Saving Environment to MMC... Writing to MMC(0)... OK
        icorem6qdl> run mycmd
        8932424 bytes read in 465 ms (18.3 MiB/s)
        37834 bytes read in 10 ms (3.6 MiB/s)
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-5.0.0-rc3-00053-g333478a7e
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    8932360 Bytes = 8.5 MiB
           Load Address: 10008000
           Entry Point:  10008000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c3c9
         
        Starting kernel ...
         
         
        U-Boot SPL 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
        Trying to boot from MMC1
        Expected Linux image is not found. Trying to start U-boot
         
         
        U-Boot 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
         
        CPU:   Freescale i.MX6Q rev1.2 at 792MHz
        CPU:   Industrial temperature grade (-40C to 105C) at 48C
        Reset cause: WDOG
        Model: Engicam i.CoreM6 Quad/Dual Starter Kit
               Watchdog enabled
        DRAM:  512 MiB
        NAND:  512 MiB
        MMC:   FSL_SDHC: 0
        Loading Environment from MMC... OK
        No panel detected: default to Amp-WD
        Display: Amp-WD (800x480)
        In:    serial
        Out:   serial
        Err:   serial
        switch to partitions #0, OK
        mmc0 is current device
        Net:  
        Error: ethernet@02188000 address not set.
        eth-1: ethernet@02188000
        Hit any key to stop autoboot:  0
        Booting from mmc ...
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        ** Unrecognized filesystem type **
        icorem6qdl> run m
          mmcargs mmcautodetect mmcboot mmcdev mmcpart mmcroot modeboot mycmd
        icorem6qdl> run mycmd
        8932424 bytes read in 463 ms (18.4 MiB/s)
        37834 bytes read in 10 ms (3.6 MiB/s)
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-5.0.0-rc3-00053-g333478a7e
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    8932360 Bytes = 8.5 MiB
           Load Address: 10008000
           Entry Point:  10008000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c3c9
         
        Starting kernel ...
         
         
        U-Boot SPL 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
        Trying to boot from MMC1
        Expected Linux image is not found. Trying to start U-boot
         
         
        U-Boot 2019.01-00357-gc9632fd11e10-dirty (Feb 06 2019 - 12:35:24 +0530)
         
        CPU:   Freescale i.MX6Q rev1.2 at 792MHz
        CPU:   Industrial temperature grade (-40C to 105C) at 52C
        Reset cause: WDOG
        Model: Engicam i.CoreM6 Quad/Dual Starter Kit
               Watchdog enabled
        DRAM:  512 MiB
        NAND:  512 MiB
        MMC:   FSL_SDHC: 0
        Loading Environment from MMC... OK
        No panel detected: default to Amp-WD
        Display: Amp-WD (800x480)
        In:    serial
        Out:   serial
        Err:   serial
        switch to partitions #0, OK
        mmc0 is current device
        Net:  
        Error: ethernet@02188000 address not set.
        eth-1: ethernet@02188000
        \*\* Warning: Bootlimit (3) exceeded. Using altbootcmd. \*\*
        Hit any key to stop autoboot:  0
        Recovery Boot from mmc ...
        8931720 bytes read in 459 ms (18.6 MiB/s)
        37834 bytes read in 10 ms (3.6 MiB/s)
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-5.0.0-rc3-00055-gcfeb525f4
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    8931656 Bytes = 8.5 MiB
           Load Address: 10008000
           Entry Point:  10008000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c3c9
         
        Starting kernel ...
         
        [    0.000000] Booting Linux on physical CPU 0x0
        [    0.000000] Linux version 5.0.0-rc3-00055-gcfeb525f403f-dirty (shyam@debian) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) 9
        [    0.000000] CPU: ARMv7 Processor [412fc09a] revision 10 (ARMv7), cr=10c5387d
        [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        [    0.000000] OF: fdt: Machine model: Engicam i.CoreM6 Quad/Dual Starter Kit
        [    0.000000] Memory policy: Data cache writealloc
        [    0.000000] cma: Reserved 64 MiB at 0x2c000000
        [    0.000000] random: get_random_bytes called from start_kernel+0x8c/0x478 with crng_init=0
        [    0.000000] percpu: Embedded 18 pages/cpu @(ptrval) s42088 r8192 d23448 u73728
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 130048
        [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/mmcblk0p2 rootwait rw
        [    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)
        [    0.000000] Inode-cache hash table entries: 32768 (order: 5, 131072 bytes)
        [    0.000000] Memory: 427728K/524288K available (11264K kernel code, 931K rwdata, 3928K rodata, 1024K init, 7588K bss, 31024K reserve)
        [    0.000000] Virtual kernel memory layout:
        [    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
        [    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
        [    0.000000]     vmalloc : 0xe0800000 - 0xff800000   ( 496 MB)
        [    0.000000]     lowmem  : 0xc0000000 - 0xe0000000   ( 512 MB)
        [    0.000000]     pkmap   : 0xbfe00000 - 0xc0000000   (   2 MB)
        [    0.000000]     modules : 0xbf000000 - 0xbfe00000   (  14 MB)
        [    0.000000]       .text : 0x(ptrval) - 0x(ptrval)   (12256 kB)
        [    0.000000]       .init : 0x(ptrval) - 0x(ptrval)   (1024 kB)
        [    0.000000]       .data : 0x(ptrval) - 0x(ptrval)   ( 932 kB)
        [    0.000000]        .bss : 0x(ptrval) - 0x(ptrval)   (7589 kB)
        [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
        [    0.000000] Running RCU self tests
        [    0.000000] rcu: Hierarchical RCU implementation.
        [    0.000000] rcu:     RCU event tracing is enabled.
        [    0.000000] rcu:     RCU lockdep checking is enabled.
        [    0.000000] rcu: RCU calculated value of scheduler-enlistment delay is 10 jiffies.
        [    0.000000] NR_IRQS: 16, nr_irqs: 16, preallocated irqs: 16
        [    0.000000] L2C-310 errata 752271 769419 enabled
        [    0.000000] L2C-310 enabling early BRESP for Cortex-A9
        [    0.000000] L2C-310 full line of zeros enabled for Cortex-A9
        [    0.000000] L2C-310 ID prefetch enabled, offset 16 lines
        [    0.000000] L2C-310 dynamic clock gating enabled, standby mode enabled
        [    0.000000] L2C-310 cache controller enabled, 16 ways, 1024 kB
        [    0.000000] L2C-310: CACHE_ID 0x410000c7, AUX_CTRL 0x76470001
        [    0.000000] Switching to timer-based delay loop, resolution 333ns
        [    0.000008] sched_clock: 32 bits at 3000kHz, resolution 333ns, wraps every 715827882841ns
        [    0.000036] clocksource: mxc_timer1: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 637086815595 ns
        [    0.001504] Console: colour dummy device 80x30
        [    0.001546] Lock dependency validator: Copyright (c) 2006 Red Hat, Inc., Ingo Molnar
        [    0.001564] ... MAX_LOCKDEP_SUBCLASSES:  8
        [    0.001580] ... MAX_LOCK_DEPTH:          48
        [    0.001597] ... MAX_LOCKDEP_KEYS:        8191
        [    0.001613] ... CLASSHASH_SIZE:          4096
        [    0.001628] ... MAX_LOCKDEP_ENTRIES:     32768
        [    0.001644] ... MAX_LOCKDEP_CHAINS:      65536
        [    0.001660] ... CHAINHASH_SIZE:          32768
        [    0.001676]  memory used by lock dependency info: 4591 kB
        [    0.001692]  per task-struct memory footprint: 1536 bytes
        [    0.001779] Calibrating delay loop (skipped), value calculated using timer frequency.. 6.00 BogoMIPS (lpj=30000)
        [    0.001808] pid_max: default: 32768 minimum: 301
        [    0.002147] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
        [    0.002179] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
        [    0.004573] CPU: Testing write buffer coherency: ok
        [    0.004655] CPU0: Spectre v2: using BPIALL workaround
        [    0.005873] CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
        [    0.008041] Setting up static identity map for 0x10100000 - 0x10100078
        [    0.008575] rcu: Hierarchical SRCU implementation.
        [    0.010759] smp: Bringing up secondary CPUs ...
        [    0.013085] CPU1: thread -1, cpu 1, socket 0, mpidr 80000001
        [    0.013095] CPU1: Spectre v2: using BPIALL workaround
        [    0.015688] CPU2: thread -1, cpu 2, socket 0, mpidr 80000002
        [    0.015698] CPU2: Spectre v2: using BPIALL workaround
        [    0.017734] CPU3: thread -1, cpu 3, socket 0, mpidr 80000003
        [    0.017744] CPU3: Spectre v2: using BPIALL workaround
        [    0.018117] smp: Brought up 1 node, 4 CPUs
        [    0.018142] SMP: Total of 4 processors activated (24.00 BogoMIPS).
        [    0.018161] CPU: All CPU(s) started in SVC mode.
        [    0.021099] devtmpfs: initialized
        [    0.044521] VFP support v0.3: implementor 41 architecture 3 part 30 variant 9 rev 4
        [    0.046699] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
        [    0.046764] futex hash table entries: 1024 (order: 4, 65536 bytes)
        [    0.050710] pinctrl core: initialized pinctrl subsystem
        [    0.055218] NET: Registered protocol family 16
        [    0.076855] DMA: preallocated 256 KiB pool for atomic coherent allocations
        [    0.079993] cpuidle: using governor menu
        [    0.080245] CPU identified as i.MX6Q, silicon rev 1.2
        [    0.098164] vdd1p1: supplied by regulator-dummy
        [    0.099863] vdd3p0: supplied by regulator-dummy
        [    0.101079] vdd2p5: supplied by regulator-dummy
        [    0.102258] vddarm: supplied by regulator-dummy
        [    0.103531] vddpu: supplied by regulator-dummy
        [    0.104724] vddsoc: supplied by regulator-dummy
        [    0.126853] No ATAGs?
        [    0.127298] hw-breakpoint: found 5 (+1 reserved) breakpoint and 1 watchpoint registers.
        [    0.127409] hw-breakpoint: maximum watchpoint size is 4 bytes.
        [    0.130289] imx6q-pinctrl 20e0000.iomuxc: initialized IMX pinctrl driver
        [    0.191353] mxs-dma 110000.dma-apbh: initialized
        [    0.198047] vgaarb: loaded
        [    0.199043] SCSI subsystem initialized
        [    0.200375] usbcore: registered new interface driver usbfs
        [    0.200583] usbcore: registered new interface driver hub
        [    0.200814] usbcore: registered new device driver usb
        [    0.201111] usb_phy_generic usbphynop1: usbphynop1 supply vcc not found, using dummy regulator
        [    0.201505] usb_phy_generic usbphynop1: Linked as a consumer to regulator.0
        [    0.201911] usb_phy_generic usbphynop2: usbphynop2 supply vcc not found, using dummy regulator
        [    0.202112] usb_phy_generic usbphynop2: Linked as a consumer to regulator.0
        [    0.205384] i2c i2c-0: IMX I2C adapter registered
        [    0.205425] i2c i2c-0: can't use DMA, using PIO instead.
        [    0.206623] i2c i2c-1: IMX I2C adapter registered
        [    0.206659] i2c i2c-1: can't use DMA, using PIO instead.
        [    0.207878] i2c i2c-2: IMX I2C adapter registered
        [    0.207917] i2c i2c-2: can't use DMA, using PIO instead.
        [    0.208201] media: Linux media interface: v0.10
        [    0.208305] videodev: Linux video capture interface: v2.00
        [    0.208742] pps_core: LinuxPPS API ver. 1 registered
        [    0.208764] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
        [    0.208821] PTP clock support registered
        [    0.209711] Advanced Linux Sound Architecture Driver Initialized.
        [    0.212954] Bluetooth: Core ver 2.22
        [    0.213058] NET: Registered protocol family 31
        [    0.213079] Bluetooth: HCI device and connection manager initialized
        [    0.213186] Bluetooth: HCI socket layer initialized
        [    0.213223] Bluetooth: L2CAP socket layer initialized
        [    0.213356] Bluetooth: SCO socket layer initialized
        [    0.215407] clocksource: Switched to clocksource mxc_timer1
        [    0.774786] VFS: Disk quotas dquot_6.6.0
        [    0.774955] VFS: Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
        [    0.801135] NET: Registered protocol family 2
        [    0.803249] tcp_listen_portaddr_hash hash table entries: 256 (order: 1, 10240 bytes)
        [    0.803328] TCP established hash table entries: 4096 (order: 2, 16384 bytes)
        [    0.803426] TCP bind hash table entries: 4096 (order: 5, 147456 bytes)
        [    0.804005] TCP: Hash tables configured (established 4096 bind 4096)
        [    0.804485] UDP hash table entries: 256 (order: 2, 20480 bytes)
        [    0.804606] UDP-Lite hash table entries: 256 (order: 2, 20480 bytes)
        [    0.805075] NET: Registered protocol family 1
        [    0.807225] RPC: Registered named UNIX socket transport module.
        [    0.807305] RPC: Registered udp transport module.
        [    0.807327] RPC: Registered tcp transport module.
        [    0.807346] RPC: Registered tcp NFSv4.1 backchannel transport module.
        [    0.810042] hw perfevents: no interrupt-affinity property for /pmu, guessing.
        [    0.810684] hw perfevents: enabled with armv7_cortex_a9 PMU driver, 7 counters available
        [    0.814986] Initialise system trusted keyrings
        [    0.815833] workingset: timestamp_bits=30 max_order=17 bucket_order=0
        [    0.832211] NFS: Registering the id_resolver key type
        [    0.832357] Key type id_resolver registered
        [    0.832439] Key type id_legacy registered
        [    0.832610] jffs2: version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
        [    0.833999] fuse init (API version 7.28)
        [    0.859230] Key type asymmetric registered
        [    0.859370] Asymmetric key parser 'x509' registered
        [    0.859549] io scheduler mq-deadline registered
        [    0.859576] io scheduler kyber registered
        [    0.866067] pwm-backlight backlight-lvds: backlight-lvds supply power not found, using dummy regulator
        [    0.866303] pwm-backlight backlight-lvds: Linked as a consumer to regulator.0
        [    0.872051] imx-sdma 20ec000.sdma: Direct firmware load for imx/sdma/sdma-imx6q.bin failed with error -2
        [    0.872154] imx-sdma 20ec000.sdma: Falling back to syfs fallback for: imx/sdma/sdma-imx6q.bin
        [    0.880744] imx-pgc-pd imx-pgc-power-domain.0: DMA mask not set
        [    0.881134] imx-pgc-pd imx-pgc-power-domain.0: Linked as a consumer to 20dc000.gpc
        [    0.881266] imx-pgc-pd imx-pgc-power-domain.1: DMA mask not set
        [    0.881554] imx-pgc-pd imx-pgc-power-domain.1: Linked as a consumer to regulator.5
        [    0.881947] PU : no governor for states
        [    0.881998] imx-pgc-pd imx-pgc-power-domain.1: Linked as a consumer to 20dc000.gpc
        [    0.885223] 21f0000.serial: ttymxc3 at MMIO 0x21f0000 (irq = 67, base_baud = 5000000) is a IMX
        [    1.810837] printk: console [ttymxc3] enabled
        [    1.836668] etnaviv etnaviv: bound 130000.gpu (ops gpu_ops)
        [    1.842877] etnaviv etnaviv: bound 134000.gpu (ops gpu_ops)
        [    1.849055] etnaviv etnaviv: bound 2204000.gpu (ops gpu_ops)
        [    1.854749] etnaviv-gpu 130000.gpu: model: GC2000, revision: 5108
        [    1.876268] etnaviv-gpu 134000.gpu: model: GC320, revision: 5007
        [    1.897970] etnaviv-gpu 2204000.gpu: model: GC355, revision: 1215
        [    1.904099] etnaviv-gpu 2204000.gpu: Ignoring GPU with VG and FE2.0
        [    1.912886] [drm] Initialized etnaviv 1.2.0 20151214 for etnaviv on minor 0
        [    1.923751] imx-ipuv3 2400000.ipu: IPUv3H probed
        [    1.931085] [drm] Supports vblank timestamp caching Rev 2 (21.10.2013).
        [    1.937832] [drm] No driver support for vblank timestamp query.
        [    1.945181] imx-drm display-subsystem: bound imx-ipuv3-crtc.2 (ops ipu_crtc_ops)
        [    1.952935] imx-drm display-subsystem: bound imx-ipuv3-crtc.3 (ops ipu_crtc_ops)
        [    1.960684] imx-drm display-subsystem: bound imx-ipuv3-crtc.6 (ops ipu_crtc_ops)
        [    1.968408] imx-drm display-subsystem: bound imx-ipuv3-crtc.7 (ops ipu_crtc_ops)
        [    1.976921] imx-drm display-subsystem: bound ldb (ops imx_ldb_ops)
        [    1.985330] [drm] Initialized imx-drm 1.0.0 20120507 for display-subsystem on minor 1
        [    2.056674] Console: switching to colour frame buffer device 100x30
        [    2.075519] imx-drm display-subsystem: fb0: DRM emulated frame buffer device
        [    2.083101] imx-ipuv3 2800000.ipu: IPUv3H probed
        [    2.110558] brd: module loaded
        [    2.142326] loop: module loaded
        [    2.165809] random: fast init done
        [    2.171104] nand: device found, Manufacturer ID: 0x2c, Chip ID: 0xdc
        [    2.177542] nand: Micron MT29F4G08ABAEAH4
        [    2.181575] nand: 512 MiB, SLC, erase size: 256 KiB, page size: 4096, OOB size: 224
        [    2.191704] Bad block table found at page 131008, version 0x01
        [    2.198203] Bad block table found at page 130944, version 0x01
        [    2.210939] gpmi-nand 112000.gpmi-nand: driver registered.
        [    2.220473] libphy: Fixed MDIO Bus: probed
        [    2.225909] CAN device driver interface
        [    2.230367] flexcan 2090000.flexcan: Linked as a consumer to regulator.9
        [    2.238724] flexcan 2090000.flexcan: device registered (reg_base=(ptrval), irq=30)
        [    2.246863] flexcan 2094000.flexcan: Linked as a consumer to regulator.9
        [    2.254876] flexcan 2094000.flexcan: device registered (reg_base=(ptrval), irq=31)
        [    2.264681] fec 2188000.ethernet: 2188000.ethernet supply phy not found, using dummy regulator
        [    2.273612] fec 2188000.ethernet: Linked as a consumer to regulator.0
        [    2.284032] pps pps0: new PPS source ptp0
        [    2.289205] fec 2188000.ethernet (unnamed net_device) (uninitialized): Invalid MAC address: 00:00:00:00:00:00
        [    2.299213] fec 2188000.ethernet (unnamed net_device) (uninitialized): Using random MAC address: 8e:87:3f:4d:42:ea
        [    2.317041] libphy: fec_enet_mii_bus: probed
        [    2.322321] fec 2188000.ethernet eth0: registered PHC device 0
        [    2.329728] usbcore: registered new interface driver r8152
        [    2.335322] usbcore: registered new interface driver lan78xx
        [    2.341164] usbcore: registered new interface driver asix
        [    2.346720] usbcore: registered new interface driver ax88179_178a
        [    2.352920] usbcore: registered new interface driver cdc_ether
        [    2.358927] usbcore: registered new interface driver smsc95xx
        [    2.364771] usbcore: registered new interface driver net1080
        [    2.370572] usbcore: registered new interface driver cdc_subset
        [    2.376640] usbcore: registered new interface driver zaurus
        [    2.382317] usbcore: registered new interface driver MOSCHIP usb-ethernet driver
        [    2.389903] usbcore: registered new interface driver cdc_ncm
        [    2.395633] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
        [    2.402179] ehci-pci: EHCI PCI platform driver
        [    2.406770] ehci-mxc: Freescale On-Chip EHCI Host driver
        [    2.412807] usbcore: registered new interface driver usb-storage
        [    2.422221] imx_usb 2184000.usb: Linked as a consumer to regulator.11
        [    2.435459] ci_hdrc ci_hdrc.0: EHCI Host Controller
        [    2.440653] ci_hdrc ci_hdrc.0: new USB bus registered, assigned bus number 1
        [    2.475472] ci_hdrc ci_hdrc.0: USB 2.0 started, EHCI 1.00
        [    2.482127] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.00
        [    2.490622] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
        [    2.497918] usb usb1: Product: EHCI Host Controller
        [    2.502818] usb usb1: Manufacturer: Linux 5.0.0-rc3-00055-gcfeb525f403f-dirty ehci_hcd
        [    2.510795] usb usb1: SerialNumber: ci_hdrc.0
        [    2.518141] hub 1-0:1.0: USB hub found
        [    2.522161] hub 1-0:1.0: 1 port detected
        [    2.529858] imx_usb 2184200.usb: Linked as a consumer to regulator.10
        [    2.540605] ci_hdrc ci_hdrc.1: EHCI Host Controller
        [    2.545615] ci_hdrc ci_hdrc.1: new USB bus registered, assigned bus number 2
        [    2.575437] ci_hdrc ci_hdrc.1: USB 2.0 started, EHCI 1.00
        [    2.581377] usb usb2: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.00
        [    2.589739] usb usb2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
        [    2.597041] usb usb2: Product: EHCI Host Controller
        [    2.601942] usb usb2: Manufacturer: Linux 5.0.0-rc3-00055-gcfeb525f403f-dirty ehci_hcd
        [    2.609931] usb usb2: SerialNumber: ci_hdrc.1
        [    2.615644] hub 2-0:1.0: USB hub found
        [    2.619510] hub 2-0:1.0: 1 port detected
        [    2.633709] input: max11801_ts as /devices/soc0/soc/2100000.aips-bus/21a0000.i2c/i2c-0/0-0048/input/input0
        [    2.651584] snvs_rtc 20cc000.snvs:snvs-rtc-lp: registered as rtc0
        [    2.658056] i2c /dev entries driver
        [    2.670660] imx2-wdt 20bc000.wdog: timeout 60 sec (nowayout=0)
        [    2.677260] Bluetooth: HCI UART driver ver 2.3
        [    2.681731] Bluetooth: HCI UART protocol H4 registered
        [    2.687381] Bluetooth: HCI UART protocol LL registered
        [    2.693884] sdhci: Secure Digital Host Controller Interface driver
        [    2.700145] sdhci: Copyright(c) Pierre Ossman
        [    2.704521] sdhci-pltfm: SDHCI platform and OF driver helper
        [    2.711506] sdhci-esdhc-imx 2190000.usdhc: Got CD GPIO
        [    2.753031] mmc0: SDHCI controller on 2190000.usdhc [2190000.usdhc] using ADMA
        [    2.767363] caam 2100000.caam: Entropy delay = 3200
        [    2.772382] caam 2100000.caam: Instantiated RNG4 SH0
        [    2.833144] caam 2100000.caam: Instantiated RNG4 SH1
        [    2.838177] caam 2100000.caam: device ID = 0x0a16010000000000 (Era 4)
        [    2.844640] caam 2100000.caam: job rings = 2, qi = 0
        [    2.882755] mmc0: host does not support reading read-only switch, assuming write-enable
        [    2.892941] caam algorithms registered in /proc/crypto
        [    2.901530] mmc0: new high speed SDHC card at address aaaa
        [    2.908475] caam_jr 2101000.jr0: registering rng-caam
        [    2.911092] mmcblk0: mmc0:aaaa SS08G 7.40 GiB
        [    2.915632] usbcore: registered new interface driver usbhid
        [    2.923794] usbhid: USB HID core driver
        [    2.927955]  mmcblk0: p1 p2
        [    2.933263] imx-media: subdev ipu1_vdic bound
        [    2.937996] imx-media: subdev ipu2_vdic bound
        [    2.942764] imx-media: subdev ipu1_ic_prp bound
        [    2.948688] ipu1_ic_prpenc: Registered ipu1_ic_prpenc capture as /dev/video0
        [    2.956126] imx-media: subdev ipu1_ic_prpenc bound
        [    2.961451] ipu1_ic_prpvf: Registered ipu1_ic_prpvf capture as /dev/video1
        [    2.968525] imx-media: subdev ipu1_ic_prpvf bound
        [    2.973390] imx-media: subdev ipu2_ic_prp bound
        [    2.978481] ipu2_ic_prpenc: Registered ipu2_ic_prpenc capture as /dev/video2
        [    2.985679] imx-media: subdev ipu2_ic_prpenc bound
        [    2.990989] ipu2_ic_prpvf: Registered ipu2_ic_prpvf capture as /dev/video3
        [    2.997993] imx-media: subdev ipu2_ic_prpvf bound
        [    3.004315] ipu1_csi0: Registered ipu1_csi0 capture as /dev/video4
        [    3.005488] usb 2-1: new high-speed USB device number 2 using ci_hdrc
        [    3.010585] imx-media: subdev ipu1_csi0 bound
        [    3.021738] imx-ipuv3 2400000.ipu: driver could not parse port@1/endpoint@0 (-22)
        [    3.029581] imx-ipuv3-csi: probe of imx-ipuv3-csi.1 failed with error -22
        [    3.036639] imx-ipuv3 2800000.ipu: driver could not parse port@0/endpoint@0 (-22)
        [    3.044202] imx-ipuv3-csi: probe of imx-ipuv3-csi.4 failed with error -22
        [    3.051842] ipu2_csi1: Registered ipu2_csi1 capture as /dev/video5
        [    3.058116] imx-media: subdev ipu2_csi1 bound
        [    3.070591] sgtl5000 2-000a: Linked as a consumer to regulator.7
        [    3.077157] sgtl5000 2-000a: Dropping the link to regulator.7
        [    3.083902] sgtl5000 2-000a: Linked as a consumer to regulator.8
        [    3.090251] sgtl5000 2-000a: Linked as a consumer to regulator.9
        [    3.097285] sgtl5000 2-000a: Linked as a consumer to regulator.7
        [    3.104665] sgtl5000 2-000a: Error reading chip id -6
        [    3.110044] sgtl5000 2-000a: Dropping the link to regulator.8
        [    3.116653] sgtl5000 2-000a: Dropping the link to regulator.9
        [    3.122627] sgtl5000 2-000a: Dropping the link to regulator.7
        [    3.134079] fsl-ssi-dai 2028000.ssi: No cache defaults, reading back from HW
        [    3.147485] NET: Registered protocol family 10
        [    3.155610] Segment Routing with IPv6
        [    3.159514] sit: IPv6, IPv4 and MPLS over IPv4 tunneling driver
        [    3.167454] NET: Registered protocol family 17
        [    3.171951] can: controller area network core (rev 20170425 abi 9)
        [    3.178404] NET: Registered protocol family 29
        [    3.182941] can: raw protocol (rev 20170425)
        [    3.187399] can: broadcast manager protocol (rev 20170425 t)
        [    3.193101] can: netlink gateway (rev 20170425) max_hops=1
        [    3.199045] Key type dns_resolver registered
        [    3.205418] cpu cpu0: Linked as a consumer to regulator.4
        [    3.211047] cpu cpu0: Linked as a consumer to regulator.5
        [    3.216726] cpu cpu0: Linked as a consumer to regulator.6
        [    3.227044] usb 2-1: New USB device found, idVendor=0424, idProduct=2514, bcdDevice= b.b3
        [    3.227450] Registering SWP/SWPB emulation handler
        [    3.235528] usb 2-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
        [    3.241787] Loading compiled-in X.509 certificates
        [    3.249392] hub 2-1:1.0: USB hub found
        [    3.256644] hub 2-1:1.0: 4 ports detected
        [    3.328359] imx_thermal tempmon: Industrial CPU temperature grade - max:105C critical:100C passive:95C
        [    3.343738] snvs_rtc 20cc000.snvs:snvs-rtc-lp: setting system clock to 1970-01-01T00:00:00 UTC (0)
        [    3.353184] cfg80211: Loading compiled-in X.509 certificates for regulatory database
        [    3.366857] cfg80211: Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
        [    3.374891] platform regulatory.0: Direct firmware load for regulatory.db failed with error -2
        [    3.375477] ALSA device list:
        [    3.383687] platform regulatory.0: Falling back to syfs fallback for: regulatory.db
        [    3.386727]   No soundcards found.
        [    3.428373] EXT4-fs (mmcblk0p2): warning: mounting unchecked fs, running e2fsck is recommended
        [    3.445686] EXT4-fs (mmcblk0p2): mounted filesystem without journal. Opts: (null)
        [    3.453314] VFS: Mounted root (ext4 filesystem) on device 179:2.
        [    3.472516] devtmpfs: mounted
        [    3.479006] Freeing unused kernel memory: 1024K
        [    3.506235] Run /sbin/init as init process
        mount: mounting proc on /proc failed: No such file or directory
        mount: can't read '/proc/mounts': No such file or directory
        mount: mounting proc on /proc failed: No such file or directory
        mount: mounting tmpfs on /tmp failed: No such file or directory
        mount: mounting sysfs on /sys failed: No such file or directory
        Starting logging: OK
        Jan  1 00:00:03 buildroot syslog.info syslogd started: BusyBox v1.27.2
        Jan  1 00:00:03 buildroot kern.notice kernel: klogd started: BusyBox v1.27.2 (2017-10-05 13:33:52 IST)
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Booting Linux on physical CPU 0x0
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000] Linux version 5.0.0-rc3-00055-gcfeb525f403f-dirty (shyam@debian) (gcc ver9
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] CPU: ARMv7 Processor [412fc09a] revision 10 (ARMv7), cr=10c5387d
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] OF: fdt: Machine model: Engicam i.CoreM6 Quad/Dual Starter Kit
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Memory policy: Data cache writealloc
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] cma: Reserved 64 MiB at 0x2c000000
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000] On node 0 totalpages: 131072
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000]   Normal zone: 1024 pages used for memmap
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000]   Normal zone: 0 pages reserved
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000]   Normal zone: 131072 pages, LIFO batch:31
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000] random: get_random_bytes called from start_kernel+0x8c/0x478 with crng_in0
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] percpu: Embedded 18 pages/cpu @(ptrval) s42088 r8192 d23448 u73728
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000] pcpu-alloc: s42088 r8192 d23448 u73728 alloc=18*4096
        Jan  1 00:00:03 buildroot kern.debug kernel: [    0.000000] pcpu-alloc: [0] 0 [0] 1 [0] 2 [0] 3
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 130048
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/mmcblk0p2 rootwait w
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Inode-cache hash table entries: 32768 (order: 5, 131072 bytes)
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Memory: 427728K/524288K available (11264K kernel code, 931K rwdata, 3928K r)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000] Virtual kernel memory layout:
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     vmalloc : 0xe0800000 - 0xff800000   ( 496 MB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     lowmem  : 0xc0000000 - 0xe0000000   ( 512 MB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     pkmap   : 0xbfe00000 - 0xc0000000   (   2 MB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]     modules : 0xbf000000 - 0xbfe00000   (  14 MB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]       .text : 0x(ptrval) - 0x(ptrval)   (12256 kB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]       .init : 0x(ptrval) - 0x(ptrval)   (1024 kB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]       .data : 0x(ptrval) - 0x(ptrval)   ( 932 kB)
        Jan  1 00:00:03 buildroot kern.notice kernel: [    0.000000]        .bss : 0x(ptrval) - 0x(ptrval)   (7589 kB)
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] Running RCU self tests
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] rcu: Hierarchical RCU implementation.
        Jan  1 00:00:03 buildroot kern.info kernel: [    0.000000] rcu:         RCU event tracing is enabled.
        Jan  1 00:00:03 buildroot kern.info Jan  1 00:00:03 buildroot kern.wJan  1 00:00:03 buildroot kern.iJan  1 00:00:03 buildroot kern.iJa)
        done.
        Jan  1 00:00:04 buildroot kern.notice kernel: [    4.200491] random: dd: uninitialized urandom read (512 bytes read)
        Starting network: OK
        Jan  1 00:00:04 buildroot daemon.info : starting pid 261, tty '/dev/ttymxc3': '/sbin/getty -L  ttymxc3 0 vt100 '
         
        Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo Starter Kit
        buildroot login:
