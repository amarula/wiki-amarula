I.MX8MM Secure Boot using High Assurance Boot v4
################################################

Introduction
============

This tutorial describes the information and usage on how to secure boot i.MX8MM chipsets using
HABv4. The platform used in this tutorial is an Engicam Ctouch 2.0 based on i.M8M Mini
chipset.

This tutorial is an addon to an already existing `i.MX6 Secure Boot <https://wiki.amarulasolutions.com/uboot/secure_boot/imx6_habv4.html>`_ tutorial.
The boot process for i.MX 8M family (including i.MX 8MQ, i.MX 8M Mini, i.MX 8M Nano and i.MX 8M Plus)
is little different compared to older i.MX6/7 platforms which will be outlined in this tutorial.

For practical purposes and to make this tutorial more understandable, i.MX8M Mini based CTouch2.0
carrier board is used.


Why Secure Boot
===============
To prevent unauthorized software execution during the device boot sequence, there should be a
mechanism and the HABv4 secure boot feature uses digital signatures to prevent unauthorized
software execution. For instance if a malware takes control of the boot sequence, sensitive data,
services and network can be impacted.


HABv4 Secure Boot Architecture
==============================
The i.MX family of applications processors provides the High Assurance Boot (HAB) feature in the 
on-chip ROM. The ROM is responsible for loading the initial program image (U-Boot) from the boot
media and HAB enables the ROM to authenticate and/or decrypt the program image by using cryptography
operations.

The main features supported by the HABv4 are:

 - Authentication of software loaded from any boot device supported, including the Serial Download Protocol (SDP).

 - Authenticated USB download fail-over on any security failure.

 - Interface with the SNVS to guarantee the system security state.

 - Initialization of security components.

 - X.509 public key certificate support.

 - CMS signature format support.

 - 1024, 2048, 3072, and 4096 bits RSA keys length support.

 - p256, p384, p521 ECC keys support.

 - SHA-256 message digest operations accelerated by hardware.

 - Manufacturing protection private key generation in supported devices.

 - Super Root Key (SRK) revocation support.

.. image:: /images/secure_boot.png
Figure I: HABv4 Secure Boot architecture[I]

The above Figure 1 can be understood in two parts: Code signing part which does the signing of
images. The authentication part which checks whether the image to be booted is not tampered and
if the verification is successful the root of trust is passed to the next image to be booted.

.. image:: /images/secure_boot1.png
Figure II: HABv4 Secure Boot flow[II]

HABv4 authentication is based on public key cryptography using the RSA or ECDSA
algorithms in which image data(for instance u-boot binary) is signed offline using a series of
private keys. The resulting signed image data is then verified on the i.MX8M processor using the
corresponding public keys.

This key structure is known as a Public Key Infrastructure(PKI) tree. Super Root Keys, or SRK, are
components of the PKI tree. HABv4 relies on a table of the public SRKs to be hashed and placed in
fuses on the target.

The i.MX Code SigningTool (CST) is used in this guide to generate the HABv4 signatures for images
using the PKI tree data and SRK table. On the target, HABv4 evaluates the SRK table included in the
signature by hashing it and comparing the result to the SRK fuse values. If the SRK verification is
successful, the root of trust is established, and the remainder of the signature can be processed to
1authenticate the image.

The U-Boot image to be programmed into the boot media needs to be properly constructed i.e. it
must contain a proper Command Sequence File (CSF).

The CSF is a binary data structure interpreted by the HAB to guide authentication process, this is
generated by the Code Signing Tool[1]. The CSF structure contains the commands, SRK table, signatures
and certificates.

i.MX8M Boot Flow
================

The boot flow on i.MX 8M family devices are slightly different when compared with i.MX 6, i.MX 7
series device. The boot flow changes are due to the different architecture, multiple firmware and
software components required to initialize the device[I].

.. image:: /images/imx8mm_bootflow.png
Figure III: i.MX8M Boot Flow[I] 

 - NOTE: for i.MX8M mini hdmi/dp firmware is not required in the boot process

On reset, ROM code reads the efuse to determine the security configuration of the SoC and
the type of the boot device. The ROM then locates flash.bin, layout shown in Figure IV.

.. image:: /images/imx8mm_flash.png
Figure IV: i.MX8M Boot Flow[I] 

The above Figure shows 2 CSF binaries required, one per verification stage:

 - CSF SPL that is used by Boot ROM to authenticate SPL + DDR FW
   
 - CSF FIT that is used by SPL (through HAB APIs) to authenticate FIT components

The ROM code first reads the Image Vector Table(IVT) and identifies the CSF location. It verifies
and loads Second Program Loader (SPL) and DDR firmware onto OCRAM. It verifies the authenticity of
the SPL binary both in memory and flash against the signature embedded in the CSF. This can be seen
as the first stage verification. If signature verification fails, execution is not allowed to leave
the ROM for securely configured SoCs, also called “closed” devices.

For an open device (meaning the fuse related to configuring SOC is not yet programmed), even if signature
verification fails one will be able to see HAB events which will tell the programmer if the image would
pass the authentication process.

During Verification, HAB evaluates the SRK table included in the signature by hashing it and comparing
the result to the SRK fuse values. If the SRK verification is successful, this establishes the root of
trust, and the remainder of the signature can be processed to authenticate the image.

If it succeeds (or if the device is open), the ROM code goes loads and jumps to SPL. SPL initializes the
clocks, PMIC, LPDDR4 and UART. SPl then loads and verifies the rest of the components using the HAB APIs
to extend the root of trust.

A FIT image is used to package all the components rtequired for i.MX8M mini which are:

 - U-Boot binary + device tree blob (dtb)

 - ARM Trusted Firmware (ATF)
   
 - OP-TEE binary (TrustZone - optional)

Once the DDR is available, the SPL code verifies and loads all the images included in the FIT structure to
their specific execution addresses. This is the second stage and if the verification succeeds, ATF is
executed which will in turn execute U-Boot.

The HABv4 APIs can be used to extend the root of trust additionally tothe Linux Kernel and Cortex-M images
and can be authenticated at bootloader level.

i.MX8M Signed Image
====================

.. image:: /images/image_flash_mem.png


The below procedure outlines on how signed secure boot has been created with Engicam i.CoreMX8M MINI CTouch2.0 board.

Download NXP Code Signing tool
-------------------------------

::

        $ git clone https://www.nxp.com/webapp/Download?colCode=IMX_CST_TOOL_NEW
        $ tar xzf cst-3.3.1.tar.gz
        $ cd cst-3.3.1/keys

Generate PKI tree (Private keys)
--------------------------------
Create a serial file with an 8-digit content. OpenSSL uses the contents of this file for the certificate
serial numbers. 

Create key_pass.txt which contains your pass phrase that will protect the HAB code signing private keys.

::

        $ echo "42424242" > serial

        $ echo "Amarual357" > key_pass.txt
        $ echo "Amarual357" >> key_pass.txt
        $ ./hab4_pki_tree.sh


            +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            This script is a part of the Code signing tools for Freescale's

            High Assurance Boot.  It generates a basic PKI tree.  The PKI

            tree consists of one or more Super Root Keys (SRK), with each

            SRK having two subordinate keys:

                + a Command Sequence File (CSF) key

                + Image key.

            Additional keys can be added to the PKI tree but a separate

            script is available for this.  This this script assumes openssl

            is installed on your system and is included in your search

            path.  Finally, the private keys generated are password

            protectedwith the password provided by the file key_pass.txt.

            The format of the file is the password repeated twice:

                my_password

                my_password

            All private keys in the PKI tree are in PKCS #8 format will be

            protected by the same password.


            +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        Do you want to use an existing CA key (y/n)?: n

        Do you want to use Elliptic Curve Cryptography (y/n)?: n

        Enter key length in bits for PKI tree: 2048

        Enter PKI tree duration (years): 10

        How many Super Root Keys should be generated? 4

        Do you want the SRK certificates to have the CA flag set? (y/n)?: y

Private keys will generate on keys directory and corresponding Certificates are placed in the crts directory.


Generate SRK table (Public keys)
--------------------------------

::

        $ cd ../crts

        $ ../linux64/bin/srktool \

        > -h 4 \

        > -t SRK_1_2_3_4_table.bin \

        > -e SRK_1_2_3_4_fuse.bin \

        > -d sha256 \

        > -c ./SRK1_sha256_2048_65537_v3_ca_crt.pem,\

        > ./SRK2_sha256_2048_65537_v3_ca_crt.pem,\

        > ./SRK3_sha256_2048_65537_v3_ca_crt.pem,\

        > ./SRK4_sha256_2048_65537_v3_ca_crt.pem

SRK_1_2_3_4_table.bin - SRK table contents with HAB data
SRK_1_2_3_4_fuse.bin - contains SHA256 result to be burned to fuse


