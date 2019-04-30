Orangepi Win
############

This tutorial will show the details of Orangepi Win/Win+ board mainline support and other needed details, for more information about `hardware <http://www.orangepi.org/OrangePiWin_WinPlus/>`_ and `linux-sunxi <https://linux-sunxi.org/Xunlong_Orange_Pi_Win>`_

Hardware Access
***************
Serial debug and Power connections

.. image:: /images/opi_win.jpeg




BSP Build
*********

Manual Build
============
Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/uboot/tools.html#arm64>`_

Below are the details of Image build for Orangepi Win/Win+ board.

ATF
---
::

        $ git clone https://github.com/apritzel/arm-trusted-firmware.git
        $ cd arm-trusted-firmware
        $ make PLAT=sun50iw1p1 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin
        
U-Boot
------
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make orangepi_win_defconfig
        $ make 
        
Linux
-----
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs

Buildroot
=========
It's easy to build entire system using buildroot and mainline supported orangepi-win already. See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/orangepi/orangepi-win/readme.txt>`_ for more info.

::

        $ git clone git://git.busybox.net/buildroot
        $ cd buildroot
        $ make orangepi_win_defconfig
        $ make

SD Boot
*******
Partition the SD card in host with `Single Falcon partition <https://wiki.amarulasolutions.com/uboot/tools.html#falcon-partition>`_
::

        $ git clone https://github.com/openedev/rootfs-sun64
        $ cp -rf rootfs-sun64/* /media/jagan/rootfs/
        $ cp /to/linux-next/arch/arm64/boot/Image /media/jagan/rootfs/boot
        $ cp /to/linux-next/arch/arm64/boot/dts/allwinner/sun50i-a64-orangepi-win.dtb /media/jagan/rootfs/boot
        $ cd /to/u-boot
        $ cat spl/sunxi-spl.bin u-boot.itb > u-boot-sunxi-with-spl.bin
        $ dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1
        $ sync && umount /dev/mmcblk0*

Insert the SD card and power-on the board. See the Linux boot start from SPL

::

        U-Boot SPL 2017.11-00061-g6130b1f (Nov 23 2017 - 22:22:00)
        DRAM: 1024 MiB
        Trying to boot from MMC1
        NOTICE:  BL3-1: Running on A64/H64 (1689) in SRAM A2 (@0x44000)
        NOTICE:  Configuring SPC Controller
        NOTICE:  BL3-1: v1.0(debug):aa75c8d
        NOTICE:  BL3-1: Built : 23:14:48, Nov  4 2017
        NOTICE:  Configuring AXP PMIC
        NOTICE:  PMIC: Output power control 2 is an unexpected 0x0
        ERROR:   PMIC: setup failed: -3
        INFO:    BL3-1: Initializing runtime services
        INFO:    BL3-1: Preparing for EL3 exit to normal world
        INFO:    BL3-1: Next image address: 0x4a000000, SPSR: 0x3c9

        U-Boot 2017.11-00061-g6130b1f (Nov 23 2017 - 22:22:00 +0530) Allwinner Technology

        CPU:   Allwinner A64 (SUN50I)
        Model: OrangePi Win/Win Plus
        DRAM:  1 GiB
        MMC:   SUNXI SD/MMC: 0
        *** Warning - bad CRC, using default environment

        Warning: HDMI PHY init timeout!
        Warning: HDMI PHY init timeout!
        In:    serial
        Out:   serial
        Err:   serial
        Net:   No ethernet found.
        starting USB...
        USB0:   USB EHCI 1.00
        USB1:   USB OHCI 1.0
        scanning bus 0 for devices... 1 USB Device(s) found
               scanning usb for storage devices... 0 Storage Device(s) found
        Hit any key to stop autoboot:  0
        switch to partitions #0, OK
        mmc0 is current device
        Scanning mmc 0:1...
        Found /boot/extlinux/extlinux.conf
        Retrieving file: /boot/extlinux/extlinux.conf
        156 bytes read in 261 ms (0 Bytes/s)
        1:      linux-next
        Retrieving file: /boot/Image
        16908800 bytes read in 1073 ms (15 MiB/s)
        append: console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait
        Retrieving file: /boot/sun50i-a64-orangepi-win.dtb
        11879 bytes read in 240 ms (47.9 KiB/s)
        ## Flattened Device Tree blob at 4fa00000
           Booting using the fdt blob at 0x4fa00000
           Loading Device Tree to 0000000049ffa000, end 0000000049fffe66 ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
        [    0.000000] Linux version 4.14.0-next-20171123-00001-gae19a8e (root@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #2 SMP PREEMPT Thu Nov 23 22:557
        [    0.000000] Machine model: OrangePi Win/Win Plus
        [    0.000000] efi: Getting EFI parameters from FDT:
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 16 MiB at 0x000000007f000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000000000-0x000000007fffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0x7efe4180-0x7efe5c7f]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA      [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000]   Normal   empty
        [    0.000000] Movable zone start for each node
        [    0.000000] Early memory node ranges
        [    0.000000]   node   0: [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000] Initmem setup node 0 [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv0.2 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: Trusted OS migration not required
        [    0.000000] random: get_random_bytes called from start_kernel+0xa4/0x408 with crng_init=0
        [    0.000000] percpu: Embedded 23 pages/cpu @ffff80003ef81000 s55832 r8192 d30184 u94208
        [    0.000000] Detected VIPT I-cache on CPU0
        [    0.000000] CPU features: enabling workaround for ARM erratum 845719
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 258048
        [    0.000000] Policy zone: DMA
        [    0.000000] Kernel command line: console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait

FEL/USB Boot
************
More information `here <http://linux-sunxi.org/FEL/USBBoot>`_ and build the fel tools `from <https://wiki.amarulasolutions.com/uboot/tools.html#sunxi>`_

Enter FEL
=========
Prepare `SD card <https://wiki.amarulasolutions.com/bsp/sunxi/a64/opi-win.html#sd-boot>`_ from and Power-on board without SD

::

        # sunxi-fel version
        ERROR: Allwinner USB FEL device not found!
        # sunxi-fel version
        AWUSBFEX soc=00001689(A64) 00000001 ver=0001 44 08 scratchpad=00017e00 00000000 00000000

Build U-Boot
============
Mainline U-Boot not supporting FEL for H5/A64 due to 64-Bit mode in SPL so we need to build 32-bit SPL and 64-bit U-Boot proper

Export arm toolchain from `here <https://wiki.amarulasolutions.com/uboot/tools.html#arm>`_

::

        $ git clone https://github.com/openedev/u-boot-amarula
        $ cd u-boot-amarula
        $ git checkout -b sun64-fel32 origin/sun64-fel32
        $ make sun50i_spl32_defconfig && make

Boot Linux
==========
From Host, get the boot.scr from `here <https://wiki.amarulasolutions.com/uboot/tools.html#boot64-fel-scr>`_

::

        # sunxi-fel -v -p spl /path/to/u-boot-amarula/sunxi-spl.bin \
        > write 0x44000 /path/to/arm-trusted-firmware/build/sun50iw1p1/debug/bl31.bin \
        > write 0x4a000000 /path/to/u-boot/u-boot.bin \
        > write 0x40080000 /root/JSpace/code/linux-next-sunxi64/arch/arm64/boot/Image \
        > write 0x4FA00000 /root/JSpace/code/linux-next-sunxi64/arch/arm64/boot/dts/allwinner/sun50i-a64-orangepi-win.dtb \
        > write 0x4FB00000 boot.scr \
        > reset64 0x44000
        Stack pointers: sp_irq=0x00012000, sp=0x00015E08
        MMU is not enabled by BROM
        => Executing the SPL... done.
        100% [================================================]    33 kB,  447.0 kB/s
        100% [================================================]   450 kB,  467.2 kB/s
        100% [================================================] 16909 kB,  467.9 kB/s
        100% [================================================]    12 kB,  476.0 kB/s
        100% [================================================]     0 kB,  130.0 kB/s
        Passing boot info via sunxi SPL: script address = 0x4FB00000, uEnv length = 0
        Store entry point 0x00044000 to RVBAR 0x017000A0, and request warm reset with RMR mode 3... done.

From Target UART

::

        U-Boot SPL 2017.09-g5f1fe13 (Nov 24 2017 - 15:25:44)
        DRAM: 1024 MiB
        Trying to boot from FEL
        NOTICE:  BL3-1: Running on A64/H64 (1689) in SRAM A2 (@0x44000)
        NOTICE:  Configuring SPC Controller
        NOTICE:  BL3-1: v1.0(debug):aa75c8d
        NOTICE:  BL3-1: Built : 23:14:48, Nov  4 2017
        NOTICE:  Configuring AXP PMIC
        NOTICE:  PMIC: setup successful
        INFO:    BL3-1: Initializing runtime services
        INFO:    BL3-1: Preparing for EL3 exit to normal world
        INFO:    BL3-1: Next image address: 0x4a000000, SPSR: 0x3c9

        U-Boot 2017.11-00063-gfb344e3 (Nov 24 2017 - 17:23:04 +0530) Allwinner Technology

        CPU:   Allwinner A64 (SUN50I)
        Model: OrangePi Win/Win Plus
        DRAM:  1 GiB
        MMC:   SUNXI SD/MMC: 0
        *** Warning - bad CRC, using default environment

        In:    serial
        Out:   serial
        Err:   serial
        Net:   No ethernet found.
        starting USB...
        USB0:   USB EHCI 1.00
        USB1:   USB OHCI 1.0
        scanning bus 0 for devices... 1 USB Device(s) found
               scanning usb for storage devices... 0 Storage Device(s) found
        Hit any key to stop autoboot:  0
        (FEL boot)
        ## Executing script at 4fb00000
        ## Flattened Device Tree blob at 4fa00000
           Booting using the fdt blob at 0x4fa00000
           Loading Device Tree to 0000000049ffa000, end 0000000049fffe66 ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
        [    0.000000] Linux version 4.14.0-next-20171123-00002-gd14e643-dirty (root@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #3 SMP PREEMPT Fri Nov 247
        [    0.000000] Machine model: OrangePi Win/Win Plus
        [    0.000000] efi: Getting EFI parameters from FDT:
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 16 MiB at 0x000000007f000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000000000-0x000000007fffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0x7efe4180-0x7efe5c7f]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA      [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000]   Normal   empty
        [    0.000000] Movable zone start for each node
        [    0.000000] Early memory node ranges
        [    0.000000]   node   0: [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000] Initmem setup node 0 [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv0.2 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: Trusted OS migration not required
        [    0.000000] random: get_random_bytes called from start_kernel+0xa4/0x408 with crng_init=0
        [    0.000000] percpu: Embedded 23 pages/cpu @ffff80003ef81000 s55832 r8192 d30184 u94208
        [    0.000000] Detected VIPT I-cache on CPU0
        [    0.000000] CPU features: enabling workaround for ARM erratum 845719
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 258048
        [    0.000000] Policy zone: DMA
        [    0.000000] Kernel command line: console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait

