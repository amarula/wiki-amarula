Optee OS
################

Optee_os Configs
****************

::

        $ git clone https://github.com/OP-TEE/optee_os.git
        $ cd optee_os
        $ cat > optee_imx6q-icore.patch
        diff --git a/core/arch/arm/plat-imx/conf.mk b/core/arch/arm/plat-imx/conf.mk
        index 3e6d61f371a9..23603a8ddbcf 100644
        --- a/core/arch/arm/plat-imx/conf.mk
        +++ b/core/arch/arm/plat-imx/conf.mk
        @@ -92,9 +92,9 @@ CFG_NS_ENTRY_ADDR ?= 0x12000000
         endif
          
         ifneq (,$(filter $(PLATFORM_FLAVOR),mx6qsabrelite mx6dlsabrelite))
        -CFG_DDR_SIZE ?= 0x40000000
        -CFG_NS_ENTRY_ADDR ?= 0x12000000
        -CFG_UART_BASE ?= UART2_BASE
        +CFG_DDR_SIZE ?= 0x1E200000
        +CFG_NS_ENTRY_ADDR ?= 0x10800000
        +CFG_UART_BASE ?= UART4_BASE
         endif
          
         ifneq (,$(filter $(PLATFORM_FLAVOR),mx6sxsabreauto))
         
        $ git apply -v  optee_imx6q-icore.patch
        $ export CROSS_COMPILE=arm-linux-gnueabi
        $ export PATH=~/gcc-linaro-6.3.1-2017.02-i686_arm-linux-gnueabi/bin:$PATH
        $ make PLATFORM=imx-mx6qsabrelite ARCH=arm CFG_BUILT_IN_ARGS=y CFG_PAGEABLE_ADDR=0 CFG_NS_ENTRY_ADDR=0x12000000 CFG_DT_ADDR=0x18000000 CFG_DT=y CFG_PSCI_ARM32=y DEBUG=y CFG_TEE_CORE_LOG_LEVEL=4 CFG_BOOT_SYNC_CPU=n CFG_BOOT_SECONDARY_REQUEST=y

U-Boot configs for optee
************************

::

        $ cd /path/to/u-boot
        $ cat > uboot-optee-imx6q-icore.patch
        diff --git a/board/engicam/common/board.c b/board/engicam/common/board.c
        index 5dccb17cb271..1272c845f943 100644
        --- a/board/engicam/common/board.c
        +++ b/board/engicam/common/board.c
        @@ -12,7 +12,7 @@
         #include "board.h"
         
         DECLARE_GLOBAL_DATA_PTR;
        -
        +#define CONFIG_TEE_RAM_SIZE 0x01e00000
         #ifdef CONFIG_ENV_IS_IN_MMC
         static void mmc_late_init(void)
         {
        @@ -109,7 +109,7 @@ int board_init(void)
         
         int dram_init(void)
         {
        - gd->ram_size = imx_ddr_size();
        + gd->ram_size = imx_ddr_size() - CONFIG_TEE_RAM_SIZE;
         
         return 0;
         }
        diff --git a/configs/imx6qdl_icore_mmc_defconfig b/configs/imx6qdl_icore_mmc_defconfig
        index cb81a7a68290..e0b5172901e2 100644
        --- a/configs/imx6qdl_icore_mmc_defconfig
        +++ b/configs/imx6qdl_icore_mmc_defconfig
        @@ -12,6 +12,10 @@ CONFIG_DEBUG_UART_BASE=0x021f0000
         CONFIG_DEBUG_UART_CLOCK=24000000
         CONFIG_SPL_LIBDISK_SUPPORT=y
         # CONFIG_CMD_BMODE is not set
        +
        +CONFIG_TEE_RAM_SIZE=0x01e00000
        +CONFIG_CMD_BOOTZ=y
        +
         CONFIG_DEBUG_UART=y
         CONFIG_NR_DRAM_BANKS=1
         CONFIG_FIT=y

        $ git apply -v uboot-optee-imx6q-icore.patch
        $ build imx6qdl for u-boot

        # Get -a and -e value from /path/to/optee_os/out/arm-plat-imx/conf.mk
        # CFG_TZDRAM_SIZE=0x01e00000
        # This will give -e value CFG_TZDRAM_START=(0x10000000 - 0x02000000 + 0x1E200000)
        # For -a value we need to substract 0x1C(optee header size) from -e value
        $ ./tools/mkimage -A arm -O linux -C none -a 0x2C1FFFE4 -e 0x2C200000 -d /path to/optee_os/out/arm-plat-imx/core/tee.bin uTee
        $  sudo cp -vf uTee /media/cdrom/

Linux steps
***********
Before build disable CAAM and Outer Cache

Cryptographic API  --->  [ ]   Hardware crypto devices

System Type  --->  [ ] Enable the L2x0 outer cache controller

::

        $ ARCH=arm make menuconfig
        $ ARCH=arm make LOADADDR=0x10008000 uImage dtbs -j4
        $ sudo cp -vf arch/arm/boot/zImage /media/cdrom/
        $ sudo cp -vf arch/arm/boot/dts/imx6q-icore.dtb /media/cdrom/
        $ sync
        $ sudo umount /media/cdrom

Final Steps
***********

Insert sd card and Turn on the board, and get into u-boot command prompt by pressing enter.

::

        Environment size: 1615/131068 bytes
        icorem6qdl> ext4load mmc ${mmcdev}:${mmcpart} ${loadaddr} zImage
        8229304 bytes read in 397 ms (19.8 MiB/s)
        icorem6qdl> ext4load mmc ${mmcdev}:${mmcpart} ${fdt_addr} ${fdt_file}
        37450 bytes read in 10 ms (3.6 MiB/s)
        icorem6qdl> #ext4load mmc ${mmcdev}:${mmcpart} 0x20000000 uTee;      
        icorem6qdl> setenv bootargs console=${console},${baudrate} root=/dev/mmcblk0p1 rootwait rw earlycon
        icorem6qdl> ext4ls mmc 0:1
        <DIR>       4096 .
        <DIR>       4096 ..
        <DIR>      16384 lost+found
        <DIR>       4096 bin
        <DIR>       4096 dev
        <DIR>       4096 etc
        <DIR>       4096 lib
        <SYM>          3 lib32
        <SYM>         11 linuxrc
        <DIR>       4096 media
        <DIR>       4096 mnt
        <DIR>       4096 opt
        <DIR>       4096 proc
        <DIR>       4096 root
        <DIR>       4096 run
        <DIR>       4096 sbin
        <DIR>       4096 sys
        <DIR>       4096 tmp
        <DIR>       4096 usr
        <DIR>       4096 var
                 8229368 uImage
                 8229304 zImage
                   37450 imx6q-icore.dtb
                  266980 uTee
        icorem6qdl> ext4load mmc ${mmcdev}:${mmcpart} 0x20000000 uTee;                                     
        266980 bytes read in 21 ms (12.1 MiB/s)
        icorem6qdl>  bootm 0x20000000 - ${fdt_addr};
        ## Booting kernel from Legacy Image at 20000000 ...
           Image Name:   
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    266916 Bytes = 260.7 KiB
           Load Address: 2c1fffe4
           Entry Point:  2c200000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c249

        Starting kernel ...

        D/TC:0 0 add_phys_mem:539 TEE_SHMEM_START type NSEC_SHM 0x2e000000 size 0x00200000
        D/TC:0 0 add_phys_mem:539 TA_RAM_START type TA_RAM 0x2c300000 size 0x01d00000
        D/TC:0 0 add_phys_mem:539 VCORE_UNPG_RW_PA type TEE_RAM_RW 0x2c241000 size 0x000bf000
        D/TC:0 0 add_phys_mem:539 VCORE_UNPG_RX_PA type TEE_RAM_RX 0x2c200000 size 0x00041000
        D/TC:0 0 add_phys_mem:539 ROUNDDOWN(PL310_BASE, CORE_MMU_DEVICE_SIZE) type IO_SEC 0x00a00000 size 0x00100000
        D/TC:0 0 add_phys_mem:539 ROUNDDOWN(IRAM_BASE, CORE_MMU_DEVICE_SIZE) type TEE_COHERENT 0x00900000 size 0x00100000
        D/TC:0 0 add_phys_mem:539 AIPS3_BASE type IO_SEC 0x02200000 size 0x00100000
        D/TC:0 0 add_phys_mem:539 AIPS2_BASE type IO_SEC 0x02100000 size 0x00100000
        D/TC:0 0 add_phys_mem:539 AIPS1_BASE type IO_SEC 0x02000000 size 0x00100000
        D/TC:0 0 add_phys_mem:539 ANATOP_BASE type IO_SEC 0x02000000 size 0x00200000
        D/TC:0 0 add_phys_mem:552 Physical mem map overlaps 0x2000000
        D/TC:0 0 add_phys_mem:539 GIC_BASE type IO_SEC 0x00a00000 size 0x00100000
        D/TC:0 0 add_phys_mem:552 Physical mem map overlaps 0xa00000
        D/TC:0 0 add_phys_mem:539 CONSOLE_UART_BASE type IO_NSEC 0x02100000 size 0x00200000
        D/TC:0 0 add_phys_mem:539 PL310_BASE type IO_SEC 0x00a00000 size 0x00200000
        D/TC:0 0 add_phys_mem:552 Physical mem map overlaps 0xa00000
        D/TC:0 0 add_phys_mem:539 SRC_BASE type IO_SEC 0x02000000 size 0x00200000
        D/TC:0 0 add_phys_mem:552 Physical mem map overlaps 0x2000000
        D/TC:0 0 verify_special_mem_areas:477 No NSEC DDR memory area defined
        D/TC:0 0 add_va_space:578 type RES_VASPACE size 0x00a00000
        D/TC:0 0 add_va_space:578 type SHM_VASPACE size 0x02000000
        D/TC:0 0 dump_mmap_table:711 type TEE_RAM_RX   va 0x2c200000..0x2c240fff pa 0x2c200000..0x2c240fff size 0x00041000 (small)
        D/TC:0 0 dump_mmap_table:711 type TEE_RAM_RW   va 0x2c241000..0x2c2fffff pa 0x2c241000..0x2c2fffff size 0x000bf000 (small)
        D/TC:0 0 dump_mmap_table:711 type SHM_VASPACE  va 0x2c300000..0x2e2fffff pa 0x00000000..0x01ffffff size 0x02000000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type IO_SEC       va 0x2e300000..0x2e3fffff pa 0x02200000..0x022fffff size 0x00100000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type RES_VASPACE  va 0x2e400000..0x2edfffff pa 0x00000000..0x009fffff size 0x00a00000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type TEE_COHERENT va 0x2ee00000..0x2eefffff pa 0x00900000..0x009fffff size 0x00100000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type TA_RAM       va 0x2ef00000..0x30bfffff pa 0x2c300000..0x2dffffff size 0x01d00000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type NSEC_SHM     va 0x30c00000..0x30dfffff pa 0x2e000000..0x2e1fffff size 0x00200000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type IO_NSEC      va 0x30e00000..0x30ffffff pa 0x02100000..0x022fffff size 0x00200000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type IO_SEC       va 0x31000000..0x311fffff pa 0x00a00000..0x00bfffff size 0x00200000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type IO_SEC       va 0x31200000..0x313fffff pa 0x02000000..0x021fffff size 0x00200000 (pgdir)
        D/TC:0 0 dump_mmap_table:711 type IO_SEC       va 0x31400000..0x314fffff pa 0x02100000..0x021fffff size 0x00100000 (pgdir)
        D/TC:0 0 core_mmu_alloc_l2:238 L2 table used: 1/4
        I/TC: 
        D/TC:0 0 init_canaries:164 #Stack canaries for stack_tmp[0] with top at 0x2c2709b8
        D/TC:0 0 init_canaries:164 watch *0x2c2709bc
        D/TC:0 0 init_canaries:164 #Stack canaries for stack_tmp[1] with top at 0x2c2710f8
        D/TC:0 0 init_canaries:164 watch *0x2c2710fc
        D/TC:0 0 init_canaries:164 #Stack canaries for stack_tmp[2] with top at 0x2c271838
        D/TC:0 0 init_canaries:164 watch *0x2c27183c
        D/TC:0 0 init_canaries:164 #Stack canaries for stack_tmp[3] with top at 0x2c271f78
        D/TC:0 0 init_canaries:164 watch *0x2c271f7c
        D/TC:0 0 init_canaries:165 #Stack canaries for stack_abt[0] with top at 0x2c26a938
        D/TC:0 0 init_canaries:165 watch *0x2c26a93c
        D/TC:0 0 init_canaries:165 #Stack canaries for stack_abt[1] with top at 0x2c26b178
        D/TC:0 0 init_canaries:165 watch *0x2c26b17c
        D/TC:0 0 init_canaries:165 #Stack canaries for stack_abt[2] with top at 0x2c26b9b8
        D/TC:0 0 init_canaries:165 watch *0x2c26b9bc
        D/TC:0 0 init_canaries:165 #Stack canaries for stack_abt[3] with top at 0x2c26c1f8
        D/TC:0 0 init_canaries:165 watch *0x2c26c1fc
        D/TC:0 0 init_canaries:167 #Stack canaries for stack_thread[0] with top at 0x2c26e238
        D/TC:0 0 init_canaries:167 watch *0x2c26e23c
        D/TC:0 0 init_canaries:167 #Stack canaries for stack_thread[1] with top at 0x2c270278
        D/TC:0 0 init_canaries:167 watch *0x2c27027c
        I/TC: OP-TEE version: 3.3.0-dev #19 Wed Oct 24 12:34:53 UTC 2018 arm
        D/TC:0 0 tee_ta_register_ta_store:534 Registering TA store: 'REE' (priority 10)
        D/TC:0 0 tee_ta_register_ta_store:534 Registering TA store: 'Secure Storage TA' (priority 9)
        D/TC:0 0 mobj_mapped_shm_init:702 Shared memory address range: 2c300000, 2e300000
        E/TC:0 0 plat_rng_init:354 Warning: seeding RNG with zeroes
        D/TC:0 0 imx_wdog_base:125 path: /soc/aips-bus@2000000/wdog@20bc000
        I/TC: Initialized
        D/TC:0 0 init_primary_helper:928 Primary CPU switching to normal world boot
        [    0.000000] Booting Linux on physical CPU 0x0
        [    0.000000] Linux version 4.19.0-00618-gbad5e39a548d (shyam@debian) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.08
        [    0.000000] CPU: ARMv7 Processor [412fc09a] revision 10 (ARMv7), cr=10c5787d
        [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        [    0.000000] OF: fdt: Machine model: Engicam i.CoreM6 Quad/Dual Starter Kit
        [    0.000000] earlycon: ec_imx21 at MMIO 0x021f0000 (options '')
        [    0.000000] bootconsole [ec_imx21] enabled
        [    0.000000] Memory policy: Data cache writealloc
        [    0.000000] OF: fdt: Reserved memory: unsupported node format, ignoring
        [    0.000000] cma: Reserved 64 MiB at 0x2a000000
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv1.0 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: MIGRATE_INFO_TYPE not supported.
        [    0.000000] psci: SMC Calling Convention v1.0
        [    0.000000] random: get_random_bytes called from start_kernel+0x90/0x490 with crng_init=0
        [    0.000000] percpu: Embedded 18 pages/cpu @(ptrval) s41832 r8192 d23704 u73728
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 122428
        [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/mmcblk0p1 rootwait rw earlycon
        [    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)
        [    0.000000] Inode-cache hash table entries: 32768 (order: 5, 131072 bytes)
        [    0.000000] Memory: 398056K/493568K available (11264K kernel code, 843K rwdata, 3620K rodata, 1024K init, 7650K bss, 2)
        [    0.000000] Virtual kernel memory layout:
        [    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
        [    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
        [    0.000000]     vmalloc : 0xde800000 - 0xff800000   ( 528 MB)
        [    0.000000]     lowmem  : 0xc0000000 - 0xde200000   ( 482 MB)
        [    0.000000]     pkmap   : 0xbfe00000 - 0xc0000000   (   2 MB)
        [    0.000000]     modules : 0xbf000000 - 0xbfe00000   (  14 MB)
        [    0.000000]       .text : 0x(ptrval) - 0x(ptrval)   (12256 kB)
        [    0.000000]       .init : 0x(ptrval) - 0x(ptrval)   (1024 kB)
        [    0.000000]       .data : 0x(ptrval) - 0x(ptrval)   ( 844 kB)
        [    0.000000]        .bss : 0x(ptrval) - 0x(ptrval)   (7651 kB)
        [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
        [    0.000000] Running RCU self tests
        [    0.000000] rcu: Hierarchical RCU implementation.
        [    0.000000] rcu:     RCU event tracing is enabled.
        [    0.000000] rcu:     RCU lockdep checking is enabled.
        [    0.000000] NR_IRQS: 16, nr_irqs: 16, preallocated irqs: 16
        [    0.000000] Switching to timer-based delay loop, resolution 333ns
        [    0.000011] sched_clock: 32 bits at 3000kHz, resolution 333ns, wraps every 715827882841ns
        [    0.008185] clocksource: mxc_timer1: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 637086815595 ns
        [    0.019725] Console: colour dummy device 80x30
        [    0.022275] Lock dependency validator: Copyright (c) 2006 Red Hat, Inc., Ingo Molnar
        [    0.030092] ... MAX_LOCKDEP_SUBCLASSES:  8
        [    0.034102] ... MAX_LOCK_DEPTH:          48
        [    0.038333] ... MAX_LOCKDEP_KEYS:        8191
        [    0.042626] ... CLASSHASH_SIZE:          4096
        [    0.047031] ... MAX_LOCKDEP_ENTRIES:     32768
        [    0.051413] ... MAX_LOCKDEP_CHAINS:      65536
        [    0.055849] ... CHAINHASH_SIZE:          32768
        [    0.060339]  memory used by lock dependency info: 4655 kB
        [    0.065681]  per task-struct memory footprint: 1536 bytes
        [    0.071201] Calibrating delay loop (skipped), value calculated using timer frequency.. 6.00 BogoMIPS (lpj=30000)
        [    0.081322] pid_max: default: 32768 minimum: 301
        [    0.086485] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
        [    0.092499] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
        [    0.102108] CPU: Testing write buffer coherency: ok
        [    0.104402] CPU0: Spectre v2: using BPIALL workaround
        [    0.111206] CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
        [    0.118881] Setting up static identity map for 0x10100000 - 0x10100078
        [    0.123446] rcu: Hierarchical SRCU implementation.
        [    0.131187] smp: Bringing up secondary CPUs ...
        D/TC:1   init_secondary_helper:952 Secondary CPU Switching to normal world boot
        [    0.144211] CPU1: thread -1, cpu 1, socket 0, mpidr 80000001
        [    0.144228] CPU1: Spectre v2: using BPIALL workaround
        D/TC:2   init_secondary_helper:952 Secondary CPU Switching to normal world boot
        [    0.163626] CPU2: thread -1, cpu 2, socket 0, mpidr 80000002
        [    0.163643] CPU2: Spectre v2: using BPIALL workaround
        D/TC:3   init_secondary_helper:952 Secondary CPU Switching to normal world boot
        [    0.182665] CPU3: thread -1, cpu 3, socket 0, mpidr 80000003
        [    0.182681] CPU3: Spectre v2: using BPIALL workaround
        [    0.191109] smp: Brought up 1 node, 4 CPUs
        [    0.194645] SMP: Total of 4 processors activated (24.00 BogoMIPS).
        [    0.200955] CPU: All CPU(s) started in SVC mode.
        [    0.208895] devtmpfs: initialized
        [    0.245968] VFP support v0.3: implementor 41 architecture 3 part 30 variant 9 rev 4
        [    0.254653] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
        [    0.261801] futex hash table entries: 1024 (order: 4, 65536 bytes)
        [    0.275909] pinctrl core: initialized pinctrl subsystem
        [    0.283581] NET: Registered protocol family 16
        [    0.324561] DMA: preallocated 256 KiB pool for atomic coherent allocations
        [    0.333324] cpuidle: using governor menu
        [    0.334723] CPU identified as i.MX6Q, silicon rev 1.2
        [    0.369464] vdd1p1: supplied by regulator-dummy
        [    0.373484] vdd3p0: supplied by regulator-dummy
        [    0.377850] vdd2p5: supplied by regulator-dummy
        [    0.382263] vddarm: supplied by regulator-dummy
        [    0.387025] vddpu: supplied by regulator-dummy
        [    0.391253] vddsoc: supplied by regulator-dummy
        [    0.430569] No ATAGs?
        [    0.431334] hw-breakpoint: found 5 (+1 reserved) breakpoint and 1 watchpoint registers.
        [    0.438942] hw-breakpoint: maximum watchpoint size is 4 bytes.
        [    0.449625] imx6q-pinctrl 20e0000.iomuxc: initialized IMX pinctrl driver
        [    0.554662] mxs-dma 110000.dma-apbh: initialized
        [    0.567720] vgaarb: loaded
        [    0.569248] SCSI subsystem initialized
        [    0.573328] usbcore: registered new interface driver usbfs
        [    0.577241] usbcore: registered new interface driver hub
        [    0.582610] usbcore: registered new device driver usb
        [    0.592020] i2c i2c-0: IMX I2C adapter registered
        [    0.593940] i2c i2c-0: can't use DMA, using PIO instead.
        [    0.601363] i2c i2c-1: IMX I2C adapter registered
        [    0.603938] i2c i2c-1: can't use DMA, using PIO instead.
        [    0.611480] i2c i2c-2: IMX I2C adapter registered
        [    0.613947] i2c i2c-2: can't use DMA, using PIO instead.
        [    0.619840] media: Linux media interface: v0.10
        [    0.623896] videodev: Linux video capture interface: v2.00
        [    0.629952] pps_core: LinuxPPS API ver. 1 registered
        [    0.634180] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
        [    0.643487] PTP clock support registered
        [    0.648561] Advanced Linux Sound Architecture Driver Initialized.
        [    0.657828] Bluetooth: Core ver 2.22
        [    0.658737] NET: Registered protocol family 31
        [    0.663014] Bluetooth: HCI device and connection manager initialized
        [    0.669584] Bluetooth: HCI socket layer initialized
        [    0.674265] Bluetooth: L2CAP socket layer initialized
        [    0.679632] Bluetooth: SCO socket layer initialized
        [    0.686984] clocksource: Switched to clocksource mxc_timer1
        [    1.007680] VFS: Disk quotas dquot_6.6.0
        [    1.008990] VFS: Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
        [    1.065012] NET: Registered protocol family 2
        [    1.069590] tcp_listen_portaddr_hash hash table entries: 256 (order: 1, 10240 bytes)
        [    1.074595] TCP established hash table entries: 4096 (order: 2, 16384 bytes)
        [    1.081854] TCP bind hash table entries: 4096 (order: 5, 147456 bytes)
        [    1.088819] TCP: Hash tables configured (established 4096 bind 4096)
        [    1.095103] UDP hash table entries: 256 (order: 2, 20480 bytes)
        [    1.100581] UDP-Lite hash table entries: 256 (order: 2, 20480 bytes)
        [    1.107496] NET: Registered protocol family 1
        [    1.114039] RPC: Registered named UNIX socket transport module.
        [    1.117515] RPC: Registered udp transport module.
        [    1.121858] RPC: Registered tcp transport module.
        [    1.126552] RPC: Registered tcp NFSv4.1 backchannel transport module.
        [    1.137939] hw perfevents: no interrupt-affinity property for /pmu, guessing.
        [    1.143341] hw perfevents: enabled with armv7_cortex_a9 PMU driver, 7 counters available
        [    1.157589] Initialise system trusted keyrings
        [    1.160156] workingset: timestamp_bits=30 max_order=17 bucket_order=0
        [    1.189590] NFS: Registering the id_resolver key type
        [    1.191961] Key type id_resolver registered
        [    1.196010] Key type id_legacy registered
        [    1.200422] jffs2: version 2.2. (NAND) ï¿½Â© 2001-2006 Red Hat, Inc.
        [    1.208473] fuse init (API version 7.27)
        [    1.229873] Key type asymmetric registered
        [    1.231255] Asymmetric key parser 'x509' registered
        [    1.236152] io scheduler noop registered
        [    1.240096] io scheduler deadline registered
        [    1.244648] io scheduler cfq registered (default)
        [    1.249289] io scheduler mq-deadline registered
        [    1.253419] io scheduler kyber registered
        [    1.266813] pwm-backlight backlight-lvds: backlight-lvds supply power not found, using dummy regulator
        [    1.273907] pwm-backlight backlight-lvds: Linked as a consumer to regulator.0
        [    1.302767] imx-pgc-pd imx-pgc-power-domain.0: DMA mask not set
        [    1.306320] imx-pgc-pd imx-pgc-power-domain.0: Linked as a consumer to 20dc000.gpc
        [    1.314443] imx-sdma 20ec000.sdma: Direct firmware load for imx/sdma/sdma-imx6q.bin failed with error -2
        [    1.317333] imx-pgc-pd imx-pgc-power-domain.1: DMA mask not set
        [    1.323256] imx-sdma 20ec000.sdma: external firmware not found, using ROM firmware
        [    1.329589] imx-pgc-pd imx-pgc-power-domain.1: Linked as a consumer to regulator.5
        [    1.344696] imx-pgc-pd imx-pgc-power-domain.1: Linked as a consumer to 20dc000.gpc
        [    1.357129] 21f0000.serial: ttymxc3 at MMIO 0x21f0000 (irq = 67, base_baud = 5000000) is a IMX
        [    1.366121] console [ttymxc3] enabled
        [    1.366121] console [ttymxc3] enabled
        [    1.370780] bootconsole [ec_imx21] disabled
        [    1.370780] bootconsole [ec_imx21] disabled
        [    1.406060] etnaviv etnaviv: bound 130000.gpu (ops gpu_ops)
        [    1.412928] etnaviv etnaviv: bound 134000.gpu (ops gpu_ops)
        [    1.419649] etnaviv etnaviv: bound 2204000.gpu (ops gpu_ops)
        [    1.425375] etnaviv-gpu 130000.gpu: model: GC2000, revision: 5108
        [    1.440028] etnaviv-gpu 134000.gpu: model: GC320, revision: 5007
        [    1.455711] etnaviv-gpu 2204000.gpu: model: GC355, revision: 1215
        [    1.461980] etnaviv-gpu 2204000.gpu: Ignoring GPU with VG and FE2.0
        [    1.471976] [drm] Initialized etnaviv 1.2.0 20151214 for etnaviv on minor 0
        [    1.485558] imx-ipuv3 2400000.ipu: IPUv3H probed
        [    1.494746] [drm] Supports vblank timestamp caching Rev 2 (21.10.2013).
        [    1.501599] [drm] No driver support for vblank timestamp query.
        [    1.509473] imx-drm display-subsystem: bound imx-ipuv3-crtc.2 (ops ipu_crtc_ops)
        [    1.517537] imx-drm display-subsystem: bound imx-ipuv3-crtc.3 (ops ipu_crtc_ops)
        [    1.525513] imx-drm display-subsystem: bound imx-ipuv3-crtc.6 (ops ipu_crtc_ops)
        [    1.533513] imx-drm display-subsystem: bound imx-ipuv3-crtc.7 (ops ipu_crtc_ops)
        [    1.542682] imx-drm display-subsystem: bound ldb (ops imx_ldb_ops)
        [    1.599213] Console: switching to colour frame buffer device 100x30
        [    1.618067] imx-drm display-subsystem: fb0: DRM emulated frame buffer device
        [    1.628930] [drm] Initialized imx-drm 1.0.0 20120507 for display-subsystem on minor 1
        [    1.637142] imx-ipuv3 2800000.ipu: IPUv3H probed
        [    1.699351] brd: module loaded
        [    1.742994] loop: module loaded
        [    1.757165] etnaviv-gpu 130000.gpu: timed out waiting for idle: idle=0x7ffffffe
        [    2.797481] gpmi-nand 112000.gpmi-nand: DMA timeout, last DMA
        [    2.803281] gpmi-nand 112000.gpmi-nand: Show GPMI registers :
        [    2.809201] gpmi-nand 112000.gpmi-nand: offset 0x000 : 0x20830001
        [    2.815342] gpmi-nand 112000.gpmi-nand: offset 0x010 : 0x00000000
        [    2.821575] gpmi-nand 112000.gpmi-nand: offset 0x020 : 0x00000000
        [    2.827825] gpmi-nand 112000.gpmi-nand: offset 0x030 : 0x00000000
        [    2.833962] gpmi-nand 112000.gpmi-nand: offset 0x040 : 0x00000000
        [    2.840203] gpmi-nand 112000.gpmi-nand: offset 0x050 : 0x00000000
        [    2.846338] gpmi-nand 112000.gpmi-nand: offset 0x060 : 0x0104000c
        [    2.852576] gpmi-nand 112000.gpmi-nand: offset 0x070 : 0x00020101
        [    2.858818] gpmi-nand 112000.gpmi-nand: offset 0x080 : 0x60000000
        [    2.864954] gpmi-nand 112000.gpmi-nand: offset 0x090 : 0x03023336
        [    2.871182] gpmi-nand 112000.gpmi-nand: offset 0x0a0 : 0x00000000
        [    2.877428] gpmi-nand 112000.gpmi-nand: offset 0x0b0 : 0xff000005
        [    2.883567] gpmi-nand 112000.gpmi-nand: offset 0x0c0 : 0x00000001
        [    2.889803] gpmi-nand 112000.gpmi-nand: offset 0x0d0 : 0x05010000
        [    2.895937] gpmi-nand 112000.gpmi-nand: Show BCH registers :
        [    2.901740] gpmi-nand 112000.gpmi-nand: offset 0x000 : 0x00000000
        [    2.907988] gpmi-nand 112000.gpmi-nand: offset 0x010 : 0x00000010
        [    2.914125] gpmi-nand 112000.gpmi-nand: offset 0x020 : 0x00000000
        [    2.920365] gpmi-nand 112000.gpmi-nand: offset 0x030 : 0x00000000
        [    2.926501] gpmi-nand 112000.gpmi-nand: offset 0x040 : 0x00000000
        [    2.932738] gpmi-nand 112000.gpmi-nand: offset 0x050 : 0x00000000
        [    2.938982] gpmi-nand 112000.gpmi-nand: offset 0x060 : 0x00000000
        [    2.945119] gpmi-nand 112000.gpmi-nand: offset 0x070 : 0xe4e4e4e4
        [    2.951356] gpmi-nand 112000.gpmi-nand: offset 0x080 : 0x070a4080
        [    2.957598] gpmi-nand 112000.gpmi-nand: offset 0x090 : 0x10da4080
        [    2.963732] gpmi-nand 112000.gpmi-nand: offset 0x0a0 : 0x070a4080
        [    2.969970] gpmi-nand 112000.gpmi-nand: offset 0x0b0 : 0x10da4080
        [    2.976106] gpmi-nand 112000.gpmi-nand: offset 0x0c0 : 0x070a4080
        [    2.982346] gpmi-nand 112000.gpmi-nand: offset 0x0d0 : 0x10da4080
        [    2.988587] gpmi-nand 112000.gpmi-nand: offset 0x0e0 : 0x070a4080
        [    2.994721] gpmi-nand 112000.gpmi-nand: offset 0x0f0 : 0x10da4080
        [    3.000956] gpmi-nand 112000.gpmi-nand: offset 0x100 : 0x00000000
        [    3.007198] gpmi-nand 112000.gpmi-nand: offset 0x110 : 0x00000000
        [    3.013332] gpmi-nand 112000.gpmi-nand: offset 0x120 : 0x00000000
        [    3.019563] gpmi-nand 112000.gpmi-nand: offset 0x130 : 0x00000000
        [    3.025698] gpmi-nand 112000.gpmi-nand: offset 0x140 : 0x00000000
        [    3.031935] gpmi-nand 112000.gpmi-nand: offset 0x150 : 0x20484342
        [    3.038179] gpmi-nand 112000.gpmi-nand: offset 0x160 : 0x01000000
        [    3.044317] gpmi-nand 112000.gpmi-nand: offset 0x170 : 0x00000000
        [    3.050563] gpmi-nand 112000.gpmi-nand: BCH Geometry :
        [    3.050563] GF length              : 0
        [    3.050563] ECC Strength           : 0
        [    3.050563] Page Size in Bytes     : 0
        [    3.050563] Metadata Size in Bytes : 0
        [    3.050563] ECC Chunk Size in Bytes: 0
        [    3.050563] ECC Chunk Count        : 0
        [    3.050563] Payload Size in Bytes  : 1024
        [    3.050563] Auxiliary Size in Bytes: 128
        [    3.050563] Auxiliary Status Offset: 0
        [    3.050563] Block Mark Byte Offset : 0
        [    3.050563] Block Mark Bit Offset  : 0
        [    3.097412] gpmi-nand 112000.gpmi-nand: Chip: 0, Error -110
        [    3.103152] gpmi-nand 112000.gpmi-nand: Chip: 0, Error -22
        [    3.108790] gpmi-nand 112000.gpmi-nand: Chip: 0, Error -22
        [    3.114336] gpmi-nand 112000.gpmi-nand: Chip: 0, Error -22
        [    3.119984] gpmi-nand 112000.gpmi-nand: Chip: 0, Error -22
        [    3.125513] nand: No NAND device found
        [    3.135679] libphy: Fixed MDIO Bus: probed
        [    3.141950] CAN device driver interface
        [    3.146829] flexcan 2090000.flexcan: Linked as a consumer to regulator.9
        [    3.156121] flexcan 2090000.flexcan: device registered (reg_base=(ptrval), irq=30)
        [    3.164707] flexcan 2094000.flexcan: Linked as a consumer to regulator.9
        [    3.173509] flexcan 2094000.flexcan: device registered (reg_base=(ptrval), irq=31)
        [    3.184791] fec 2188000.ethernet: 2188000.ethernet supply phy not found, using dummy regulator
        [    3.193977] fec 2188000.ethernet: Linked as a consumer to regulator.0
        [    3.205632] pps pps0: new PPS source ptp0
        [    3.211043] fec 2188000.ethernet (unnamed net_device) (uninitialized): Invalid MAC address: 00:00:00:00:00:00
        [    3.221146] fec 2188000.ethernet (unnamed net_device) (uninitialized): Using random MAC address: ce:1b:e6:93:20:79
        [    3.247287] libphy: fec_enet_mii_bus: probed
        [    3.253253] fec 2188000.ethernet eth0: registered PHC device 0
        [    3.261854] usbcore: registered new interface driver asix
        [    3.267612] usbcore: registered new interface driver ax88179_178a
        [    3.273930] usbcore: registered new interface driver cdc_ether
        [    3.280076] usbcore: registered new interface driver net1080
        [    3.285924] usbcore: registered new interface driver cdc_subset
        [    3.292131] usbcore: registered new interface driver zaurus
        [    3.298063] usbcore: registered new interface driver cdc_ncm
        [    3.303767] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
        [    3.310418] ehci-pci: EHCI PCI platform driver
        [    3.315093] ehci-mxc: Freescale On-Chip EHCI Host driver
        [    3.321857] usbcore: registered new interface driver usb-storage
        [    3.333990] imx_usb 2184000.usb: Linked as a consumer to regulator.11
        [    3.348852] ci_hdrc ci_hdrc.0: EHCI Host Controller
        [    3.354112] ci_hdrc ci_hdrc.0: new USB bus registered, assigned bus number 1
        [    3.387136] ci_hdrc ci_hdrc.0: USB 2.0 started, EHCI 1.00
        [    3.398319] hub 1-0:1.0: USB hub found
        [    3.402581] hub 1-0:1.0: 1 port detected
        [    3.411864] imx_usb 2184200.usb: Linked as a consumer to regulator.10
        [    3.423107] ci_hdrc ci_hdrc.1: EHCI Host Controller
        [    3.428281] ci_hdrc ci_hdrc.1: new USB bus registered, assigned bus number 2
        [    3.467105] ci_hdrc ci_hdrc.1: USB 2.0 started, EHCI 1.00
        [    3.475714] hub 2-0:1.0: USB hub found
        [    3.479909] hub 2-0:1.0: 1 port detected
        [    3.499496] input: max11801_ts as /devices/soc0/soc/2100000.aips-bus/21a0000.i2c/i2c-0/0-0048/input/input0
        [    3.522605] snvs_rtc 20cc000.snvs:snvs-rtc-lp: rtc core: registered 20cc000.snvs:snvs-rtc-lp as rtc0
        [    3.532625] i2c /dev entries driver
        [    3.532983] random: fast init done
        [    3.550859] imx2-wdt 20bc000.wdog: timeout 60 sec (nowayout=0)
        [    3.558128] Bluetooth: HCI UART driver ver 2.3
        [    3.562626] Bluetooth: HCI UART protocol H4 registered
        [    3.568221] Bluetooth: HCI UART protocol LL registered
        [    3.576009] sdhci: Secure Digital Host Controller Interface driver
        [    3.582350] sdhci: Copyright(c) Pierre Ossman
        [    3.586751] sdhci-pltfm: SDHCI platform and OF driver helper
        [    3.595298] sdhci-esdhc-imx 2190000.usdhc: Got CD GPIO
        [    3.638809] mmc0: SDHCI controller on 2190000.usdhc [2190000.usdhc] using ADMA
        [    3.649600] usbcore: registered new interface driver usbhid
        [    3.655220] usbhid: USB HID core driver
        [    3.668105] imx-media: subdev ipu1_vdic bound
        [    3.672957] imx-media: subdev ipu2_vdic bound
        [    3.678189] imx-media: subdev ipu1_ic_prp bound
        [    3.684548] ipu1_ic_prpenc: Registered ipu1_ic_prpenc capture as /dev/video0
        [    3.687903] mmc0: host does not support reading read-only switch, assuming write-enable
        [    3.692118] imx-media: subdev ipu1_ic_prpenc bound
        [    3.705758] ipu1_ic_prpvf: Registered ipu1_ic_prpvf capture as /dev/video1
        [    3.710982] mmc0: new high speed SDHC card at address aaaa
        [    3.712867] imx-media: subdev ipu1_ic_prpvf bound
        [    3.721588] mmcblk0: mmc0:aaaa SS08G 7.40 GiB 
        [    3.723288] imx-media: subdev ipu2_ic_prp bound
        [    3.733384] ipu2_ic_prpenc: Registered ipu2_ic_prpenc capture as /dev/video2
        [    3.739278]  mmcblk0: p1
        [    3.740674] imx-media: subdev ipu2_ic_prpenc bound
        [    3.749087] ipu2_ic_prpvf: Registered ipu2_ic_prpvf capture as /dev/video3
        [    3.756097] imx-media: subdev ipu2_ic_prpvf bound
        [    3.763099] ipu1_csi0: Registered ipu1_csi0 capture as /dev/video4
        [    3.769481] imx-media: subdev ipu1_csi0 bound
        [    3.775007] ipu1_csi1: Registered ipu1_csi1 capture as /dev/video5
        [    3.781391] imx-media: subdev ipu1_csi1 bound
        [    3.787052] ipu2_csi0: Registered ipu2_csi0 capture as /dev/video6
        [    3.793294] imx-media: subdev ipu2_csi0 bound
        [    3.798999] ipu2_csi1: Registered ipu2_csi1 capture as /dev/video7
        [    3.805239] imx-media: subdev ipu2_csi1 bound
        [    3.815756] optee: probing for conduit method from DT.
        I/TC: Dynamic shared memory is enabled
        [    3.821057] optee: revision 3.3 (ee595e95)
        [    3.826361] optee: initialized driver
        [    3.842348] sgtl5000 2-000a: Linked as a consumer to regulator.7
        [    3.847166] usb 2-1: new high-speed USB device number 2 using ci_hdrc
        [    3.849043] sgtl5000 2-000a: Dropping the link to regulator.7
        [    3.862448] sgtl5000 2-000a: Linked as a consumer to regulator.8
        [    3.869046] sgtl5000 2-000a: Linked as a consumer to regulator.9
        [    3.875526] sgtl5000 2-000a: Linked as a consumer to regulator.7
        [    3.884344] sgtl5000 2-000a: Error reading chip id -6
        [    3.889919] sgtl5000 2-000a: Dropping the link to regulator.8
        [    3.896069] sgtl5000 2-000a: Dropping the link to regulator.9
        [    3.903215] sgtl5000 2-000a: Dropping the link to regulator.7
        [    3.918960] fsl-ssi-dai 2028000.ssi: No cache defaults, reading back from HW
        [    3.936809] NET: Registered protocol family 10
        [    3.946827] Segment Routing with IPv6
        [    3.951015] sit: IPv6, IPv4 and MPLS over IPv4 tunneling driver
        [    3.959870] NET: Registered protocol family 17
        [    3.964416] can: controller area network core (rev 20170425 abi 9)
        [    3.971178] NET: Registered protocol family 29
        [    3.975728] can: raw protocol (rev 20170425)
        [    3.980320] can: broadcast manager protocol (rev 20170425 t)
        [    3.986073] can: netlink gateway (rev 20170425) max_hops=1
        [    3.992631] Key type dns_resolver registered
        [    4.000036] cpu cpu0: Linked as a consumer to regulator.4
        [    4.005829] cpu cpu0: Linked as a consumer to regulator.5
        [    4.011739] cpu cpu0: Linked as a consumer to regulator.6
        [    4.023404] Registering SWP/SWPB emulation handler
        [    4.031655] Loading compiled-in X.509 certificates
        [    4.051831] hub 2-1:1.0: USB hub found
        [    4.056247] hub 2-1:1.0: 4 ports detected
        [    4.150497] imx-media: subdev ipu1_csi0_mux bound
        [    4.156761] imx-media: subdev ipu2_csi1_mux bound
        [    4.161952] imx-media: ipu2_csi1:1 -> ipu2_ic_prp:0
        [    4.167058] imx-media: ipu2_csi1:1 -> ipu2_vdic:0
        [    4.171853] imx-media: ipu2_csi1_mux:2 -> ipu2_csi1:0
        [    4.177095] imx-media: ipu2_csi0:1 -> ipu2_ic_prp:0
        [    4.182030] imx-media: ipu2_csi0:1 -> ipu2_vdic:0
        [    4.186816] imx-media: ipu1_csi1:1 -> ipu1_ic_prp:0
        [    4.191879] imx-media: ipu1_csi1:1 -> ipu1_vdic:0
        [    4.196677] imx-media: ipu1_csi0:1 -> ipu1_ic_prp:0
        [    4.201729] imx-media: ipu1_csi0:1 -> ipu1_vdic:0
        [    4.206555] imx-media: ipu1_csi0_mux:2 -> ipu1_csi0:0
        [    4.211775] imx-media: ipu2_ic_prp:1 -> ipu2_ic_prpenc:0
        [    4.217262] imx-media: ipu2_ic_prp:2 -> ipu2_ic_prpvf:0
        [    4.222548] imx-media: ipu1_ic_prp:1 -> ipu1_ic_prpenc:0
        [    4.228014] imx-media: ipu1_ic_prp:2 -> ipu1_ic_prpvf:0
        [    4.233295] imx-media: ipu2_vdic:2 -> ipu2_ic_prp:0
        [    4.238324] imx-media: ipu1_vdic:2 -> ipu1_ic_prp:0
        [    4.261225] imx_thermal tempmon: Industrial CPU temperature grade - max:105C critical:100C passive:95C
        [    4.279775] snvs_rtc 20cc000.snvs:snvs-rtc-lp: setting system clock to 1970-01-01 00:00:00 UTC (0)
        [    4.289558] cfg80211: Loading compiled-in X.509 certificates for regulatory database
        [    4.305308] cfg80211: Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
        [    4.313379] ALSA device list:
        [    4.316481]   No soundcards found.
        [    4.321343] platform regulatory.0: Direct firmware load for regulatory.db failed with error -2
        [    4.330340] cfg80211: failed to load regulatory.db
        [    4.379989] EXT4-fs (mmcblk0p1): mounted filesystem with ordered data mode. Opts: (null)
        [    4.388566] VFS: Mounted root (ext4 filesystem) on device 179:1.
        [    4.402367] devtmpfs: mounted
        [    4.408244] Freeing unused kernel memory: 1024K
        [    4.429082] Run /sbin/init as init process
        [    4.596182] EXT4-fs (mmcblk0p1): re-mounted. Opts: (null)
        Starting logging: OK
        Initializing random number generator... [    4.937381] random: dd: uninitialized urandom read (512 bytes read)
        done.
        Starting network: OK

        Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo
        buildroot login: 
        Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo
        buildroot login: root
        # uname -a
        Linux buildroot 4.19.0-00618-gbad5e39a548d #16 SMP Wed Oct 24 18:00:15 IST 2018 armv7l GNU/Linux
