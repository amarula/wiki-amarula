RK3288 Vyasa
############

Partition Table
***************

================= ====================== ====================
Start KB (blocks)  Size KB (Blocks)       Usage
================= ====================== ====================
0                       4K                Partition Table etc
4K	                32KB	          TPL
32K                     100K              SPL
8M	                1024K - 256K      U-Boot
                        1MB               env (redundant)
16MB                    1MB (0x800)       args
17MB                    8MB (0x4000)      kernel
30MB                    partitions        rootfs
================= ====================== ====================

Build
*****

::

        bash> git clone git://git.denx.de/u-boot.git
        bash> cd u-boot
        bash> make vyasa-rk3288_defconfig
        bash> make -j 4

Create SD
*********

Create Falcon partition and Insert the SD on host and Built the images from Image Build

::

        $ cd /path/to/u-boot
        $./tools/mkimage -n rk3288 -T rksd -d ./tpl/u-boot-tpl.bin out
        $ cat ./spl/u-boot-spl-dtb.bin >> out
        $ dd if=out of=/dev/mmcblk0 seek=64
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 seek=16384
        $ git clone https://github.com/openedev/rfs-rk3288
        $ cd /path/to/rfs-rk3288
        $ cp -rf * /path/to/rfs-rk3288
        $ mkdir /path/to/rfs-rk3288/boot
        $ cd /path/to/linux-next
        $ cp arch/arm/boot/uImage /path/to/rfs-rk3288
        $ cp arch/arm/boot/dts/rk3288-vyasa.dtb /path/to/rfs-rk3288
        $ sync && sudo umount /media/rfs-rk3288

Configure Falcon
****************
Now insert the SD and configure the falcon and restart

::

        U-Boot TPL 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:04:00)

        Trying to boot from BOOTROM

        Returning to boot ROM...


        U-Boot SPL 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:04:00)

        Trying to boot from MMC1

        Expected Linux image is not found. Trying to start U-boot



        U-Boot 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:04:00 +0530)


        Model: Amarula Vyasa-RK3288

        DRAM:  2 GiB

        MMC:   dwmmc@ff0c0000: 1

        *** Warning - bad CRC, using default environment


        In:    serial@ff690000

        Out:   serial@ff690000

        Err:   serial@ff690000

        Model: Amarula Vyasa-RK3288

        Net:   Net Initialization Skipped

        No ethernet found.

        Hit any key to stop autoboot:  0

        => mmc dev 1

        switch to partitions #0, OK

        mmc1 is current device

        => ext4load mmc 1:1 $kernel_addr_r /boot/uImage

        8143432 bytes read in 378 ms (20.5 MiB/s)

        => mmc write $kernel_addr_r 0x8800 0x4000      

        MMC write: dev # 1, block # 34816, count 16384 ... 16384 blocks written: OK

        => ext4load mmc 1:1 $fdt_addr_r /boot/rk3288-vyasa.dtb   

        37307 bytes read in 23 ms (1.5 MiB/s)

        => setenv bootargs 'console=ttyS2,115200n8 root=/dev/mmcblk0p1 rootwait'

        => spl export fdt $kernel_addr_r - $fdt_addr_r

        ## Booting kernel from Legacy Image at 02000000 ...

           Image Name:   Linux-4.14.0-rc4-next-20171013-0

           Image Type:   ARM Linux Kernel Image (uncompressed)

           Data Size:    8143368 Bytes = 7.8 MiB

           Load Address: 02000000

           Entry Point:  02000000

           Verifying Checksum ... OK

        ## Flattened Device Tree blob at 01f00000

           Booting using the fdt blob at 0x1f00000

           Loading Kernel Image ... OK

           Loading Device Tree to 0fff3000, end 0ffff1ba ... OK

        subcommand not supported

        subcommand not supported

           Loading Device Tree to 0ffe3000, end 0fff21ba ... OK

        Argument image is now in RAM: 0x0ffe3000

        => mmc write 0x0ffe3000 0x8000 0x800


        MMC write: dev # 1, block # 32768, count 2048 ... 2048 blocks written: OK

Falcon mode
***********
Reset or Power on board with SD, Ctr+C will boot U-Boot and/or Linux boot normally

::

        U-Boot TPL 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:11:25)

        Trying to boot from BOOTROM

        Returning to boot ROM...


        U-Boot SPL 2017.11-rc4-00029-gb142d38-dirty (Nov 10 2017 - 17:11:25)

        Trying to boot from MMC1

        [    0.000000] Booting Linux on physical CPU 0x500
        [    0.000000] Linux version 4.14.0-rc4-next-20171013-00012-gd26a4df (root@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #2 SMP Mon Oct 23 01:00:23 7
        [    0.000000] CPU: ARMv7 Processor [410fc0d1] revision 1 (ARMv7), cr=10c5387d
        [    0.000000] CPU: div instructions available: patching division code
        [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        [    0.000000] OF: fdt: Machine model: Amarula Vyasa-RK3288
