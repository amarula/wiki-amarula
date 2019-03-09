Mamoj
======

This tutorial will show the detail usage of BTicino i.MX6DL Mamoj board with respective mainline projects.

Hardware Access
BSP Building
U-Boot
Linux
Buildroot
Boot
USB SDP
eMMC
Normal Mode
Falcon Mode
Secure Boot
U-Boot Accessing Peripherals
eMMC
FEC
I2C
PFUSE100
USB
Linux Accessing Peripherals
eMMC
FEC
I2C
USB
Hardware Access
BSP Building
Image building need host to ready with all necessary tools ready, refer here

U-Boot

::

        $ git clone https://github.com/openedev/u-boot-amarula.git
        $ cd u-boot
        $ git checkout bticino origin/bticino
        $ make imx6dl_mamoj_defconfig && make

Linux

::

        $ git clone https://github.com/openedev/linux-openedev
        $ cd linux-openedev
        $ git checkout bticino origin/bticino
        $ ARCH=arm make imx_v6_v7_defconfig
        $ ARCH=arm make LOADADDR=0x10008000 uImage dtbs

Buildroot
Boot
USB SDP
More info at, u-boot/doc/README.sdp

1. Clone imx_usb_loader

::

        $ git clone git://github.com/boundarydevices/imx_usb_loader.git
        $ cd imx_usb_loader
        $ make

2. Build the BSP and copy SPL, u-boot-dtb.img in imx_usb_loader directory

3. Put the board in "Serial Download Mode"

4. Plug-in USB-to-Serial and USB OTG cables to Host and Turn-on board

5. Identify VID/PID using lsusb

Bus 001 Device 010: ID 15a2:0061 Freescale Semiconductor, Inc. i.MX 6Solo/6DualLite SystemOnChip in RecoveryMode

6. Update the conf files

   imx_usb.conf

   ::

        0x15a2:0x0061, mx6_usb_rom.conf, 0x0525:0xb4a4, mx6_usb_sdp_spl.conf

  mx6_usb_rom.conf

  ::
        mx6_usb
        hid,1024,0x910000,0x10000000,512M,0x00900000,0x40000
        SPL:jump header2
         
  mx6_usb_sdp_spl.conf

  ::

        mx6_spl_sdp
        hid,uboot_header,1024,0x910000,0x10000000,512M,0x00900000,0x40000
        u-boot-dtb.img:jump header2

7. Launch the loader

::
        $ ./imx_usb

8. Identify board booting on serial

::

        U-Boot SPL 2018.03-rc3-00114-gcd9c6d25c1-dirty (Mar 08 2018 - 00:26:48 +0530)          
        Trying to boot from USB SDP                                                               
        SDP: initialize...                                                                        
        SDP: handle requests...                                                                   
        Downloading file of size 344342 to 0x177fffc0... done                                     
        Jumping to header at 0x177fffc0                                                           
        Header Tag is not an IMX image                                                            

        U-Boot 2018.03-rc3-00114-gcd9c6d25c1-dirty (Mar 08 2018 - 00:26:48 +0530)                 
        CPU:   Freescale i.MX6DL rev1.3 996 MHz (running at 792 MHz)                              
        CPU:   Extended Commercial temperature grade (-20C to 105C) at 49C                        
        Reset cause: POR                                                                          
        Model: BTicino Mamoj board                                                                
        DRAM:  512 MiB                                                                            
        MMC:   FSL_SDHC: 2                                                                        
        Loading Environment from MMC... OK                                                        
        In:    serial                                                                             
        Out:   serial
        Err:   serial
        Net:   eth0: ethernet@02188000
        Hit any key to stop autoboot:  0
        
eMMC
Normal Mode
Falcon Mode
Secure Boot
U-Boot Accessing Peripherals
eMMC
FEC
Build the BSP and Setup host tftp server from here

