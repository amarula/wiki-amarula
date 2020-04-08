SiFive HiFive Unleashed A00
###########################

This tutorial will show the details of SiFive HiFive Unleashed A00 board mainline support.

More information about SoC manual and schematics are at
`FU540 C000 <https://static.dev.sifive.com/FU540-C000-v1.0.pdf>`_ and
`Schematics <https://sifive.cdn.prismic.io/sifive%2Ff7173056-bf37-4407-87cb-d5ab76abf61a_hifive-unleashed-a00-schematics.pdf>`_

Building
========

OpenSBI
------

.. code-block:: none

   git clone https://github.com/riscv/opensbi
   cd opensbi
   CROSS_COMPILE=/path/to/riscv64-linux-gnu- make PLATFORM=sifive/fu540 FW_DYNAMIC=y

U-Boot
------

.. code-block:: none

   git clone https://github.com/amarula/u-boot-amarula
   cd u-boot-amarula
   make sifive_fu540_defconfig
   make

Linux
-----

.. code-block:: none

   git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
   cd linux-next
   make mrproper
   ARCH=riscv make defconfig
   ARCH=arm64 make Image dtbs

Buildroot
--------

.. code-block:: none

   git clone https://github.com/amarula/buildroot-amarula
   cd buildroot-amarula
   make hifive_unleashed_defconfig

Booting
=======

1. Parttion table
   SiFive ZSBL (BROM) would look for partition GUID for next boot stages like
.. code-block:: none

   5B193300-FC78-40CD-8002-E86C45580B47 - FSBL
   2E54B353-1271-4842-806F-E436D6AF6985 - Bootloader

   So, use buildroot sdcard.img and write into SD card since it has default
   partition table.

2. Bootmodes
   Bootmodes are configured in SiFive Unleased via MSEL3-MSEL0.
.. code-block:: none

   MSEL = 1111, default bootmode. load FSBL from QSPI
   MSEL = 1011, load FSB from SD card

   Make sure the MSEL will be in default.

3. Serial ports

   Board as USB port which used USB-to-Serial, host will trigger
.. code-block:: none
 
   /dev/ttyUSB1 - for debug
   /dev/ttyUSB0 - for JTAG

OpenSBI with Linux as payload
-----------------------------

Take the empty unpartitioned SD card

Build the Buildroot like

.. code-block:: none

   git clone https://github.com/amarula/buildroot-amarula
   cd buildroot-amarula
   make hifive_unleashed_defconfig
   sudo dd if=output/images/sdcard.img of=/dev/mmcblk0

Set MSEL[3:0] to 1111, default bootmode. load FSBL from QSPI

Turn On the board and open minicom with /dev/ttyUSB1 with 115200 baudrate.

.. code-block:: none

   SiFive FSBL:       2018-03-20
   HiFive-U serial #: 000001e0

   OpenSBI v0.4 (Sep 18 2019 22:56:42)
        ____                    _____ ____ _____
       / __ \                  / ____|  _ \_   _|
      | |  | |_ __   ___ _ __ | (___ | |_) || |
      | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
      | |__| | |_) |  __/ | | |____) | |_) || |_
       \____/| .__/ \___|_| |_|_____/|____/_____|
             | |
             |_|

   Platform Name          : SiFive Freedom U540
   Platform HART Features : RV64ACDFIMSU
   Platform Max HARTs     : 5
   Current Hart           : 2
   Firmware Base          : 0x80000000
   Firmware Size          : 92 KB
   Runtime SBI Version    : 0.1

   PMP0: 0x0000000080000000-0x000000008001ffff (A)
   PMP1: 0x0000000000000000-0x0000007fffffffff (A,R,W,X)
   [    0.000000] OF: fdt: Ignoring memory range 0x80000000 - 0x80200000
   [    0.000000] Linux version 5.1.0 (jagan@jagan-XPS-13-9350) (gcc version 8.3.0 (Buildroot 2019.11-git-00334-g2b5e835dcd)) #1 SMP Wed Sep 18 22:51:28 IST 9
   [    0.000000] earlycon: sbi0 at I/O port 0x0 (options '')


OpenSBI with U-Boot as payload
-----------------------------

Use same SD card partition as of above method.

Attach u-boot payload from `U-Boot <https://wiki.amarulasolutions.com/bsp/riscv/hifive-unleashed.html#u-boot>_`

.. code-block:: none

   cd /path/to/opensbi
   make distclean
   make PLATFORM=sifive/fu540 FW_PAYLOAD_PATH=/path/to/u-boot/u-boot-dtb.bin
   sudo dd if=./build/platform/sifive/fu540/firmware/fw_payload.bin of=/dev/mmcblk0p1 bs=1024

Set MSEL[3:0] to 1111, default bootmode. load FSBL from QSPI

Turn On the board and open minicom with /dev/ttyUSB1 with 115200 baudrate.