Build ARM Trusted firmware:
---------------------------

::

        $ git clone https://source.codeaurora.org/external/imx/imx-atf -b  imx_4.19.35_1.0.0
        $ make PLAT=imx8mm bl31

Get the ddr firmware
--------------------

::

        $ wget https://www.nxp.com/lgfiles/NMG/MAD/YOCTO/firmware-imx-8.0.bin
        $ chmod +x firmware-imx-8.0.bin
        $ ./firmware-imx-8.0

Build U-Boot with HAB enabled
-----------------------------

::

        u-boot> git clone https://github.com/sunielmahesh/u-boot-cam-imx.git -b imx_v2020.04_5.4.70_2.3.0
        
        $ export ATF_LOAD_ADDR=0x920000
        $ make imx8mm_ctouch_defconfig
        $ make ARCH=arm menuconfig

        enable CONFIG_IMX_HAB=y

        $ make CROSS_COMPILE=aarch64-buildroot-linux-gnu- flash.bin V=1


Preparing the FIT Image
-----------------------
Download imx-mkimage tool and copy ATF, ddr binaries, u-boot-nodtb.bin u-boot-spl.bin and dtb files.
After the process flash.bin is created.

::

        $ git clone https://github.com/sunielmahesh/imx-mkimage-imx8mm.git
        $ cd imx-mkimage-imx8mm/iMX8M
        $ cp ~atf/build/imx8mm/release/bl31.bin ./
        $ cp ~firmware-imx-8.0/firmware/ddr/synopsys/lpddr4*.bin ./
        $ cp ~u-boot/u-boot-nodtb.bin ./
        $ cp ~u-boot/arch/arm/dts/imx8mm-ctouch.dtb ./
        $ cp ~u-boot/spl/u-boot-spl.bin ./
        $ cp ~uboot/tools/mkimage ./mkimage_uboot

        $ make SOC=iMX8MM flash_ctouch_spl_uboot

        Compiling mkimage_imx8
        PLAT=imx8mm HDMI=no
        Compiling mkimage_imx8
        cc -O2 -Wall -std=c99 -static mkimage_imx8.c -o mkimage_imx8 -lz
        19802+0 records in
        19802+0 records out
        79208 bytes (79 kB, 77 KiB) copied, 0.0230843 s, 3.4 MB/s
        ./../scripts/pad_image.sh tee.bin
        Pad file tee.bin NOT found
        ./../scripts/pad_image.sh bl31.bin
        ./../scripts/pad_image.sh u-boot-nodtb.bin ctouch.dtb
        DEK_BLOB_LOAD_ADDR=0x40400000 TEE_LOAD_ADDR=0xbe000000 ATF_LOAD_ADDR=0x00920000 ./mkimage_fit_atf.sh ctouch.dtb > u-boot.its
        bl31.bin size:
        37216
        u-boot-nodtb.bin size:
        580784
        ctouch.dtb size:
        29936
        ./mkimage_uboot -E -p 0x3000 -f u-boot.its u-boot.itb
        u-boot.itb.tmp: Warning (unit_address_vs_reg): Node /images/uboot@1 has a unit name, but no reg property
        u-boot.itb.tmp: Warning (unit_address_vs_reg): Node /images/fdt@1 has a unit name, but no reg property
        u-boot.itb.tmp: Warning (unit_address_vs_reg): Node /images/atf@1 has a unit name, but no reg property
        u-boot.itb.tmp: Warning (unit_address_vs_reg): Node /configurations/config@1 has a unit name, but no reg property
        FIT description: Configuration to load ATF before U-Boot
        Created:         Sat Mar 13 02:04:05 2021
         Image 0 (uboot@1)
         Description:  U-Boot (64-bit)
         Created:      Sat Mar 13 02:04:05 2021
         Type:         Standalone Program
         Compression:  uncompressed
         Data Size:    580784 Bytes = 567.17 KiB = 0.55 MiB
         Architecture: AArch64
         Load Address: 0x40200000
         Entry Point:  unavailable
        Image 1 (fdt@1)
         Description:  ctouch
         Created:      Sat Mar 13 02:04:05 2021
         Type:         Flat Device Tree
         Compression:  uncompressed
         Data Size:    29936 Bytes = 29.23 KiB = 0.03 MiB
         Architecture: Unknown Architecture
        Image 2 (atf@1)
         Description:  ARM Trusted Firmware
         Created:      Sat Mar 13 02:04:05 2021
         Type:         Firmware
         Compression:  uncompressed
         Data Size:    37216 Bytes = 36.34 KiB = 0.04 MiB
         Architecture: AArch64
          OS:           Unknown OS
         Load Address: 0x00920000
         Default Configuration: 'config@1'
        Configuration 0 (config@1)
         Description:  ctouch
         Kernel:       unavailable
         Firmware:     uboot@1
         FDT:          fdt@1
         Loadables:    atf@1
        ./mkimage_imx8 -version v1 -fit -loader u-boot-spl-ddr.bin 0x7E1000 -second_loader u-boot.itb 0x40200000 0x60000 -out flash.bin
        Platform:       i.MX8M (mScale)
        ROM VERSION:    v1
        Using FIT image
        LOADER IMAGE:   u-boot-spl-ddr.bin start addr: 0x007e1000
        SECOND LOADER IMAGE:    u-boot.itb start addr: 0x40200000 offset: 0x00060000
        Output:         flash.bin
        ========= IVT HEADER [HDMI FW] =========
        header.tag:             0x0
        header.length:          0x0
        header.version:         0x0
        entry:                  0x0
        reserved1:              0x0
        dcd_ptr:                0x0
        boot_data_ptr:          0x0
        self:                   0x0
        csf:                    0x0
        reserved2:              0x0
        boot_data.start:        0x0
        boot_data.size:         0x0
        boot_data.plugin:       0x0
        ========= IVT HEADER [PLUGIN] =========
        header.tag:             0x0
        header.length:          0x0
        header.version:         0x0
        entry:                  0x0
        reserved1:              0x0
        dcd_ptr:                0x0
        boot_data_ptr:          0x0
        self:                   0x0
        csf:                    0x0
        reserved2:              0x0
        boot_data.start:        0x0
        boot_data.size:         0x0
        boot_data.plugin:       0x0
        ========= IVT HEADER [LOADER IMAGE] =========
        header.tag:             0xd1
        header.length:          0x2000
        header.version:         0x41
        entry:                  0x7e1000
        reserved1:              0x57c00
        dcd_ptr:                0x0
        boot_data_ptr:          0x7e0fe0
        self:                   0x7e0fc0
        csf:                    0x808bc0
        reserved2:              0x0
        boot_data.start:        0x7e0bc0
        boot_data.size:         0x2a060
        boot_data.plugin:       0x0
        ========= OFFSET dump =========
        Loader IMAGE:
        header_image_off       0x0
        dcd_off                0x0
        image_off              0x40
        csf_off                0x27c00
        spl hab block:         0x7e0fc0 0x0 0x27c00

        Second Loader IMAGE:
        sld_header_off         0x57c00
        sld_csf_off            0x58c20
        sld hab block:         0x401fcdc0 0x57c00 0x1020


