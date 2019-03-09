Tools
=====


Host

These are host ready tools installation for Ubuntu 18.04 LTS on 64 bit

::

        $ apt-get install flex bison libsdl2-dev libssl-dev u-boot-tools git python python-dev ia32-libs lib32ncurses5 lib32z1 swig
        $ git clone git://git.kernel.org/pub/scm/utils/dtc/dtc.git
        $ cd dtc
        $ make && make install PREFIX=/path/to/install
        $ export PATH=/path/to/install/dtc:$PATH

Crosstool
ARM

::

        bash> cd /to/path
        bash> wget https://releases.linaro.org/components/toolchain/binaries/6.3-2017.02/arm-linux-gnueabi/gcc-linaro-6.3.1-2017.02-i686_arm-linux-gnueabi.tar.xz
        bash> tar xvf gcc-linaro-6.3.1-2017.02-i686_arm-linux-gnueabi.tar.xz
        bash> export PATH=/to/path/gcc-linaro-6.3.1-2017.02-i686_arm-linux-gnueabi/bin:$PATH
        bash> export CROSS_COMPILE=arm-linux-gnueabi-

ARM64

::

        bash> cd /to/path
        bash> wget https://releases.linaro.org/components/toolchain/binaries/6.3-2017.02/aarch64-linux-gnu/gcc-linaro-6.3.1-2017.02-i686_aarch64-linux-gnu.tar.xz
        bash> tar xvf gcc-linaro-6.3.1-2017.02-i686_aarch64-linux-gnu.tar.xz
        bash> export PATH=/to/path/gcc-linaro-6.3.1-2017.02-i686_aarch64-linux-gnu/bin:$PATH
        bash> export CROSS_COMPILE=aarch64-linux-gnu-

SD Setup
Single partition

::

        $ fdisk /dev/mmcblk0


        Welcome to fdisk (util-linux 2.27.1).

        Changes will remain in memory only, until you decide to write them.

        Be careful before using the write command.



        Command (m for help): n

        To create more partitions, first replace a primary with an extended partition.


        Command (m for help): p

        Disk /dev/mmcblk0: 14.9 GiB, 15931539456 bytes, 31116288 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Device         Boot Start      End  Sectors  Size Id Type

        /dev/mmcblk0p1       2048 31116287 31114240 14.9G 83 Linux


        Command (m for help): d

        Selected partition 1

        Partition 1 has been deleted.


        Command (m for help): p

        Disk /dev/mmcblk0: 14.9 GiB, 15931539456 bytes, 31116288 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Command (m for help): n

        Partition type

           p   primary (0 primary, 0 extended, 4 free)

           e   extended (container for logical partitions)

        Select (default p):


        Using default response p.

        Partition number (1-4, default 1):

        First sector (2048-31116287, default 2048):

        Last sector, +sectors or +size{K,M,G,T,P} (2048-31116287, default 31116287):


        Created a new partition 1 of type 'Linux' and of size 14.9 GiB.


        Command (m for help): w

        The partition table has been altered.

        Calling ioctl() to re-read partition table.

        Syncing disks.


        $ mkfs.ext4 -L rootfs /dev/mmcblk0p1

Falcon partition

::

        $ fdisk /dev/mmcblk0


        Welcome to fdisk (util-linux 2.27.1).

        Changes will remain in memory only, until you decide to write them.

        Be careful before using the write command.



        Command (m for help): p

        Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Command (m for help): q


        $ sfdisk /dev/mmcblk0


        Welcome to sfdisk (util-linux 2.27.1).

        Changes will remain in memory only, until you decide to write them.

        Be careful before using the write command.


        Checking that no-one is using this disk right now ... OK


        Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Old situation:


        Type 'help' to get more information.


        >>> 30M,

        Created a new DOS disklabel with disk identifier 0x13e85f5a.

        Created a new partition 1 of type 'Linux' and of size 14.4 GiB.

        /dev/mmcblk0p1 :        20480     30253055 (14.4G) Linux

        /dev/mmcblk0p2: write


        New situation:


        Device         Boot Start      End  Sectors  Size Id Type

        /dev/mmcblk0p1      20480 30253055 30232576 14.4G 83 Linux


        The partition table has been altered.


        Calling ioctl() to re-read partition table.

        $ mkfs.ext4 -L rootfs /dev/mmcblk0p1

Dual partition

