Boot Linux on Engicam i.MX6
===========================


This tutorial describe possible ways of booting Image like Linux and detailed documents are 1 2

Build the images here, and setup SD card with Single and Dual partitions here

bootm
Ramdisk

Create Single partition and Insert the SD on host and Built the images from Image Build

::

        $ cd /path/to/u-boot
        $ dd if=SPL of=/dev/mmcblk0 bs=1k seek=1
        $ dd if=u-boot-dtb.img of=/dev/mmcblk0 bs=1k seek=69
        $ cd /path/to/linux-next
        $ cp arch/arm/boot/uImage /media/jagan/rootfs
        $ cp arch/arm/boot/dts/imx6q-icore.dtb /media/jagan/rootfs
        $ cp uarm_ramdisk.image.gz /media/jagan/rootfs
        $ sync
        $ umount /dev/mmcblk0p1

JM3 Closed

Connect the Serial cable between the Starter Kit and the PC for the console (J28 is the Linux Serial console connector)

Insert the micro SD card in the board, power it up.

::

        U-Boot SPL 2017.09-00371-gcf42f39-dirty (Oct 05 2017 - 14:28:57)

        Trying to boot from MMC1

        Expected Linux image is not found. Trying to start U-boot


        U-Boot 2017.09-00371-gcf42f39-dirty (Oct 05 2017 - 14:28:57 +0530)


        CPU:   Freescale i.MX6Q rev1.2 at 792MHz

        CPU:   Industrial temperature grade (-40C to 105C) at 31C

        Reset cause: POR

        Model: Engicam i.CoreM6 Quad/Dual Starter Kit

        DRAM:  512 MiB

        MMC:   FSL_SDHC: 0

        *** Warning - bad CRC, using default environment


        No panel detected: default to Amp-WD

        Display: Amp-WD (800x480)

        In:    serial

        Out:   serial

        Err:   serial

        switch to partitions #0, OK

        mmc0 is current device

        Net:   

        Error: ethernet@02188000 address not set.

        No ethernet found.

        Hit any key to stop autoboot:  0

        icorem6qdl>

        icorem6qdl> ext4load mmc 0:1 ${loadaddr} uImage

        7085712 bytes read in 372 ms (18.2 MiB/s)

        icorem6qdl> ext4load mmc 0:1 0x83000000 uarm_ramdisk.image.gz

        691373 bytes read in 89 ms (7.4 MiB/s)

        icorem6qdl> ext4load mmc 0:1 ${fdt_addr} imx6q-icore.dtb    

        37085 bytes read in 45 ms (804.7 KiB/s)

        icorem6qdl> printenv mmcargs

        mmcargs=setenv bootargs console=${console},${baudrate} root=${mmcroot}

        icorem6qdl> printenv mmcroot

        mmcroot=/dev/mmcblk0p2 rootwait rw

        icorem6qdl> setenv mmcroot '/dev/ram rw earlycon'

        icorem6qdl> run mmcargs

        icorem6qdl> printenv bootargs

        bootargs=console=ttymxc3,115200 root=/dev/ram rw earlycon

        icorem6qdl> bootm ${loadaddr} 0x83000000 ${fdt_addr}

        ## Booting kernel from Legacy Image at 12000000 ...

           Image Name:   Linux-4.14.0-rc2-next-20170929-0

           Image Type:   ARM Linux Kernel Image (uncompressed)

           Data Size:    7085648 Bytes = 6.8 MiB

           Load Address: 10008000

           Entry Point:  10008000

           Verifying Checksum ... OK

        ## Loading init Ramdisk from Legacy Image at 13000000 ...

           Image Name:   

           Image Type:   ARM Linux RAMDisk Image (gzip compressed)

           Data Size:    691309 Bytes = 675.1 KiB

           Load Address: 00000000

           Entry Point:  00000000

           Verifying Checksum ... OK

        ## Flattened Device Tree blob at 18000000

           Booting using the fdt blob at 0x18000000

           Loading Kernel Image ... OK

           Loading Ramdisk to 2eed2000, end 2ef7ac6d ... CACHE: Misaligned operation at range [2eed2000, 2ef7ac6d]

        OK

           Using Device Tree in place at 18000000, end 1800c0dc


        Starting kernel ...


Rootfs Monolithic FIT vmlinux.bin

::
        
        $ arm-linux-gnueabi-objcopy -O binary /to/path/linux-next-imx/vmlinux vmlinux.bin

        $ gzip vmlinux.bin

FIT Input

FIT input for Linux and FDT, here and Linux, FDT and Ramdisk, here

::

        /dts-v1/;

        / {

            description = "FIT image with single Linux kernel and FDT blob";

            #address-cells = <1>;


            images {

                kernel@1 {

                    description = "i.MX6Q Linux kernel";

                    data = /incbin/("./vmlinux.bin.gz");

                    type = "kernel";

                    arch = "arm";

                    os = "linux";

                    compression = "gzip";

                    load = <0x10008000>;

                    entry = <0x10008000>;

                    hash@1 {

                        algo = "md5";

                    };

                    hash@2 {

                        algo = "sha1";

                    };

                };


                fdt@1 {

                    description = "i.CoreM6 Quad/Dual Devicetree blob";

                    data = /incbin/("./imx6q-icore.dtb");

                    type = "flat_dt";

                    arch = "arm";

                    compression = "none";

                    hash@1 {

                        algo = "md5";

                    };

                    hash@2 {

                        algo = "sha1";

                    };

                };

            };

            configurations {

                default = "conf@1";

                conf@1 {

                    description = "Boot Linux kernel and FDT blob";

                    kernel = "kernel@1";

                    fdt = "fdt@1";

                };

            };

        };

FIT Output

::

        $ /to/path/u-boot/tools/mkimage -f kernel_fdt.its fit.itb
        $ cp fit.itb /media/jagan/BOOT

FIT Boot

::

        Hit any key to stop autoboot:  0

        Booting from mmc ...

        reading boot.scr

        ** Unable to read file boot.scr **

        reading fit.itb

        6485068 bytes read in 335 ms (18.5 MiB/s)

        Booting FIT image from mmc ...

        ## Loading kernel from FIT Image at 12000000 ...

           Using 'conf@1' configuration

           Verifying Hash Integrity ... OK

           Trying 'kernel@1' kernel subimage

             Description:  i.MX6Q Linux kernel

             Type:         Kernel Image

             Compression:  gzip compressed

             Data Start:   0x120000e4

             Data Size:    6446108 Bytes = 6.1 MiB

             Architecture: ARM

             OS:           Linux

             Load Address: 0x10008000

             Entry Point:  0x10008000

             Hash algo:    md5

             Hash value:   1580c77b97e137d81d4ad804fba3065c

             Hash algo:    sha1

             Hash value:   e699babcc853bf0be519eedbba173e5795a8941b

           Verifying Hash Integrity ... md5+ sha1+ OK

        ## Loading fdt from FIT Image at 12000000 ...

           Using 'conf@1' configuration

           Trying 'fdt@1' fdt subimage

             Description:  i.CoreM6 Quad/Dual Devicetree blob

             Type:         Flat Device Tree

             Compression:  uncompressed

             Data Start:   0x12625e38

             Data Size:    37081 Bytes = 36.2 KiB

             Architecture: ARM

             Hash algo:    md5

             Hash value:   7e01cb60cef8d98d018aaf0d4455b970

             Hash algo:    sha1

             Hash value:   4ecef92ce375160d11ee7363aebc8058c1e02878

           Verifying Hash Integrity ... md5+ sha1+ OK

           Booting using the fdt blob at 0x12625e38

           Uncompressing Kernel Image ... OK

           Using Device Tree in place at 12625e38, end 12631f10


        Starting kernel ...


Verified Boot
vmlinux.bin

::

        $ arm-linux-gnueabi-objcopy -O binary vmlinux vmlinux.bin

        $ gzip vmlinux.bin

        $ cp imx6q-icore-rqs.dtb imx6q-icore-rqs-pubkey.dtb

FIT input

::

        kernel_fdt.its

        /* Simple U-Boot uImage source file containing a single kernel and FDT blob */

        /dts-v1/;

        / {

            description = "Verified RSA image with single Linux kernel and FDT blob";

            #address-cells = <1>;

            images {

                kernel@1 {

                    description = "i.MX6 Linux kernel";

                    data = /incbin/("./vmlinux.bin.gz");

                    type = "kernel";

                    arch = "arm";

                    os = "linux";

                    compression = "gzip";

                    load = <0x10008000>;

                    entry = <0x10008000>;

                    hash@1 {

                        algo = "md5";

                    };

                    hash@2 {

                        algo = "sha1";

                    };

                    signature@1 {

                        algo = "sha1,rsa2048";

                        key-name-hint = "eng";

                    };

                };

                fdt@1 {

                    description = "Engicam i.CoreM6 Quad/Dual RQS Starter Kit Devicetree blob";

                    data = /incbin/("./imx6q-icore-rqs.dtb");

                    type = "flat_dt";

                    arch = "arm";

                    compression = "none";

                    hash@1 {

                        algo = "md5";

                    };

                    hash@2 {

                        algo = "sha1";

                    };

                    signature@1 {

                        algo = "sha1,rsa2048";

                        key-name-hint = "eng";

                    };

                };

            };

            configurations {

                default = "conf@1";

                conf@1 {

                    description = "Boot Linux kernel with FDT blob";

                    kernel = "kernel@1";

                    fdt = "fdt@1";

                };

            };

        };

RSA key

::

        - Create RSA key pair
        $ mkdir mykeys
        $ openssl genrsa -F4 -out mykeys/eng.key 2048

        - Create a certificate contains public key

        $ openssl req  -batch -new -x509 -key mykeys/eng.key -out mykeys/eng.crt

FIT output

