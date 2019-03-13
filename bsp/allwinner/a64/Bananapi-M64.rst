A60 Bananapi M64
======================

Hardware Access
Serial debug and Power connections

.. image:: /images/bpi-m64.jpeg


BSP Build
Manual Build
For manual building refer here for all necessary information.

Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Banana Pi BPI-M64 board.

ATF

::

        git clone https://github.com/apritzel/arm-trusted-firmware.git
        cd arm-trusted-firmware
        make PLAT=sun50iw1p1 bl31
        export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin

U-Boot

::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make bananapi_m64_defconfig
        make 

Linux

::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm64 make defconfig
        ARCH=arm64 make -j 4 Image dtbs

Buildroot
It's easy to build entire system using buildroot and mainline supported bananapi-m64 already. See read this readme.txt for more info.

::

        git clone git://git.busybox.net/buildroot
        cd buildroot
        make bananapi_m64_defconfig
        make

Booting

SD Boot

Partition the SD card in host with Single Falcon partition

Prepare SD

Write boot image

::

        cd /to/u-boot
        cat spl/sunxi-spl.bin u-boot.itb > u-boot-sunxi-with-spl.bin
        dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1

Write rootfs, update boot/extlinux/extlinux.conf

::

        git clone https://github.com/openedev/rootfs-sun64
        cp -rf rootfs-sun64/* /media/jagan/rootfs/
        cp /to/linux-next/arch/arm64/boot/Image /media/jagan/rootfs/boot
        cp /to/linux-next/arch/arm64/boot/dts/allwinner/sun50i-a64-orangepi-win.dtb /media/jagan/rootfs/boot
        sync && umount /dev/mmcblk0*

Insert the SD card and power-on the board. See the Linux boot start from SPL - unplug SD Card during U-Boot proper boot

USB Boot
Prepare SD card with from SD Boot and prepare USB mass storage with single partition by copying rootfs and update boot/extlinux/extlinux.conf

Insert the SD card, USB Mass storage and power-on the board. See the Linux boot start from SPL

::

        U-Boot SPL 2017.11-00063-gfb344e3-dirty (Nov 27 2017 - 12:38:05)
        DRAM: 2048 MiB
        Trying to boot from MMC1
        NOTICE:  BL3-1: Running on A64/H64 (1689) in SRAM A2 (@0x44000)
        NOTICE:  Configuring SPC Controller
        NOTICE:  BL3-1: v1.0(debug):aa75c8d
        NOTICE:  BL3-1: Built : 23:14:48, Nov  4 2017
        NOTICE:  Configuring AXP PMIC
        NOTICE:  PMIC: setup successful
        INFO:    BL3-1: Initializing runtime services
        INFO:    BL3-1: Preparing for EL3 exit to normal world
        INFO:    BL3-1: Next image address: 0x4a000000, SPSR: 0x3c9


        U-Boot 2017.11-00063-gfb344e3-dirty (Nov 27 2017 - 12:38:05 +0530) Allwinner Technology

        CPU:   Allwinner A64 (SUN50I)
        Model: BananaPi-M64
        DRAM:  2 GiB
        MMC:   SUNXI SD/MMC: 0, SUNXI SD/MMC: 1
        *** Warning - bad CRC, using default environment

        In:    serial
        Out:   serial
        Err:   serial
        Net:   No ethernet found.
        starting USB...
        USB0:   USB EHCI 1.00
        scanning bus 0 for devices... 3 USB Device(s) found
               scanning usb for storage devices... 1 Storage Device(s) found
        Hit any key to stop autoboot:  0
        Card did not respond to voltage select!
        mmc_init: -95, time 22
        switch to partitions #0, OK
        mmc1(part 0) is current device
        ** No partition table - mmc 1 **

        Device 0: Vendor: Sony     Rev: 0100 Prod: Storage Media   
                    Type: Removable Hard Disk
                    Capacity: 30040.8 MB = 29.3 GB (61523712 x 512)
        ... is now current device
        Scanning usb 0:1...
        Found /boot/extlinux/extlinux.conf
        Retrieving file: /boot/extlinux/extlinux.conf
        151 bytes read in 157 ms (0 Bytes/s)
        1:      linux-next
        Retrieving file: /boot/Image
        16908800 bytes read in 21856 ms (754.9 KiB/s)
        append: console=ttyS0,115200 earlyprintk root=/dev/sda1 rootwait
        Retrieving file: /boot/sun50i-a64-bananapi-m64.dtb
        12817 bytes read in 142 ms (87.9 KiB/s)
        ## Flattened Device Tree blob at 4fa00000
           Booting using the fdt blob at 0x4fa00000
           Loading Device Tree to 0000000049ff9000, end 0000000049fff210 ... OK

        Starting kernel ...

        [�r��������Booting Linux on physical CPU 0x0000000000 [0x410fd034]
        [    0.000000] Linux version 4.14.0-next-20171123-00001-gae19a8e (root@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) 7
        [    0.000000] Machine model: BananaPi-M64
        [    0.000000] efi: Getting EFI parameters from FDT:
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 16 MiB at 0x00000000bf000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000000000-0x00000000bfffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0xbefe3000-0xbefe4aff]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA      [mem 0x0000000040000000-0x00000000bfffffff]
        [    0.000000]   Normal   empty
        [    0.000000] Movable zone start for each node
        [    0.000000] Early memory node ranges
        [    0.000000]   node   0: [mem 0x0000000040000000-0x00000000bfffffff]
        [    0.000000] Initmem setup node 0 [mem 0x0000000040000000-0x00000000bfffffff]
        [    0.000000] psci: probing for conduit method from DT.
        [    0.000000] psci: PSCIv0.2 detected in firmware.
        [    0.000000] psci: Using standard PSCI v0.2 function IDs
        [    0.000000] psci: Trusted OS migration not required
        [    0.000000] random: get_random_bytes called from start_kernel+0xa4/0x408 with crng_init=0
        [    0.000000] percpu: Embedded 23 pages/cpu @ffff80007ef80000 s55832 r8192 d30184 u94208
        [    0.000000] Detected VIPT I-cache on CPU0
        [    0.000000] CPU features: enabling workaround for ARM erratum 845719
        [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 516096
        [    0.000000] Policy zone: DMA
        [    0.000000] Kernel command line: console=ttyS0,115200 earlyprintk root=/dev/sda1 rootwait
        
U-Boot
USB Mass Storage gadget
We can use the board as a USB Mass Storage device:

You will be able to access all the partitions of any block device that is on the board or connected to it,

from your host PC - You will see them as /dev/sdXX, just like connecting a regular USB storage to your PC,

and you'll be able to mount them, and have full read/write access to them.

We can even use it to flash a new U-Boot, re-partition the storage, re-format it, etc.

This is especially useful for updating the internal eMMC.

To do this you need to connect a USB cable between the OTG/Client port of the board and a regular USB Host port on your PC,

and use U-Boot's ums command.

Linux
USB OTG
Here, we can take mass storage as gadget function and will show how it can work with 'host' and 'peripheral' modes

Build otg mass storage as statically linked module with

`CONFIG_USB_MASS_STORAGE=y`

Append bootargs with 'g_mass_storage.removable=1 g_mass_storage.luns=1'

Peripheral
Plug USB otg cable A-type to host pc and B-type to bananapi

::

        [    1.952386] usb_phy_generic usb_phy_generic.0.auto: usb_phy_generic.0.auto supply vcc not found, using dummy regulator
        [    1.952954] musb-hdrc musb-hdrc.1.auto: MUSB HDRC host driver
        [    1.952965] musb-hdrc musb-hdrc.1.auto: new USB bus registered, assigned bus number 5
        [    1.957274] hub 5-0:1.0: USB hub found
        [    1.957303] hub 5-0:1.0: 1 port detected
        [    1.961702] Mass Storage Function, version: 2009/09/11
        [    1.961708] LUN: removable file: (no medium)
        [    1.961761] LUN: removable file: (no medium)
        [    1.961764] Number of LUNs=1
        [    1.972523] g_mass_storage gadget: Mass Storage Gadget, version: 2009/09/11
        [    1.972527] g_mass_storage gadget: userspace failed to provide iSerialNumber
        [    1.972530] g_mass_storage gadget: g_mass_storage ready
        # cat /proc/cmdline
        console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait g_mass_storage.removable=1 g_mass_storage.luns=1
        # fdisk -l
        Disk /dev/mmcblk0: 15 GB, 15931539456 bytes, 31116288 sectors
        486192 cylinders, 4 heads, 16 sectors/track
        Units: cylinders of 64 * 512 = 32768 bytes

        Device       Boot StartCHS    EndCHS        StartLBA     EndLBA    Sectors  Size Id Type
        /dev/mmcblk0p1    320,0,1     815,3,16         20480   31116287   31095808 14.8G 83 Linux
        # echo /dev/mmcblk0 > /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/gadget/lun0/file
        
Access the disk at host pc and write and umount
Host
Plug USB host cable where A-type connect with USB stick and B-type connect to bananapi and

See USB stick detection on bananapi

::

        # cat /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/mode
        b_peripheral
        # echo host > /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/mode
        [   19.231613] phy phy-1c19400.phy.0: Changing dr_mode to 1
        # [  451.961240] usb 1-1: new high-speed USB device number 2 using ehci-platform
        [  452.133893] usb-storage 1-1:1.0: USB Mass Storage device detected
        [  452.140884] scsi host0: usb-storage 1-1:1.0
        [  453.151349] scsi 0:0:0:0: Direct-Access     Generic  Flash Disk       8.07 PQ: 0 ANSI: 4
        [  453.161156] sd 0:0:0:0: [sda] 15728640 512-byte logical blocks: (8.05 GB/7.50 GiB)
        [  453.169900] sd 0:0:0:0: [sda] Write Protect is off
        [  453.175770] sd 0:0:0:0: [sda] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
        [  453.191292]  sda: sda1
        [  453.197283] sd 0:0:0:0: [sda] Attached SCSI removable disk