::

        $ fdisk /dev/mmcblk0


        Welcome to fdisk (util-linux 2.27.1).

        Changes will remain in memory only, until you decide to write them.

        Be careful before using the write command.



        Command (m for help): p

        Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Command (m for help): n

        Partition type

           p   primary (0 primary, 0 extended, 4 free)

           e   extended (container for logical partitions)

        Select (default p):


        Using default response p.

        Partition number (1-4, default 1):

        First sector (2048-30253055, default 2048):

        Last sector, +sectors or +size{K,M,G,T,P} (2048-30253055, default 30253055): +64M


        Created a new partition 1 of type 'Linux' and of size 64 MiB.


        Command (m for help): n

        Partition type

           p   primary (1 primary, 0 extended, 3 free)

           e   extended (container for logical partitions)

        Select (default p):


        Using default response p.

        Partition number (2-4, default 2):

        First sector (133120-30253055, default 133120):

        Last sector, +sectors or +size{K,M,G,T,P} (133120-30253055, default 30253055):


        Created a new partition 2 of type 'Linux' and of size 14.4 GiB.


        Command (m for help): p

        Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors

        Units: sectors of 1 * 512 = 512 bytes

        Sector size (logical/physical): 512 bytes / 512 bytes

        I/O size (minimum/optimal): 512 bytes / 512 bytes

        Disklabel type: dos

        Disk identifier: 0x00000000


        Device         Boot  Start      End  Sectors  Size Id Type

        /dev/mmcblk0p1        2048   133119   131072   64M 83 Linux

        /dev/mmcblk0p2      133120 30253055 30119936 14.4G 83 Linux


        Command (m for help): w

        The partition table has been altered.

        Calling ioctl() to re-read partition table.

        Syncing disks.

        $ mkfs.vfat -n BOOT /dev/mmcblk0p1

        $ mkfs.ext4 -L rootfs /dev/mmcblk0p2


Console Setting

We use minicom to get serial console.

SUNXI
sunxi-fel

::

        $ git clone https://github.com/openedev/sunxi-tools
        $ cd sunxi-tools
        $ git checkout -b working origin/working
        $ make

boot32-fel.scr

::

        $ boot32-fel.cmd
        setenv bootargs console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait
        bootz $kernel_addr_r - $fdt_addr_r
        # ./tools/mkimage -C none -A arm -T script -d boot32-fel.cmd boot.scr
        Image Name:   
        Created:      Fri Nov 24 14:29:56 2017
        Image Type:   ARM Linux Script (uncompressed)
        Data Size:    121 Bytes = 0.12 KiB = 0.00 MiB
        Load Address: 00000000
        Entry Point:  00000000
        Contents:
           Image 0: 113 Bytes = 0.11 KiB = 0.00 MiB

boot64-fel.scr

::

        $ boot64-fel.cmd
        setenv bootargs console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait
        booti $kernel_addr_r - $fdt_addr_r
        # ./tools/mkimage -C none -A arm -T script -d boot64-fel.cmd boot.scr
        Image Name:   
        Created:      Fri Nov 24 14:29:56 2017
        Image Type:   ARM Linux Script (uncompressed)
        Data Size:    121 Bytes = 0.12 KiB = 0.00 MiB
        Load Address: 00000000
        Entry Point:  00000000
        Contents:
           Image 0: 113 Bytes = 0.11 KiB = 0.00 MiB

Virtual disk

::

        # dd if=/dev/zero of=zero.bin bs=1024 count=1024
        1024+0 records in
        1024+0 records out
        # du -hs zero.bin
        1.0M    zero.bin
        # losetup /dev/loop0 zero.bin
        # losetup -a
        /dev/loop0: 0 zero.bin
        # mke2fs -F -m0 /dev/loop0
        Filesystem label=
        OS type: Linux
        Block size=1024 (log=0)
        Fragment size=1024 (log=0)
        128 inodes, 1024 blocks
        0 blocks (0%) reserved for the super user
        First data block=1
        Maximum filesystem blocks=262144
        1 block groups
        8192 blocks per group, 8192 fragments per group
        128 inodes per group
        # mount -t ext4 /dev/loop0 /mnt/
        [  293.048823] EXT4-fs (loop0): mounted filesystem without journal. Opts: (null)
        # ls /mnt/
        lost+found
        # mount
        /dev/loop0 on /mnt type ext4 (rw,relatime,block_validity,delalloc,barrier,user_xattr,acl)
        # cd /mnt/
        # ls
        lost+found
        # cp /etc/wpa_supplicant.conf .
        # ls
        lost+found           wpa_supplicant.conf
        # cd -
        /root
        # sync
        # umount  /mnt/
        # losetup -d /dev/loop0

Network
TFTP

Install package

::

        $ sudo apt-get install xinetd tftpd tftp

Create /etc/xinetd.d/tftp and put this entry

::

        service tftp
        {
        protocol        = udp
        port            = 69
        socket_type     = dgram
        wait            = yes
        user            = nobody
        server          = /usr/sbin/in.tftpd
        server_args     = /tftpboot
        disable         = no
        }


Create a folder /tftpboot this should match whatever you gave in server_args

::

        $ sudo mkdir /tftpboot
        $ sudo chmod -R 777 /tftpboot
        $ sudo chown -R nobody /tftpboot

Build images from and copy on /tftpboot, example rk3288-vyasa board

::

        $ cp /path/to/linux-next/arch/arm/boot/uImage /tftpboot
        $ cp /path/to/linux-next/arch/arm/boot/dts/rk3288-vyasa.dtb /tftpboot

Setup Host IP address, remember this is compatible with target serverip

::

        $ ifconfig eth0 10.39.66.9 netmask 255.255.255.0 up

Restart the xinetd service

::

        $ sudo service xinetd restart
