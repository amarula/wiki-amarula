Allwinner SUNXI64
=================
.. note:: **TL;DR**
   - Technical guide covering **U-Boot** features for embedded systems — part of Amarula Solutions' upstream-first boot firmware documentation.
   - Includes build instructions, configuration steps, and production deployment guidance.

Image building need host to ready with all necessary tools ready, `refer here <https://wiki.amarulasolutions.com/uboot/tools.html>`_

Below are the details of Image build for Banana Pi BPI-M64 board.


How do you build ATF?
*********************
::

        $ git clone https://github.com/apritzel/arm-trusted-firmware.git
        $ cd arm-trusted-firmware
        $ make PLAT=sun50iw1p1 bl31
        $ export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin

How do you build U-Boot?
************************
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make bananapi_m64_defconfig
        $ make 

How do you build the Linux kernel?
**********************************
::

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git

        $ cd linux-next
        $ make mrproper
        $ ARCH=arm64 make defconfig
        $ ARCH=arm64 make -j 4 Image dtbs


.. tip::
   Need U-Boot development or secure boot implementation for your embedded
   product? Amarula Solutions provides boot firmware engineering, mainline
   upstreaming, and production boot configuration.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