::

        => setenv ethaddr 00:01:02:03:04:05
        => setenv serverip 10.39.66.9
        => setenv ipaddr 10.39.66.10
        ping 10.39.66.9
        Using ethernet@02188000 device
        host 10.39.66.9 is alive
        # tftpboot $loadaddr uImage
        Using ethernet@02188000 device
        TFTP from server 10.39.66.9; our IP address is 10.39.66.10
        Filename 'uImage'.
        Load address: 0x12000000
        Loading: #################################################################
                 #################################################################
                 #################################################################
                 #################################################################
                 #################################################################
                 #################################################################
                 #################################################################
                 ####################################################
                 969.7 KiB/s
        done
        Bytes transferred = 7437704 (717d88 hex)
        # tftpboot $fdtaddr imx6dl-mamoj.dtb
        Using ethernet@02188000 device
        TFTP from server 10.39.66.9; our IP address is 10.39.66.10
        Filename 'imx6dl-mamoj.dtb'.
        Load address: 0x18000000
        Loading: ###
                 5.9 KiB/s
        done
        Bytes transferred = 32233 (7de9 hex)
        # setenv bootargs 'console=ttymxc2,115200n8 rw root=/dev/mmcblk1p3'
        # bootm $loadaddr - $fdtaddr
        ## Booting kernel from Legacy Image at 12000000 ...
           Image Name:   Linux-4.16.0-rc2-next-20180221-0
           Image Type:   ARM Linux Kernel Image (uncompressed)
           Data Size:    7437640 Bytes = 7.1 MiB
           Load Address: 10008000
           Entry Point:  10008000
        ## Flattened Device Tree blob at 18000000
           Booting using the fdt blob at 0x18000000
           Loading Kernel Image ... OK
           Loading Device Tree to 2ef6c000, end 2ef76de8 ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0
        [    0.000000] Linux version 4.16.0-rc2-next-20180221-00004-gd4b3e85ef7dc (root@localhost.localdomain) (gcc versi
        on 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #2 SMP Thu Mar 8 00:35:51 IST 2018
        
I2C

::

        => i2c bus
        Bus 2:  i2c@021a8000
        Bus 3:  i2c@021f8000
        => i2c dev 2
        Setting bus to 2
        => i2c speed 400000
        Setting bus speed to 400000 Hz
        => i2c probe
        Valid chip addresses: 20 51 53
        => i2c md 53 0xff
        00ff: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
        => i2c md 51 0xff
        00ff: a8 08 40 50 09 43 46 52 42 18 80 8e ae a9 d0 53    ..@P.CFRB......S
        => i2c dev 3
        Setting bus to 3
        => i2c speed 100000
        Setting bus speed to 100000 Hz
        => i2c probe
        Valid chip addresses: 08 40 48 4B
        => i2c md 08 0xff
        00ff: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
        
PFUSE100

::

        => pmic list
        | Name                            | Parent name         | Parent uclass @ seq
        | pfuze100@08                     | i2c@021f8000        | i2c @ 3
        => pmic dev pfuze100@08
        dev: 0 @ pfuze100@08
        => pmic dump
        Dump pmic: pfuze100@08 registers

        0x00: 10 00 00 21 00 01 3f 01 00 7f 00 00 00 00 00 81
        0x10: 00 00 3f 00 00 00 00 00 00 00 00 10 00 00 00 00
        0x20: 2b 2b 2b 08 c4 00 00 00 00 00 00 00 00 00 2b 2b
        0x30: 2b 08 c4 00 00 72 72 72 08 d4 00 00 2c 2c 2c 08
        0x40: e4 00 00 2c 2c 2c 08 e4 00 00 6f 6f 6f 08 f4 00
        0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x60: 00 00 00 00 00 00 48 00 00 00 10 06 1e 1e 17 10
        0x70: 1a 1f 00 00 00 00 00 00 00 00 00 00 00 00 00
        
USB
Linux Accessing Peripherals
eMMC
FEC
I2C
USB
