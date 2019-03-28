Giotto Tune
===========

Giotto tune-box and board-amarula

.. image:: /images/giotto-tune-box-and-board-amarula.jpg


WE PRESENT YOU GIOTTO TUNE
Giotto Tune is born from a passion to make great sound quality available and affordable to everyone. Named after the painter who stayed true to nature’s purest form, it allows you to listen to music clear and cleaner as you’ve never heard before.

WHAT IS GIOTTO TUNE?
Giotto Tune plays music files encoded in PCM of different formats and at different bitrates, ranging from 44.100Khz to 192.000Khz up to 32bit and files in DSD64 format and DSD128 format.
It allows you to enjoy and control your music with the Open Source Audiophile Music player Volumio 2, Kodi, UPnP and all mpd compatible players.

Plus, it is highly compatible. Not only does it fit perfectly on the well known Raspberry PI, but we are making the Giotto Tune also compatible with the Asus Tinker board.

DOWNLOAD SOURCE CODE FOR GIOTTO AND COMPILE

::

        git clone https://github.com/panicking/linux-giotto
         
         
        export ARCH=arm
        export CROSS_COMPILE=arm-linux-gnueabihf-
        make bcm2709_defconfig
        make zImage modules dtbs
        mount sdcard partitions
        cp arch/arm/boot/zImage /media/user/boot/kernel7.img
        cp arch/arm/boot/dts/*.dtb /media/user/boot/
        cp arch/arm/boot/dts/overlays/*.dtb* /media/user/boot/overlays/
         
Change or add in /media/user/config.txt dtoverlay=giotto-dac

::

        sudo make -j4 ARCH=arm INSTALL_MOD_PATH=/media/user/rootfs/ modules_install
         
        umount the sdcard partitions
 
# Now your device is ready. Volume should be controlled by sysfs but this will be in another update
