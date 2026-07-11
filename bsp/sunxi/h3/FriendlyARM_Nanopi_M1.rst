FriendlyARM Nanopi M1
#####################

.. note:: **TL;DR**
   - Mainline BSP bring-up guide for this board — covering **U-Boot**, **Linux kernel**, and **Buildroot** build from source with SD/flash boot, serial console access, and device tree configuration.
   - Part of Amarula Solutions' upstream-first BSP documentation for Allwinner SoCs.

How do you access the hardware?
*******************************

.. image:: /images/nanopi_m1.jpg

How do you build with Buildroot?
********************************

It’s easy to build entire system using buildroot and mainline supported FriendlyARM Nanopi M1 Plus.
See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/friendlyarm/nanopi-m1/readme.txt>`_ for more info.

::

   $ git clone git://git.busybox.net/buildroot
   $ cd buildroot
   $ make nanopi_m1_defconfig
   $ make

.. tip::
   Need mainline BSP support for Allwinner platforms? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Buildroot/Yocto integration,
   and upstream-first development for Allwinner-based embedded products.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
