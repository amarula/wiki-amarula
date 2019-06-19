Verified Boot on SUNXI64
########################

U-Boot supports an image verification method called "Verified Boot". This tutorial will show the details of verified-boot on SUNXI64 platform with Orangepi A64 board.

See here for more documentation of verified-boot - doc/uImage.FIT directory

Generate RSA key to sign
************************
::

        # Create RSA key pair
        $ mkdir keys
        $ openssl genpkey -algorithm RSA -out keys/dev.key -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537

        # Create a certificate contains public key
        $ openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt

Build Linux
***********
See this `page <https://wiki.amarulasolutions.com/bsp/sunxi/a64/opi-win.html#linux>`_ for building linux

FIT Input
*********
`kernel_fdt.its <https://downloads.amarulasolutions.com/public/linux_image_boot_sunxi/kernel_fdt.its>`_

::

        /dts-v1/;

        / {

            description = "FIT image with single Linux kernel, FDT blob";

            #address-cells = <1>;


            images {

                kernel@0 {

                    description = "ARM64 Linux kernel";

                    data = /incbin/("./Image.gz");

                    type = "kernel";

                    arch = "arm64";

                    os = "linux";

                    compression = "gzip";

                    load = <0x50080000>;

                    entry = <0x50080000>;

                    hash@1 {

                        algo = "sha256";

                    };

                };


                fdt@0 {

                    description = "Orangepi Win/Win+ Devicetree blob";

                    data = /incbin/("./sun50i-a64-orangepi-win.dtb");

                    type = "flat_dt";

                    arch = "arm64";

                    compression = "none";

                    hash@1 {

                        algo = "sha256";

                    };

                };

            };


            configurations {

                default = "conf@0";


                conf@0 {

                    description = "Boot Linux kernel, FDT blob";

                    kernel = "kernel@0";

                    fdt = "fdt@0";

                    signature@0 {

                        algo = "sha256,rsa2048";

                        key-name-hint = "dev";

                        sign-images = "kernel", "fdt";

                    };

                };

            };

        };

You need to change the two '/incbin/' lines, depending on the location of your kernel image, devicetree blob.  The "load" and "entry" properties also need to be adjusted if you want to change the physical placement of the kernel.

The "key-name-hint" must specify the key name you have created in the "Generate RSA key to sign" step

Build U-Boot
************
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make orangepi_win_defconfig
        $ make menuconfig
        [ enable CONFIG_FIT, CONFIG_FIT_SIGNATURE and CONFIG_FIT_VERBOSE ]
        $ make

FIT Output
**********
::

        $ tools/mkimage -f kernel_fdt.its -k keys -K dts/dt.dtb -r -F fitImage

            => k options for specifying keys directory from "Generate RSA key to sign" step
            => dts/dt.dtb from U-Boot
            => The public key needed for the run-time verification is stored in "dts/dt.dtb"

Build Signed-U-Boot
*******************
"dt.dtb" has been updated in above step, you need to re-compile the U-Boot.
::

        $ make

The re-compiled "u-boot.bin" is appended with DTB that contains the public key.

Verified Boot
*************
::

        U-Boot SPL 2017.11-rc4-dirty (Nov 08 2017 - 00:11:54)

        DRAM: 1024 MiB

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


        U-Boot 2017.11-rc4-dirty (Nov 08 2017 - 00:11:54 +0530) Allwinner Technology


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

        switch to partitions #0, OK

        mmc0 is current device

        Scanning mmc 0:1...

        Found /boot/extlinux/extlinux.conf

        Retrieving file: /boot/extlinux/extlinux.conf

        185 bytes read in 274 ms (0 Bytes/s)

        1:      Opi Win/Win+

        Retrieving file: /boot/fitImage

        6895614 bytes read in 607 ms (10.8 MiB/s)

        append: console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait

        ## Loading kernel from FIT Image at 40080000 ...

           Using 'conf@0' configuration

           Verifying Hash Integrity ... OK

           Trying 'kernel@0' kernel subimage

             Description:  ARM64 Linux kernel

             Type:         Kernel Image

             Compression:  gzip compressed

             Data Start:   0x400800e4

             Data Size:    6884659 Bytes = 6.6 MiB

             Architecture: AArch64

             OS:           Linux

             Load Address: 0x50080000

             Entry Point:  0x50080000

             Hash algo:    sha256

             Hash value:   6808fe51ea3c15f31c4510d2701d4707b56d20213c9da05bce79fb53bf108f1a

           Verifying Hash Integrity ... sha256+ OK

        ## Loading fdt from FIT Image at 40080000 ...

           Using 'conf@0' configuration

           Trying 'fdt@0' fdt subimage

             Description:  Orangepi Win/Win+ Devicetree blob

             Type:         Flat Device Tree

             Compression:  uncompressed

             Data Start:   0x40710f24

             Data Size:    9032 Bytes = 8.8 KiB

             Architecture: AArch64

             Hash algo:    sha256

             Hash value:   ca3d874cd10466633ff133cc0156828d48c8efb96987fa45f885761d22a25dc1

           Verifying Hash Integrity ... sha256+ OK

           Booting using the fdt blob at 0x40710f24

           Uncompressing Kernel Image ... OK

           Loading Device Tree to 0000000049ffa000, end 0000000049fff347 ... OK

        Cannot setup simplefb: node not found


        Starting kernel ...


        [    0.000000] Booting Linux on physical CPU 0x0
