Allwinner SUNXI64
=================

Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Banana Pi BPI-M64 board.

    ATF
    U-Boot
    Linux

ATF

::

        $ git clone https://github.com/apritzel/arm-trusted-firmware.git
        $ cd arm-trusted-firmware
        $ make PLAT=sun50iw1p1 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin

U-Boot

::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make bananapi_m64_defconfig
        $ make 

Linux

::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git

        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs
