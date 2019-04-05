FriendlyARM Nanopi M1 Plus
##########################

Hardware
********

.. image:: /images/friendlyarm_nanopi_m1_plus.jpg

Buildroot
*********

It’s easy to build entire system using buildroot and mainline supported FriendlyARM Nanopi M1 Plus.
See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/friendlyarm/nanopi-m1-plus/readme.txt>`_ for more info.

::

   $ git clone git://git.busybox.net/buildroot
   $ cd buildroot
   $ make nanopi_m1_plus_defconfig
   $ make