.. code-block:: none

   SiFive FSBL:       2018-03-20
   HiFive-U serial #: 000001e0

   OpenSBI v0.4 (Sep 18 2019 22:56:42)
        ____                    _____ ____ _____
       / __ \                  / ____|  _ \_   _|
      | |  | |_ __   ___ _ __ | (___ | |_) || |
      | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
      | |__| | |_) |  __/ | | |____) | |_) || |_
       \____/| .__/ \___|_| |_|_____/|____/_____|
             | |
             |_|

   Platform Name          : SiFive Freedom U540
   Platform HART Features : RV64ACDFIMSU
   Platform Max HARTs     : 5
   Current Hart           : 2
   Firmware Base          : 0x80000000
   Firmware Size          : 92 KB
   Runtime SBI Version    : 0.1

   PMP0: 0x0000000080000000-0x000000008001ffff (A)
   PMP1: 0x0000000000000000-0x0000007fffffffff (A,R,W,X)


   U-Boot 2020.01-rc1-00217-g10aa74cb53-dirty (Nov 09 2019 - 17:12:46 +0530)

   CPU:   rv64imafdc
   Model: SiFive HiFive Unleashed A00
   DRAM:  8 GiB
   MMC:   spi@10050000:mmc@0: 0
   In:    serial@10010000
   Out:   serial@10010000
   Err:   serial@10010000
   Net:   eth0: ethernet@10090000
   Hit any key to stop autoboot:  0
   =>

OpenSBI FW_DYNAMIC
------------------

1. Boot from MMC

Take the empty unpartitioned SD card

Create the GPT parttion to the SD card.

.. code-block:: none

   sudo sgdisk --clear \
   > --new=1:34:2081 --change-name=1:loader1 --typecode=1:5B193300-FC78-40CD-8002-E86C45580B47 \
   > --new=2:2082:10273 --change-name=2:loader2 --typecode=2:2E54B353-1271-4842-806F-E436D6AF6985 \
   > --new=3:10274: --change-name=3:rootfs --typecode=3:0FC63DAF-8483-4772-8E79-3D69D8477DE4 \
   > /dev/mmcblk0

Build the `Buildroot <https://wiki.amarulasolutions.com/bsp/riscv/hifive-unleashed.html#buildroot>_`

.. code-block:: none

   cd /path/to/buildroot
   sudo dd if=output/images/sdcard.img of=/dev/mmcblk0
   sudo sync

Set MSEL jumper to MSEL[3:0] to 1011 like

.. image:: /images/hifive-unleashed-sdboot.jpg

Turn On the board and open minicom with /dev/ttyUSB1 with 115200 baudrate.

.. code-block:: none

   U-Boot SPL 2020.04-rc4 (Apr 08 2020 - 23:26:19 +0530)
   Trying to boot from MMC1
   
   
   U-Boot 2020.04-rc4 (Apr 08 2020 - 23:26:19 +0530)
   
   CPU:   rv64imafdc
   Model: SiFive HiFive Unleashed A00
   DRAM:  8 GiB
   MMC:   spi@10050000:mmc@0: 0
   In:    serial@10010000
   Out:   serial@10010000
   Err:   serial@10010000
   Net:   eth0: ethernet@10090000
   Hit any key to stop autoboot:  0
   switch to partitions #0, OK
   mmc0 is current device
   Scanning mmc 0:3...
   Found /boot/extlinux/extlinux.conf
   Retrieving file: /boot/extlinux/extlinux.conf
   151 bytes read in 3 ms (48.8 KiB/s)
   1:      HiFive-Unleashed linux
   Retrieving file: /boot/Image
   9734224 bytes read in 4735 ms (2 MiB/s)
   append: console=ttySIF0 root=/dev/mmcblk0p3 rootwait rw
   Retrieving file: /boot/hifive-unleashed-a00.dtb
   6987 bytes read in 7 ms (974.6 KiB/s)
   ## Flattened Device Tree blob at 88000000
   Booting using the fdt blob at 0x88000000
   Using Device Tree in place at 0000000088000000, end 0000000088004b4a
   
   Starting kernel ...
   
   [    0.000000] OF: fdt: Ignoring memory range 0x80000000 - 0x80200000
   [    0.000000] Linux version 5.6.0 (jagan@jagan-XPS-13-9350) (gcc version 8.4.0 (Buildroot 2020.05-git-00624-g689b9c1a7c-dirty)) #1 SMP Wed Apr 8
   22:35:27 IST 2020
   [    0.000000] initrd not found or empty - disabling initrd
   [    0.000000] Zone ranges:
   [    0.000000]   DMA32    [mem 0x0000000080200000-0x00000000ffffffff]
   [    0.000000]   Normal   [mem 0x0000000100000000-0x000000027fffffff]
   [    0.000000] Movable zone start for each node
   [    0.000000] Early memory node ranges
   [    0.000000]   node   0: [mem 0x0000000080200000-0x000000027fffffff]
   [    0.000000] Initmem setup node 0 [mem 0x0000000080200000-0x000000027fffffff]
   [    0.000000] software IO TLB: mapped [mem 0xfbfff000-0xfffff000] (64MB)
   [    0.000000] CPU with hartid=0 is not available
   [    0.000000] CPU with hartid=0 is not available
   [    0.000000] elf_hwcap is 0x112d
   [    0.000000] percpu: Embedded 17 pages/cpu s31848 r8192 d29592 u69632
   [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 2067975
   [    0.000000] Kernel command line: console=ttySIF0 root=/dev/mmcblk0p3 rootwait rw
