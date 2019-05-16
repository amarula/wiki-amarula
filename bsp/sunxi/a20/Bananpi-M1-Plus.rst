Bananapi M1 Plus
################
This tutorial will show the details of Bananapi M1 board mainline support and other needed details, for more information about `hardware <http://www.banana-pi.org/m1.html>`_ and `linux-sunxi <http://linux-sunxi.org/LeMaker_Banana_Pi>`_


BSP Build
*********

Image building need host to ready with all necessary tools ready, refer `here <https://wiki.amarulasolutions.com/uboot/tools.html#arm>`_

U-Boot
======
::

   $ git clone git://git.denx.de/u-boot.git
   $ cd u-boot
   $ make make Bananapi_defconfig
   $ make 

Linux
=====
::

   $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git

   $ cd linux-next
   $ make mrproper
   $ ARCH=arm sunxi_defconfig
   $ ARCH=arm make -j 4 zImage dtbs

SD Boot
*******

FEL/USB Boot
************
More information `here <http://linux-sunxi.org/FEL/USBBoot>`_ and build the fel tools from `here <https://wiki.amarulasolutions.com/uboot/tools.html#sunxi>`_

Insert SD card from and Press K3 located between the HDMI and USB host connectors and Power-on

Enter FEL
==========

::

   # sunxi-fel version
   ERROR: Allwinner USB FEL device not found!
   # sunxi-fel version
   AWUSBFEX soc=00001651(A20) 00000001 ver=0001 44 08 scratchpad=00007e00 00000000 00000000

Boot Linux
==========

From Host, get the boot.scr from `here <https://wiki.amarulasolutions.com/uboot/tools.html#boot32-fel-scr>`_

::

   # sunxi-fel -v uboot /path/to/u-boot-sunxi-with-spl.bin \
   > write 0x42000000 /path/to/linux-next/arch/arm/boot/zImage \
   > write 0x43000000 /path/to/linux-next/arch/arm/boot/dts/sun7i-a20-bananapi.dtb \
   > write 0x43000000 boot.scr
   Stack pointers: sp_irq=0x00002000, sp=0x00005E08
   Reading the MMU translation table from 0x00020000
   Disabling I-cache, MMU and branch prediction... done.
   => Executing the SPL... done.
   Setting write-combine mapping for DRAM.
   Setting cached mapping for BROM.
   Writing back the MMU translation table.
   Enabling I-cache, MMU and branch prediction... done.
   Writing image "U-Boot 2017.11-00063-gfb344e3 fo", 376540 bytes @ 0x4A000000.
   Passing boot info via sunxi SPL: script address = 0x43000000, uEnv length = 0
   Starting U-Boot (0x4A000000).

From Target UART

::

   U-Boot SPL 2017.11-00063-gfb344e3 (Nov 24 2017 - 12:40:59)

   DRAM: 1024 MiB

   CPU: 912000000Hz, AXI/AHB/APB: 3/2/2

   Trying to boot from FEL

   U-Boot 2017.11-00063-gfb344e3 (Nov 24 2017 - 12:40:59 +0530) Allwinner Technology

   CPU:   Allwinner A20 (SUN7I)

   Model: LeMaker Banana Pi

   I2C:   ready

   DRAM:  1 GiB

   MMC:   SUNXI SD/MMC: 0

   *** Warning - bad CRC, using default environment


   Setting up a 720x576i composite-pal console (overscan 32x20)

   In:    serial

   Out:   vga

   Err:   vga

   SCSI:  SATA link 0 timeout.

   AHCI 0001.0100 32 slots 1 ports 3 Gbps 0x1 impl SATA mode

   flags: ncq stag pm led clo only pmp pio slum part ccc apst

   Net:   eth0: ethernet@01c50000

   starting USB...
   USB0:   USB EHCI 1.00
   USB1:   USB OHCI 1.0
   USB2:   USB EHCI 1.0
   USB3:   USB OHCI 1.0
   scanning bus 0 for devices... 1 USB Device(s) found
   scanning bus 2 for devices... 1 USB Device(s) found
          scanning usb for storage devices... 0 Storage Device(s) found
   Hit any key to stop autoboot:  0
   (FEL boot)
   ## Executing script at 43100000
   ## Flattened Device Tree blob at 43000000
      Booting using the fdt blob at 0x43000000
      Loading Device Tree to 49ff6000, end 49fff8ed ... OK

   Starting kernel ...


   [    0.000000] Booting Linux on physical CPU 0x0

   [    0.000000] Linux version 4.14.0-next-20171121 (root@jagan-XPS-13-9350) (gcc version 6.3.1 20170109 (Linaro GCC 6.3-2017.02)) #1 SMP Fri Nov 24 01:26:00 IST 2017

   [    0.000000] CPU: ARMv7 Processor [410fc074] revision 4 (ARMv7), cr=10c5387d

   [    0.000000] CPU: div instructions available: patching division code

   [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache

   [    0.000000] OF: fdt: Machine model: LeMaker Banana Pi

   [    0.000000] Memory policy: Data cache writealloc

   [    0.000000] psci: probing for conduit method from DT.

   [    0.000000] psci: Using PSCI v0.1 Function IDs from DT

   [    0.000000] percpu: Embedded 16 pages/cpu @ef7c6000 s33740 r8192 d23604 u65536

   [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 260202

   [    0.000000] Kernel command line: console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait
