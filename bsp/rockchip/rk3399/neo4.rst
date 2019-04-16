NanoPI NEO4
===========

This tutorial will show the details of NanoPI NEO4 board mainline support.

Hardware details and wiki `NanoPI NEO4 <http://wiki.friendlyarm.com/wiki/index.php/NanoPi_NEO4>`_

Hardware Access

.. image:: /images/neo4.jpg

BSP Build

ATF
::
        $ git clone https://github.com/ARM-software/arm-trusted-firmware.git
        $ cd /path/to/arm-trusted-firmware
        $ make realclean
        $ make CROSS_COMPILE=aarch64-linux-gnu- PLAT=rk3399
        $ cp /path/to/arm-trusted-firmware/build/rk3399/release/bl31/bl31.elf /path/to/u-boot

U-Boot
::     
        $ git clone https://github.com/amarula/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b rockdev origin/rockdev
        $ make nanopi-neo4-rk3399_defconfig
        $ make
        $ make u-boot.itb

Rockchip miniloader
::

        $ git clone https://github.com/rockchip-linux/rkbin.git
        $ cd /path/to/rkbin
        $ ./tools/trust_merger RKTRUST/RK3399TRUST.ini
        $ ./tools/loaderimage --pack --uboot /path/to/u-boot/u-boot-dtb.bin uboot.img

Linux

::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make Image dtbs -j 4

Buildroot


SD Boot

Create Single partition and Insert the SD on host

::

        $ cd /path/to/u-boot
        $ ./tools/mkimage  -n rk3399 -T rksd -d /path/to/rkbin/bin/rk33/rk3399_ddr_800MHz_v1.20.bin idbloader.img
        $ cat /path/to/rkbin/bin/rk33/rk3399_miniloader_v1.19.bin >> idbloader.img

        $ sudo dd if=idbloader.img of=/dev/sdc seek=64
        $ sudo dd if=trust.img of=/dev/sdc seek=24576
        $ sudo dd if=uboot.img of=/dev/sdc seek=16384
        $ sync

Put this SD (or micro-SD) card into your board and reset it. You should see
something like:

