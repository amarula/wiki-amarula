Allwinner SUNXI32
=================

Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Banana Pi BPI-M1 board.

    U-Boot
    Linux
    Rootfs

U-Boot

::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make bananapi_m1_defconfig
        $ make 

Linux

::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git

        $ cd linux-next
        $ make mrproper
        $ ARCH=arm make sunxi_defconfig
        $ ARCH=arm make -j 4 zImage dtbs

Rootfs

::

        $ git clone https://github.com/openedev/rfs-rk3288

        $ dd if=/dev/zero of=arm_ramdisk.image bs=1k count=16384

        $ mke2fs -F -m0 arm_ramdisk.image

        $ mount -t ext4 arm_ramdisk.image /mnt -o loop

        $ cp -rf rfs-rk3288/* /mnt

        $ umount /mnt