Creating the CSF description files
----------------------------------

The CSF description file sample is provided at u-boot/doc/imx/habv4/csf_examples

There are two files since we have two stage bootloader, csf_spl.txt and csf_fit.txt. Create a directory
csf and copy both the files from u-boot/doc/imx/habv4/csf_examples.

For csf_spl.txt, in the Authenticate Data section replace Blocks with spl hab block content above:

::

        Blocks = 0x7e0fc0 0x0 0x27c00 "flash.bin"

Adjust necessary paths.

For csf_fit.txt, in the Authenticate Data section replace the first line in Blocks with sld hab block content above
and the next three lines by the output provided by the below command:

::

        imx-mkimage$ make SOC=iMX8MM print_fit_hab
        ./../scripts/dtb_check.sh imx8mm-ctouch.dtb ctouch.dtb
        Use u-boot DTB: imx8mm-ctouch.dtb
        ./../scripts/pad_image.sh tee.bin
        Pad file tee.bin NOT found
        ./../scripts/pad_image.sh bl31.bin
        ./../scripts/pad_image.sh u-boot-nodtb.bin ctouch.dtb
        u-boot-nodtb.bin + ctouch.dtb are padded to 610720
        TEE_LOAD_ADDR=0xbe000000 ATF_LOAD_ADDR=0x00920000 VERSION=v1 ./print_fit_hab.sh 0x60000 ctouch.dtb
        0x40200000 0x5AC00 0x8DCB0 
        0x4028DCB0 0xE88B0 0x74F0
        0x920000 0xEFDA0 0x9160

