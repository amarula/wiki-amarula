Measurement
============

Tool
Procedure
Normal mode
Falcon mode
Vyasa-RK3288 Timings
i.CoreM6 RQS Duallite/Solo
Normal Mode
mmc Falcon Mode
emmc Falcon Mode
Is.IoT eMMC
mmc Normal
Tool
Grabserial - Get log and timestamp console output

::

        bash> git clone https://github.com/tbird20d/grabserialbash> sudo grabserial/grabserial /usr/local bin
        bash> grabserial

Procedure
Normal mode

::

        bash> grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t -m "Starting kernel.*"
        Opening serial port /dev/ttyUSB0115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Matching pattern 'Starting kernel.*' to set base time
        Use Control-C to stop...
        [0.000002 0.000002]
        [0.001344 0.001342] U-Boot TPL 2017.09-rc2-13373-g2cffd0d-dirty (Aug 31 2017 - 20:41:14)
        [0.005975 0.004631] Trying to boot from BOOTROM
        [0.008394 0.002419] Returning to boot ROM...
        [0.216735 0.208341]
        [0.217195 0.000460] U-Boot SPL 2017.09-rc2-13373-g2cffd0d-dirty (Aug 31 2017 - 20:41:14)
        [0.223097 0.005902] Trying to boot from MMC1[0.262093 0.038996] Expected Linux image is not found. Trying to start U-boot
        [0.436129 0.174036]
        [0.436416 0.000287]
        [0.436696 0.000280] U-Boot 2017.09-rc2-13373-g2cffd0d-dirty (Aug 31 2017 - 20:41:14 +0530)
        [0.442273 0.005577][0.442369 0.000096] Model: Amarula Vyasa-RK3288
        [0.444854 0.002485] DRAM:  2 GiB
        [0.479422 0.034568] MMC:   dwmmc@ff0c0000: 1
        [0.627295 0.147873] *** Warning - bad CRC, using default environment
        [0.631527 0.004232]
        [0.635980 0.004453] In:    serial@ff690000
        [0.637982 0.002002] Out:   serial@ff690000
        [0.640004 0.002022] Err:   serial@ff690000
        [0.642244 0.002240] Model: Amarula Vyasa-RK3288
        [0.644783 0.002539] Net:   Net Initialization Skipped
        [0.647824 0.003041] No ethernet found.
        [0.651954 0.004130] Hit any key to stop autoboot:  0
        [0.772503 0.120549] switch to partitions #0, OK
        [0.774802 0.002299] mmc1 is current device
        [1.069762 0.294960] Scanning mmc 1:1...
        [1.312386 0.242624] Found /boot/extlinux/extlinux.conf
        [1.315209 0.002823] Retrieving file: /boot/extlinux/extlinux.conf
        [1.353460 0.038251] 145 bytes read in 28 ms (4.9 KiB/s)
        [1.356412 0.002952] 1:    Vyasa Linux-4.13
        [1.358237 0.001825] Retrieving file: /boot/uImage
        [1.740753 0.382516] 7836344 bytes read in 375 ms (19.9 MiB/s)
        [1.744302 0.003549] append: console=ttyS2,115200n8 root=/dev/mmcblk0p1 rootwait quiet
        [1.750086 0.005784] Retrieving file: /boot/rk3288-vyasa.dtb
        [1.786952 0.036866] 36291 bytes read in 28 ms (1.2 MiB/s)
        [1.789950 0.002998] ## Booting kernel from Legacy Image at 02000000 ...
        [1.794524 0.004574]    Image Name:   Linux-4.13.0-rc4-next-20170810-0
        [1.799040 0.004516]    Image Type:   ARM Linux Kernel Image (uncompressed)
        [1.803818 0.004778]    Data Size:    7836280 Bytes = 7.5 MiB
        [1.807426 0.003608]    Load Address: 02000000
        [1.809776 0.002350]    Entry Point:  02000000
        [1.812097 0.002321]    Verifying Checksum ... OK
        [1.945372 0.133275] ## Flattened Device Tree blob at 01f00000
        [1.948106 0.002734]    Booting using the fdt blob at 0x1f00000
        [1.951715 0.003609]    Loading Kernel Image ... OK
        [1.968363 0.016648]    Loading Device Tree to 0fff4000, end 0ffffdc2 ... OK
        [1.974709 0.006346]
        [1.974911 0.000202] Starting kernel ...
        [0.002243 0.002243]
        [1.273396 1.271153] [    0.090111] dmi: Firmware registration failed.
        [1.617881 0.344485] [    0.581926] EXT4-fs (mmcblk0p1): couldn't mount as ext3 due to feature incompatibilities
        [1.627592 0.009711] [    0.592177] EXT4-fs (mmcblk0p1): couldn't mount as ext2 due to feature incompatibilities
        [4.596400 2.968808] Starting logging: OK
        [4.610216 0.013816] Initializing random number generator... done.
        [4.622379 0.012163] Starting network: OK
        [4.746329 0.123950]
        [4.748163 0.001834] Welcome to VYASA RK3288!
        [4.750725 0.002562] vyasa-rk3288 login:

