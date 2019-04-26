Engicam i.MX6
#############

Image building need host to ready with all necessary tools ready, `refer here <https://wiki.amarulasolutions.com/uboot/tools.html>`_ Below are the details of Image build for Engicam i.CoreM6 Quad board

U-Boot
******
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make imx6qdl_icore_mmc_defconfig
        $ make 

Linux
*****
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        $ cd linux-next
        $ ARCH=arm make imx_v6_v7_defconfig
        $ ARCH=arm make LOADADDR=0x10008000 uImage dtbs

Ramdisk
*******
::

        $ git clone https://github.com/openedev/rootfs-imx6q.git

        $ dd if=/dev/zero of=arm_ramdisk.image bs=1k count=16384

        $ mke2fs -F -m0 arm_ramdisk.image

        $ mount -t ext4 arm_ramdisk.image /mnt -o loop

        $ cp -rf rootfs-imx6q/* /mnt

        $ umount /mnt

        $ gzip arm_ramdisk.image

        $ mkimage -A arm -T ramdisk -C gzip -d arm_ramdisk.image.gz uarm_ramdisk.image.gz

        Image Name:   

        Created:      Thu Oct  5 14:18:23 2017

        Image Type:   ARM Linux RAMDisk Image (gzip compressed)

        Data Size:    691309 Bytes = 675.11 kB = 0.66 MB

        Load Address: 00000000

        Entry Point:  00000000