::

        DDR Version 1.20 20190314
        In
        Channel 0: DDR3, 933MHz
        Bus Width=32 Col=10 Bank=8 Row=15 CS=1 Die Bus-Width=16 Size=1024MB
        no stride
        ch 0 ddrconfig = 0x101, ddrsize = 0x20
        pmugrf_os_reg[2] = 0x10006281, stride = 0x17
        OUT
        Boot1: 2019-03-14, version: 1.19
        CPUId = 0x0
        ChipType = 0x10, 239
        mmc: ERROR: SDHCI ERR:cmd:0x102,stat:0x18000
        mmc: ERROR: Card did not respond to voltage select!
        emmc reinit
        mmc: ERROR: SDHCI ERR:cmd:0x102,stat:0x18000
        mmc: ERROR: Card did not respond to voltage select!
        emmc reinit
        mmc: ERROR: SDHCI ERR:cmd:0x102,stat:0x18000
        mmc: ERROR: Card did not respond to voltage select!
        SdmmcInit=2 1
        mmc0:cmd5,20
        SdmmcInit=0 0
        BootCapSize=0
        UserCapSize=60543MB
        FwPartOffset=2000 , 0
        StorageInit ok = 45266
        SecureMode = 0
        SecureInit read PBA: 0x4
        SecureInit read PBA: 0x404
        SecureInit read PBA: 0x804
        SecureInit read PBA: 0xc04
        SecureInit read PBA: 0x1004
        SecureInit read PBA: 0x1404
        SecureInit read PBA: 0x1804
        SecureInit read PBA: 0x1c04
        SecureInit ret = 0, SecureMode = 0
        atags_set_bootdev: ret:(0)
        GPT 0x3380ec0 signature is wrong
        recovery gpt...
        GPT 0x3380ec0 signature is wrong
        recovery gpt fail!
        LoadTrust Addr:0x4000
        No find bl30.bin
        Load uboot, ReadLba = 2000
        hdr 0000000003380880 + 0x0:0x88,0x41,0x3e,0x97,0xe6,0x61,0x54,0x23,0xe9,0x5a,0xd1,0x2b,0xdc,0x2f,0xf9,0x35,

        Load OK, addr=0x200000, size=0x9c9c0
        RunBL31 0x10000
        NOTICE:  BL31: v1.3(debug):370ab80
        NOTICE:  BL31: Built : 09:23:41, Mar  4 2019
        NOTICE:  BL31: Rockchip release version: v1.1
        INFO:    GICv3 with legacy support detected. ARM GICV3 driver initialized in EL3
        INFO:    Using opteed sec cpu_context!
        INFO:    boot cpu mask: 0
        INFO:    plat_rockchip_pmu_init(1181): pd status 3e
        INFO:    BL31: Initializing runtime services
        INFO:    BL31: Initializing BL32
        INF [0x0] TEE-CORE:init_primary_helper:337: Initializing (1.1.0-195-g8f090d20 #6 Fri Dec  7 06:11:20 UTC 2018 aarch64)

        INF [0x0] TEE-CORE:init_primary_helper:338: Release version: 1.2

        INF [0x0] TEE-CORE:init_teecore:83: teecore inits done
        INFO:    BL31: Preparing for EL3 exit to normal world
        INFO:    Entry point address = 0x200000
        INFO:    SPSR = 0x3c9


        U-Boot 2019.04-rc4-00136-gfd121f9641-dirty (Apr 16 2019 - 14:02:47 +0530)

        Model: FriendlyARM NanoPi NEO4
        DRAM:  1022 MiB
        MMC:   dwmmc@fe310000: 2, dwmmc@fe320000: 1, sdhci@fe330000: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial@ff1a0000
        Out:   serial@ff1a0000
        Err:   serial@ff1a0000
        Model: FriendlyARM NanoPi NEO4
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
        160 bytes read in 5 ms (31.3 KiB/s)
        1:      linux-4.17.0-rc3
        Retrieving file: /boot/Image
        20361728 bytes read in 1308 ms (14.8 MiB/s)
        append: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk0p1 rootwait
        Retrieving file: /boot/rk3399-nanopi-neo4.dtb
        54786 bytes read in 11 ms (4.7 MiB/s)
        ## Flattened Device Tree blob at 01f00000
           Booting using the fdt blob at 0x1f00000
           Loading Device Tree to 000000003df1c000, end 000000003df2c601 ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
        [    0.000000] Linux version 5.1.0-rc1 (jagan@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #1 SMP PREEMPT Mon Apr 15 22:40:42
         IST 2019
        [    0.000000] Machine model: FriendlyARM NanoPi NEO4
        [    0.000000] earlycon: uart8250 at MMIO32 0x00000000ff1a0000 (options '')
        [    0.000000] printk: bootconsole [uart8250] enabled
        [    0.000000] efi: Getting EFI parameters from FDT:
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 32 MiB at 0x000000003e000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000200000-0x000000003fffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0x3dda2840-0x3dda3fff]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA32    [mem 0x0000000000200000-0x000000003fffffff]
        [    0.000000]   Normal   empty
        [    0.000000] Movable zone start for each node
        [    0.000000] Early memory node ranges
        [    0.000000]   node   0: [mem 0x0000000000200000-0x000000003fffffff]
        [    0.000000] Initmem setup node 0 [mem 0x0000000000200000-0x000000003fffffff]
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv1.0 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: Trusted OS migration not required
        [    0.000000] psci: SMC Calling Convention v1.0
        [    0.000000] random: get_random_bytes called from start_kernel+0xac/0x46c with crng_init=0
        [    0.000000] percpu: Embedded 23 pages/cpu @(____ptrval____) s56664 r8192 d29352 u94208
        [    0.000000] Detected VIPT I-cache on CPU0
        [    0.000000] CPU features: detected: ARM erratum 845719
        [    0.000000] CPU features: detected: GIC system register CPU interface
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 257544
        [    0.000000] Policy zone: DMA32
        [    0.000000] Kernel command line: earlycon=uart8250,mmio32,0xff1a0000 root=/dev/mmcblk0p1 rootwait

