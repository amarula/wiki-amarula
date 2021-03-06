Rockchip RK3288
###############

Image building need host to ready with all necessary tools ready, `refer here <https://wiki.amarulasolutions.com/uboot/tools.html>`_

Below are the details of Image build for Vyasa RK3288 board.

U-Boot
******
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make vyasa-rk3288_defconfig
        $ make 

Linux
*****
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git

        $ cd linux-next
        $ make mrproper
        $ ARCH=arm make multi_v7_defconfig
        $ ARCH=arm make -j 4 LOADADDR=0x02000000 uImage dtbs
        $ ARCH=arm make modules -j 4
        $ ARCH=arm make modules_install -j 4

Rootfs
******
::

        $ git clone https://github.com/openedev/rfs-rk3288

        $ dd if=/dev/zero of=arm_ramdisk.image bs=1k count=16384

        $ mke2fs -F -m0 arm_ramdisk.image

        $ mount -t ext4 arm_ramdisk.image /mnt -o loop

        $ cp -rf rfs-rk3288/* /mnt

        $ umount /mnt
