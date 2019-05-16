Olimex A33 OlinuXino
####################

This tutorial will show the details of Olimex A33-OLinuXino board mainline support
and other details like hardware, documentation, schematics are available at `hardware <https://www.olimex.com/Products/OLinuXino/A33/A33-OLinuXino/open-source-hardware>`_ and linux-sunxi

Hardware Access
***************
Power supply: External 5V Jack
USB OTG Cable, USB to TTL for debug

BSP Build
*********
Image building need host to ready with all necessary tools ready, refer here

U-Boot
======
::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make A33-OLinuXino_defconfig && make

Linux
=====
::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm sunxi_defconfig
        ARCH=arm make -j 4 zImage dtbs

Booting
*******

SD Boot
=======
Write Boot image

::

   dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=8k seek=1

Now insert the card into A33-OlinuXino board, power on.