Falcon mode

::

        bash> grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t -m "Starting kernel.*"
        Opening serial port /dev/ttyUSB0115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Matching pattern 'Starting kernel.*' to set base time
        Use Control-C to stop...
        [0.000001 0.000001]
        [0.001135 0.001134] U-Boot TPL 2017.09-rc2-13373-g2cffd0d-dirty (Aug 31 2017 - 20:41:14)
        [0.005690 0.004555] Trying to boot from BOOTROM
        [0.008221 0.002531] Returning to boot ROM...
        [0.196488 0.188267]
        [0.196704 0.000216] U-Boot SPL 2017.09-rc2-13373-g2cffd0d-dirty (Aug 31 2017 - 20:41:14)
        [0.202759 0.006055] Trying to boot from MMC1
        [1.879613 1.676854] [    0.090151] dmi: Firmware registration failed.
        [2.287880 0.408267] [    0.645755] EXT4-fs (mmcblk0p1): couldn't mount as ext3 due to feature incompatibilities
        [2.301935 0.014055] [    0.660209] EXT4-fs (mmcblk0p1): couldn't mount as ext2 due to feature incompatibilities
        [2.425052 0.123117] Starting logging: OK
        [2.440868 0.015816] Initializing random number generator... done.
        [2.452302 0.011434] Starting network: OK
        [2.580451 0.128149]
        [2.584354 0.003903] Welcome to VYASA RK3288!
        [2.586697 0.002343] vyasa-rk3288 login:
        
Vyasa-RK3288 Timings

==============   ================== ============= ======================= =======================================
Mode of Boot      Bootloader (sec)   Linux (sec)   Total Boot time (sec)   Remarks
==============   ================== ============= ======================= =======================================
Normal Boot        1.974909          2.775814       4.753287 
Falcon Boot        0.208814          2.380226       2.58904                ~54.56% reduction in boot time compared to Normal mode boot
==============   ================== ============= ======================= =======================================

i.CoreM6 RQS Duallite/Solo

=================   ====================== =============
Mode of Boot         Total Boot Time (sec)  Remarks 
=================   ====================== =============
Normal Boot           3.582790  
mmc Falcon Boot       4.436016
emmc Falcon Boot      3.358925     
=================   ====================== =============

Normal Mode

