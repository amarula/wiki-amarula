FriendlyARM Nanopi M1 
#####################

Hardware
********

.. image:: /images/nanopi_m1.jpg

Buildroot
*********

It’s easy to build entire system using buildroot and mainline supported FriendlyARM Nanopi M1 Plus.
See read this `readme.txt <https://git.buildroot.net/buildroot/tree/board/friendlyarm/nanopi-m1/readme.txt>`_ for more info.

::

   $ git clone git://git.busybox.net/buildroot
   $ cd buildroot
   $ make nanopi_m1_defconfig
   $ make

