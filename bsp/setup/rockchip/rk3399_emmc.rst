RK3399 eMMC Boot
################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, **Buildroot/Yocto** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation.

Few of high ended RK3399 SBC's like Firefly and Orangepi vendor boards 
by default boot from eMMC and there is no way to boot from SD by means 
of any hardware jumpers or etc.

So, this document hack the boot mode programmatically erasing eMMC so-that 
the Rockchip BootROM will look for proper boot image in SD, assuming the 
SD card has valid boot image.

By default, the rockchip BootROM looking for IDB loader in eMMC at 
offsets {0, 512, 1024, 1536, 2048}KB + 32KB which are
sectors 64, 1088, 2112, 3136, 4160

So zero to one byte on each above sector can by pass the ROM to look 
for another boot source.

So, boot the default board, which automatically boot from eMMC.

Better preserve existing eMMC data into disk, so it can help for
future recovery.

::

        $ dd if=/dev/block/mmcxxx of=orangepi-rk3399-emmc-default.img
        $ dd if=/dev/zero of=/dev/block/mmcxxx bs=1b seek=64 count=1
        $ dd if=/dev/zero of=/dev/block/mmcxxx bs=1b seek=1088 count=1
        $ dd if=/dev/zero of=/dev/block/mmcxxx bs=1b seek=2112 count=1
        $ dd if=/dev/zero of=/dev/block/mmcxxx bs=1b seek=3136 count=1
        $ dd if=/dev/zero of=/dev/block/mmcxxx bs=1b seek=4160 count=1

.. tip::
   Need help setting up BSPs for embedded platforms? Amarula Solutions
   provides mainline U-Boot and Linux kernel support, Yocto/Buildroot
   integration, and eMMC/SDRAM flashing guidance.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