::

        bash> grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t 
        Opening serial port /dev/ttyUSB0
        115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Use Control-C to stop...
        [0.000001 0.000001] 
        [0.463108 0.463107] U-Boot SPL 2018.03-rc3-00088-gd231182441d2-dirty (Mar 09 2018 - 15:33:18 +0530)
        [0.494895 0.031787] Trying to boot from MMC1
        [0.648928 0.154033] Expected Linux image is not found. Trying to start U-boot
        [0.809112 0.160184] 
        [0.809201 0.000089] 
        [0.809261 0.000060] U-Boot 2018.03-rc3-00088-gd231182441d2-dirty (Mar 09 2018 - 15:33:18 +0530)
        [0.814423 0.005162] 
        [0.814462 0.000039] CPU:   Freescale i.MX6DL rev1.3 at 792 MHz
        [0.815548 0.001086] Reset cause: POR
        [0.820317 0.004769] Model: Engicam i.CoreM6 DualLite/Solo RQS Starter Kit
        [0.822997 0.002680] DRAM:  512 MiB
        [0.872900 0.049903] MMC:   FSL_SDHC: 1, FSL_SDHC: 2
        [0.902445 0.029545] Loading Environment from MMC... OK
        [1.002036 0.099591] In:    serial
        [1.002604 0.000568] Out:   serial
        [1.003187 0.000583] Err:   serial
        [1.088991 0.085804] switch to partitions #0, OK
        [1.089517 0.000526] mmc1 is current device
        [1.089980 0.000463] Net:   No ethernet found.
        [1.097563 0.007583] Hit any key to stop autoboot:  0 
        [1.098690 0.001127] Booting from mmc ...
        [1.196918 0.098228] ** Unable to read file boot.scr **
        [1.209813 0.012895] ** Unable to read file fit.itb **
        [1.547007 0.337194] 6560488 bytes read in 329 ms (19 MiB/s)
        [1.573893 0.026886] 36829 bytes read in 16 ms (2.2 MiB/s)
        [1.574753 0.000860] ## Booting kernel from Legacy Image at 12000000 ...
        [1.579472 0.004719]    Image Name:   Linux-4.16.0-rc1-next-20180215-0
        [1.585049 0.005577]    Image Type:   ARM Linux Kernel Image (uncompressed)
        [1.589958 0.004909]    Data Size:    6560424 Bytes = 6.3 MiB
        [1.590683 0.000725]    Load Address: 10008000
        [1.593919 0.003236]    Entry Point:  10008000
        [1.594299 0.000380]    Verifying Checksum ... OK
        [1.673030 0.078731] ## Flattened Device Tree blob at 18000000
        [1.673681 0.000651]    Booting using the fdt blob at 0x18000000
        [1.678218 0.004537]    Loading Kernel Image ... OK
        [1.715904 0.037686]    Using Device Tree in place at 18000000, end 1800bfdc
        [1.716830 0.000926] 
        [1.716849 0.000019] Starting kernel ...
        [1.719020 0.002171] 
        [2.471013 0.751993] [    0.332029] fec 2188000.ethernet (unnamed net_device) (uninitialized): Invalid MAC address: 00:00:00:00:00:00
        [2.481794 0.010781] [    0.343118] mdio_bus 2188000.ethernet-1: MDIO device at address 0 is missing.
        [2.962948 0.481154] [    0.824062] EXT4-fs (mmcblk1p2): couldn't mount as ext3 due to feature incompatibilities
        [3.271957 0.309009] Starting logging: OK
        [3.324930 0.052973] Initializing random number generator... done.
        [3.367783 0.042853] Starting network: OK
        [3.561869 0.194086] 
        [3.579876 0.018007] Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo RQS Starter Kit
        [3.582790 0.002914] buildroot login:

mmc Falcon Mode

::

        $ grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t 
        Opening serial port /dev/ttyUSB0
        115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Use Control-C to stop...
        [0.000000 0.000000] 
        [0.000057 0.000057] U-Boot SPL 2018.03-rc3-00088-gd231182441d2-dirty (Mar 09 2018 - 11:37:43 +0530)
        [0.031834 0.031777] Trying to boot from MMC1
        [3.384035 3.352201] [    0.328707] fec 2188000.ethernet (unnamed net_device) (uninitialized): Invalid MAC address: 00:00:00:00:00:00
        [3.391705 0.007670] [    0.339778] mdio_bus 2188000.ethernet-1: MDIO device at address 0 is missing.
        [4.127913 0.736208] Starting logging: OK
        [4.185913 0.058000] Initializing random number generator... done.
        [4.223928 0.038015] Starting network: OK
        [4.415099 0.191171] 
        [4.432932 0.017833] Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo RQS Starter Kit
        [4.436016 0.003084] buildroot login:

emmc Falcon Mode

::

        bash> grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t 
        Opening serial port /dev/ttyUSB0
        115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Use Control-C to stop...
        [0.000001 0.000001] 
        [0.655035 0.655034] U-Boot SPL 2018.03-rc3-00088-gd231182441d2-dirty (Mar 09 2018 - 15:33:18 +0530)
        [0.686997 0.031962] Trying to boot from MMC2
        [1.870018 1.183021] [ 0.326646] fec 2188000.ethernet (unnamed net_device) (uninitialized): Invalid MAC address: 00:00:00:00:00:00
        [1.878300 0.008282] [ 0.337702] mdio_bus 2188000.ethernet-1: MDIO device at address 0 is missing.
        [3.088918 1.210618] Starting logging: OK
        [3.142994 0.054076] [ 1.599852] EXT2-fs (mmcblk2p1): error: ext2_lookup: deleted inode referenced: 95087
        [3.150190 0.007196] read-only file system detected...done
        [3.163792 0.013602] Starting network: OK
        [3.346881 0.183089] 
        [3.355940 0.009059] Welcome to Engicam i.CoreM6 Quad/Dual/DualLite/Solo RQS Starter Kit
        [3.358925 0.002985] buildroot login:


Is.IoT eMMC
mmc Normal	
3.714112

mmc Falcon	

emmc Falcon	

Nand	
mmc Normal

::

        $ sudo grabserial -v -d /dev/ttyUSB0 -b 115200 -w 8 -p N -s 1 -e 30 -t 
        Opening serial port /dev/ttyUSB0
        115200:8N1:xonxoff=0:rtscts=0
        Program will end in 30 seconds
        Printing timing information for each line
        Use Control-C to stop...
        [0.000000 0.000000] - 19:13:25 +0530)
        [0.013855 0.013855] Trying to boot from MMC1
        [0.220067 0.206212] 
        [0.220117 0.000050] 
        [0.220146 0.000029] U-Boot 2018.03-rc3-00088-gd231182441d2-dirty (Mar 13 2018 - 19:13:25 +0530)
        [0.226245 0.006099] 
        [0.226272 0.000027] CPU: Freescale i.MX6UL rev1.1 528 MHz (running at 396 MHz)
        [0.232175 0.005903] CPU: Industrial temperature grade (-40C to 105C) at 41C
        [0.258167 0.025992] Reset cause: POR
        [0.258616 0.000449] Model: Engicam Is.IoT MX6UL eMMC Starterkit
        [0.261050 0.002434] DRAM: 128 MiB
        [0.301016 0.039966] MMC: FSL_SDHC: 0, FSL_SDHC: 1
        [0.337436 0.036420] Loading Environment from MMC... *** Warning - bad CRC, using default environment
        [0.455263 0.117827] 
        [0.466979 0.011716] Failed (-5)
        [0.467455 0.000476] In: serial
        [0.467939 0.000484] Out: serial
        [0.468417 0.000478] Err: serial
        [0.538150 0.069733] switch to partitions #0, OK
        [0.539125 0.000975] mmc0 is current device
        [0.539859 0.000734] Net: No ethernet found.
        [0.551962 0.012103] Hit any key to stop autoboot: 0 
        [0.553081 0.001119] Booting from mmc ...
        [0.628995 0.075914] ** Unable to read file boot.scr **
        [0.642894 0.013899] ** Unable to read file fit.itb **
        [0.988019 0.345125] 6875712 bytes read in 337 ms (19.5 MiB/s)
        [1.014014 0.025995] 20839 bytes read in 16 ms (1.2 MiB/s)
        [1.014736 0.000722] ## Booting kernel from Legacy Image at 82000000 ...
        [1.019656 0.004920] Image Name: Linux-4.11.5
        [1.020205 0.000549] Image Type: ARM Linux Kernel Image (uncompressed)
        [1.025803 0.005598] Data Size: 6875648 Bytes = 6.6 MiB
        [1.030385 0.004582] Load Address: 80008000
        [1.030872 0.000487] Entry Point: 80008000
        [1.035195 0.004323] Verifying Checksum ... OK
        [1.200143 0.164948] ## Flattened Device Tree blob at 87800000
        [1.200792 0.000649] Booting using the fdt blob at 0x87800000
        [1.205454 0.004662] Loading Kernel Image ... OK
        [1.224963 0.019509] Using Device Tree in place at 87800000, end 87808166
        [1.226014 0.001051] 
        [1.226036 0.000022] Starting kernel ...
        [1.228339 0.002303] 
        [2.077080 0.848741] [ 0.008752] /cpus/cpu@0 missing clock-frequency property
        [2.517077 0.439997] [ 0.897731] cpu cpu0: dev_pm_opp_get_opp_count: OPP table not found (-19)
        [2.673071 0.155994] [ 1.053370] EXT4-fs (mmcblk0p2): couldn't mount as ext3 due to feature incompatibilities
        [3.188012 0.514941] Starting logging: OK
        [3.306131 0.118119] Initializing random number generator... done.
        [3.437959 0.131828] Starting network: OK
        [3.692050 0.254091] 
        [3.709005 0.016955] Welcome to Engicam Is.IoT eMMC Starter Kit
        [3.714112 0.005107] buildroot login:



