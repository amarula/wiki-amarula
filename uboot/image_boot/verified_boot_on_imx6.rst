Verified Boot on i.MX6
========================

Create vmlinux.bin

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

RSA key generation

::

        - Create RSA key pair
        $ mkdir mykeys
        $ openssl genrsa -F4 -out mykeys/eng.key 2048

        - Create a certificate contains public key

        $ openssl req  -batch -new -x509 -key mykeys/eng.key -out mykeys/eng.crt

FIT output

::

        $ ./mkimage -f kernel_fdt.its -K imx6q-icore-rqs-pubkey.dtb -k mykeys/ -r fit.itb

Build U-Boot with Public key

::

        $ .make DEV_TREE_BIN=../imx6q-icore-rqs-pubkey.dtb

Boot VerifiedBoot

::

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

