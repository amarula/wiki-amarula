Boot Linux on Vyasa RK3288
==========================


Build the images here, and setup SD card with Single partition here

    bootm
        Ramdisk
        Rootfs
    Monolithic
    FIT
    Verified Boot

bootm
Ramdisk

Create Single partition and Insert the SD on host and Built the images from Image Build

::

        $ cd /path/to/u-boot
        $./tools/mkimage -n rk3288 -T rksd -d ./tpl/u-boot-tpl.bin out
        $ cat ./spl/u-boot-spl-dtb.bin >> out
        $ dd if=out of=/dev/mmcblk0 seek=64
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 seek=256
        $ cd /path/to/linux-next
        $ cp arch/arm/boot/uImage /media/jagan/rootfs/boot
        $ cp arch/arm/boot/dts/rk3288-vyasa.dtb /media/jagan/rootfs/boot
        $ cp arm_ramdisk.image /media/jagan/rootfs
        $ sync
        $ umount /dev/mmcblk0p1

Close JP4 and Insert the SD card and power-on the board.

::

        U-Boot TPL 2017.11-rc1-00238-g26f9184 (Oct 13 2017 - 21:15:23)

        Trying to boot from BOOTROM

        Returning to boot ROM...


        U-Boot SPL 2017.11-rc1-00238-g26f9184 (Oct 13 2017 - 21:15:23)

        Trying to boot from MMC1

        Expected Linux image is not found. Trying to start U-boot



        U-Boot 2017.11-rc1-00238-g26f9184 (Oct 13 2017 - 21:15:23 +0530)


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

        => setenv bootargs 'console=ttyS2,115200n8 root=/dev/ram0 rw initrd=0x03000000,16M ramdisk_size=16384'

        => ext4load mmc 0:1 ${kernel_addr_r} uImage

        => ext4load mmc 0:1 ${fdt_addr_r} rk3288-vyasa.dtb

        => ext4load mmc 0:1 0x03000000 arm_ramdisk.image

        => bootm ${kernel_addr_r} - ${fdt_addr_r}

        reading uImage

        7343688 bytes read in 537 ms (13 MiB/s)

        reading rk3288-vyasa.dtb

        34632 bytes read in 9 ms (3.7 MiB/s)

        reading arm_ramdisk.image

        16777216 bytes read in 1212 ms (13.2 MiB/s)

        ## Booting kernel from Legacy Image at 02000000 ...

           Image Name:   Linux-4.11.0-00003-gb75686b-dirt

           Image Type:   ARM Linux Kernel Image (uncompressed)

           Data Size:    7343624 Bytes = 7 MiB

           Load Address: 02000000

           Entry Point:  02000000

           Verifying Checksum ... OK

        ## Flattened Device Tree blob at 01f00000

           Booting using the fdt blob at 0x1f00000

           Loading Kernel Image ... OK

           Loading Device Tree to 0fff4000, end 0ffff747 ... OK


        Starting kernel ...

Rootfs

Create Single partition and Insert the SD on host and Built the images from Image Build

::

        $ cd /path/to/u-boot

        $./tools/mkimage -n rk3288 -T rksd -d ./tpl/u-boot-tpl.bin out
        $ cat ./spl/u-boot-spl-dtb.bin >> out
        $ dd if=out of=/dev/mmcblk0 seek=64
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 seek=256
        $ cp -rf rfs-rk3288/* /media/jagan/rootfs
        $ cd /path/to/linux-next
        $ cp arch/arm/boot/uImage /media/jagan/rootfs/boot
        $ cp arch/arm/boot/dts/rk3288-vyasa.dtb /media/jagan/rootfs/boot

Create extlinux script

::

        $ cat /mnt/boot/extlinux/extlinux.conf

        label Vyasa kernel-4.13

                kernel /boot/uImage

                devicetree /boot/rk3288-vyasa.dtb

                append console=ttyS2,115200n8 root=/dev/mmcblk0p1 rootwait

        $ sync
        $ umount /dev/mmcblk0p1

Close JP4 and Insert the SD card and power-on the board.

::

        Hit any key to stop autoboot:  0

        switch to partitions #0, OK

        mmc1 is current device

        Scanning mmc 1:1...

        Found /extlinux/extlinux.conf

        Retrieving file: /extlinux/extlinux.conf

        reading /extlinux/extlinux.conf

        128 bytes read in 7 ms (17.6 KiB/s)

        1:      Vyasa kernel-4.13

        Retrieving file: /boot/uImage

        reading /boot/uImage

        7836888 bytes read in 575 ms (13 MiB/s)

        append: console=ttyS2,115200n8 root=/dev/mmcblk0p2 rootwait

        Retrieving file: /boot/rk3288-vyasa.dtb

        reading /boot/rk3288-vyasa.dtb

        36283 bytes read in 12 ms (2.9 MiB/s)

        ## Booting kernel from Legacy Image at 02000000 ...

           Image Name:   Linux-4.13.0-rc4-next-20170810-0

           Image Type:   ARM Linux Kernel Image (uncompressed)

           Data Size:    7836824 Bytes = 7.5 MiB

           Load Address: 02000000

           Entry Point:  02000000

           Verifying Checksum ... OK

        ## Flattened Device Tree blob at 01f00000

           Booting using the fdt blob at 0x1f00000

           Loading Kernel Image ... OK

           Loading Device Tree to 0fff4000, end 0ffffdba ... OK


        Starting kernel ...

Monolithic
FIT
Verified Boot


