Engicam i.MX6Q
==============

Partitions
================= ====================== =============
Start KB (blocks)  Size KB (Blocks)       Usage             
================= ====================== =============
0                   1KB (2)               Partition Table etc
1KB (0x2)           68KB (0x88)           SPL
1MB (0x800)         1MB (0x800)           args/dtb
2MB (0x1000)        8M (0x4000)           kernel
10M (0x5000)        partitions            rootfs
69KB (0x8a)         640KB (0x500)         U-Boot
709KB (0x58a)       256KB (0x512)         env (redundant)
965KB               59KB                  unused
================= ====================== =============

Built the images from Image Build

Configure SD
Create Falcon partition and Insert the SD on host

::

        $ cd /path/to/
        $ dd if=SPL of=/dev/mmcblk0 bs=1k seek=1
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 bs=1k seek=69
        $ git clone https://github.com/openedev/rootfs-imx6q
        $ cp -rf rootfs-imx6q/* /media/jagan/rootfs
        $ cp /path/to/linux-next/arch/arm/boot/uImage /media/jagan/rootfs
        $ cp arch/arm/boot/dts/imx6q-icore.dtb /media/jagan/rootfs
        $ sync && sudo umount /dev/mmcblk0*
        
Configure Falcon
Insert the SD and power-on the board.

::

        # load kernel from rootfs
        icorem6qdl> ext4load mmc ${mmcdev}:${mmcpart} ${loadaddr} ${image}
        6449304 bytes read in 376 ms (16.4 MiB/s)

        # write kernel at 2MB offset
        icorem6qdl> mmc write ${loadaddr} 0x1000 0x4000

        MMC write: dev # 0, block # 4096, count 16384 ... 16384 blocks written: OK

        # setup kernel bootargs
        icorem6qdl> setenv bootargs 'console=ttymxc3,115200 root=/dev/mmcblk0p1 rootfstype=ext4 rootwait rw'

        # load device-tree from rootfs
        icorem6qdl> ext4load mmc ${mmcdev}:${mmcpart} ${fdt_addr} ${fdt_file}
        37081 bytes read in 43 ms (841.8 KiB/s)

        # prepare args
        icorem6qdl> spl export fdt ${loadaddr} - ${fdt_addr}
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-4.14.0-rc2-next-20170929
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    6449240 Bytes = 6.2 MiB
           Load Address: 10008000
           Entry Point:  10008000
           Verifying Checksum ... OK
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Using Device Tree in place at 18000000, end 1800c0d8
        subcommand not supported
        subcommand not supported
           Using Device Tree in place at 18000000, end 1800f0d8
        Argument image is now in RAM: 0x18000000

        # write args 1MB data (0x800 sectors) to 1MB offset (0x800 sectors)
        icorem6qdl> mmc write 18000000 0x800 0x800

        MMC write: dev # 0, block # 2048, count 2048 ... 2048 blocks written: OK

Boot Linux using Falcon
Reset the board and see Linux booting, Pressing 'C' will prevent Linux boot and moved to U-Boot.

::

        U-Boot SPL 2017.11-00056-g3751590 (Nov 20 2017 - 23:14:20)
        Trying to boot from MMC1
        [    0.000000] Booting Linux on physical CPU 0x0
        [    0.000000] Linux version 4.14.0-rc2-next-20170929 (root@jagan-XPS-13-9350) (gcc version 6.4.0 (Buildroot 2017.11-git-00570-ged6f079)) #1 SMP Tue Oct 3 15:15:58 IST 2017
        [    0.000000] CPU: ARMv7 Processor [412fc09a] revision 10 (ARMv7), cr=10c5387d
        [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        [    0.000000] OF: fdt: Machine model: Engicam i.CoreM6 Quad/Dual Starter Kit