The resulting Authenticate Data section in csf_fit.txt should be:

::

        Blocks = 0x401fcdc0 0x57c00 0x01020 "flash.bin", \
                     0x40200000 0x5AC00 0x8DCB0 "flash.bin", \
                     0x4028DCB0 0xE88B0 0x074F0 "flash.bin", \
                     0x00920000 0xEFDA0 0x09160 "flash.bin"

Adjust necessary paths in both csf_spl.txt and csf_fit.txt.

Signing and Asembling the flash.bin binary
-------------------------------------------

::

         csf$ ../cst-3.3.1/linux64/bin/cst -i csf_spl.txt -o csf_spl.bin
         Install SRK
         Install CSFK
         Authenticate CSF
         Install key
         Authenticate data
         CSF Processed successfully and signed data available in csf_spl.bin

         csf$ ../cst-3.3.1/linux64/bin/cst -i csf_fit.txt -o csf_fit.bin
         Install SRK
         Install CSFK
         Authenticate CSF
         Install key
         Authenticate data
         CSF Processed successfully and signed data available in csf_fit.bin

         csf$ copy flash.bin from imx-mkimage/IMX8M to csf directory         
         csf$ cp flash.bin signed_flash.bin

         csf$ dd if=csf_spl.bin of=signed_flash.bin seek=$((0x27c00)) bs=1 conv=notrunc
         the seek above is csf_off

         csf$ dd if=csf_fit.bin of=signed_flash.bin seek=$((0x58c20)) bs=1 conv=notrunc
         the seek above is sld_csf_off


Flashing and Power on:
----------------------
Flash signed_flash.bin onto SD card and power-on the board

::

        $ sudo dd if=signed_flash.bin of=/dev/sdX bs=1024 seek=33
        $ sync

        U-Boot SPL 2020.04-00035-g7807920922 (Mar 12 2021 - 22:25:59 +0530)
        Can't find PMIC:PCA9450
        DDRINFO: start DRAM init
        DDRINFO: DRAM rate 3000MTS
        DDRINFO:ddrphy calibration done
        DDRINFO: ddrmix config done
        Normal Boot
        Trying to boot from MMC1
        hab fuse not enabled

        Authenticate image from DDR location 0x401fcdc0...


        U-Boot 2020.04-00035-g7807920922 (Mar 12 2021 - 22:25:59 +0530)

        CPU:   i.MX8MMQ rev1.0 1600 MHz (running at 1200 MHz)
        CPU:   Industrial temperature grade (-40C to 105C) at 38C
        Reset cause: POR
        Model: Engicam i.Core MX8M Mini C.TOUCH 2.0
        DRAM:  2 GiB
        MMC:   FSL_SDHC: 0, FSL_SDHC: 2
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial
        Out:   serial
        Err:   serial

         BuildInfo:
          - ATF da29a16
          - U-Boot 2020.04-00035-g7807920922

        switch to partitions #0, OK
        mmc0 is current device
        Net:   
        Error: ethernet@30be0000 address not set.

        Error: ethernet@30be0000 address not set.
        No ethernet found.

        Normal Boot
        Hit any key to stop autoboot:  0 
        u-boot=> 
        u-boot=> 
        u-boot=> 
        u-boot=> hab_status 

        Secure boot disabled

        HAB Configuration: 0xf0, HAB State: 0x66
        No HAB Events Found!

The above is the bootlog and hab status doesnt show any HAB events meaning the signed images generated are as per
procedure and each stage has verified the other successsully without any errors.


Programming e-fuse with SRK Hash
---------------------------------
::

        efuse dump

        $ cd ../crts

        $ hexdump -e '/4 "0x"' -e '/4 "%X""\n"' < ../cst-3.3.1/crts/SRK_1_2_3_4_fuse.bin
        0x44DF5F5B
        0xF82E1DA5
        0x4DEC9AC4
        0x8D48E35C
        0x7D33FEC0
        0xD267E7B6
        0xF80E67B4
        0xF69365A3       

The fuse table generated in the above process is what needs to be flashed to the device. U-Boot fuse
command can be used for programming eFuses.

Once the eFuses are programmed check for any errors using hab_status command. If there are no HAB events
then we can close the device implies Secure Boot is enabled.

References
----------
- 1. https://www.nxp.com/docs/en/application-note/AN4581.pdf
- 2. u-boot/doc/imx/habv4/introdcution_habv4.txt 