::

        $ ./mkimage -f kernel_fdt.its -K imx6q-icore-rqs-pubkey.dtb -k mykeys/ -r fit.itb

        Build U-Boot Public key

        $ .make DEV_TREE_BIN=../imx6q-icore-rqs-pubkey.dtb

        VerifiedBoot

        U-Boot SPL 2017.01-rc2-00010-gb42d823 (Dec 21 2016 - 11:13:46)
        Trying to boot from MMC1

        U-Boot 2017.01-rc2-00010-gb42d823 (Dec 21 2016 - 11:13:46 +0100)

        CPU:   Freescale i.MX6D rev1.2 at 792 MHz
        Reset cause: POR
        Model: Engicam i.CoreM6 Quad/Dual RQS Starter Kit
        DRAM:  512 MiB
        MMC:   FSL_SDHC: 0
        *** Warning - bad CRC, using default environment

        In:    serial
        Out:   serial
        Err:   serial
        Net:   No ethernet found.
        Hit any key to stop autoboot:  0 
        switch to partitions #0, OK
        mmc0 is current device
        reading boot.scr
        ** Unable to read file boot.scr **
        reading fit.itb
        6167494 bytes read in 335 ms (17.6 MiB/s)
        Booting FIT image from mmc ...
        ## Loading kernel from FIT Image at 12000000 ...
           Using 'conf@1' configuration
           Verifying Hash Integrity ... OK
           Trying 'kernel@1' kernel subimage
             Description:  i.MX6 Linux kernel
             Type:         Kernel Image
             Compression:  gzip compressed
             Data Start:   0x120000f0
             Data Size:    6130148 Bytes = 5.8 MiB
             Architecture: ARM
             OS:           Linux
             Load Address: 0x10008000
             Entry Point:  0x10008000
             Hash algo:    md5
             Hash value:   b975a202ea2963c53c53f527329930cd
             Hash algo:    sha1
             Hash value:   78b93fe404b795de8c837af27d67f4df9b96083a
             Sign algo:    sha1,rsa2048:eng
             Sign value:   4288ce2c7380a90b7b7b9c000760f086fe67560d16fb5ea85bc792ff3ed70e381956bbff99c514213e00e3d21838650ada0eb68439e253ef493e3e0098e0d47109d3e
           Verifying Hash Integrity ... md5+ sha1+ sha1,rsa2048:eng- OK
        ## Loading fdt from FIT Image at 12000000 ...
           Using 'conf@1' configuration
           Trying 'fdt@1' fdt subimage
             Description:  Engicam i.CoreM6 Quad/Dual RQS Starter Kit Devicetree blob
             Type:         Flat Device Tree
             Compression:  uncompressed
             Data Start:   0x125d8dbc
             Data Size:    35298 Bytes = 34.5 KiB
             Architecture: ARM
             Hash algo:    md5
             Hash value:   4371a4dfe55127c2fda8a9feb4d3b313
             Hash algo:    sha1
             Hash value:   e34a9326b5e7fd43557753ef980fe67326f82ea1
             Sign algo:    sha1,rsa2048:eng
             Sign value:   94cebd60a6ff2e123ed763760b88c026b74b12eb9c37a97d73eec1a25e01d6e29284f393c5ca20951a605378bf8b547bdc0ce0aae16e069e6db0c5af7f00d4cfc6c94
           Verifying Hash Integrity ... md5+ sha1+ sha1,rsa2048:eng- OK
           Booting using the fdt blob at 0x125d8dbc
           Uncompressing Kernel Image ... OK
           Using Device Tree in place at 125d8dbc, end 125e479d

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0
        [    0.000000] Linux version 4.9.0-next-20161216-dirty (root@jagan-XPS-13-9350) (gcc version 4.7.1 20120402 (prerelease) (crosstool-NG linaro-1.13.1-206
        [    0.000000] CPU: ARMv7 Processor [412fc09a] revision 10 (ARMv7), cr=10c5387d
        [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
        [    0.000000] OF: fdt:Machine model: Engicam i.CoreM6 Quad SOM
        [    0.000000] cma: Reserved 64 MiB at 0x2c000000
        [    0.000000] Memory policy: Data cache writealloc
        [    0.000000] percpu: Embedded 14 pages/cpu @dbb9d000 s26816 r8192 d22336 u57344
        [    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 130048
        [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/mmcblk0p2 rootwait rw
        [    0.000000] PID hash table entries: 2048 (order: 1, 8192 bytes)
        [    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)

        [    3.750068]   #0: imx-audio-sgtl5000
        [    3.765128] EXT4-fs (mmcblk0p2): couldn't mount as ext3 due to feature incompatibilities
        [    3.807473] usb 1-1: device descriptor read/64, error -71
        [    4.020338] EXT4-fs (mmcblk0p2): mounted filesystem with ordered data mode. Opts: (null)
        [    4.028685] VFS: Mounted root (ext4 filesystem) on device 179:2.
        [    4.038301] devtmpfs: mounted
        [    4.044169] Freeing unused kernel memory: 1024K
        INIT: [    4.177458] usb 1-1: device descriptor read/64, error -71
        version 2.88 booting
        [    4.437640] usb 1-1: new full-speed USB device number 3 using ci_hdrc
        mount: mount point /mnt/.psplash does not exist
        [    4.677537] usb 1-1: device descriptor read/64, error -71
        Starting udev

