SiFive HiFive Unleashed A00
###########################

This tutorial will show the details of SiFive HiFive Unleashed A00 board mainline support.

More information about SoC manual and schematics are at
`FU540 C000 <https://static.dev.sifive.com/FU540-C000-v1.0.pdf>`_ and
`Schematics <https://sifive.cdn.prismic.io/sifive%2Ff7173056-bf37-4407-87cb-d5ab76abf61a_hifive-unleashed-a00-schematics.pdf>`_

Building
========

Setup riscv64 cross compiler

.. code-block:: none

   export CROSS_COMPILE=riscv64-buildroot-linux-gnu-

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

.. code-block:: none

   sudo dd if=/path/to/buildroot/sdcard.img of=/dev/mmcblk0

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

.. code-block:: none

   cd /path/to/opensbi
   make PLATFORM=sifive/fu540 FW_PAYLOAD_PATH=/path/to/u-boot/u-boot-dtb.bin
   sudo dd if=/path/to/opensbi/fw_payload.bin of=/dev/mmcblk0p1 bs=1024

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

OpenSBI as FW_DYNAMIC
---------------------
