Engicam MicroGEA STM32MP1 Linux-5.10, U-Boot-2021-01-rc2
========================================================

.. note:: **TL;DR**
   - Amarula Solutions mainlined the **Engicam MicroGEA STM32MP1 SoM** with STM32MP157 — running **Linux 5.10 and U-Boot 2021-01-rc2** with SD card boot instructions, including a capacitive carrier board and 7" LVDS Open Frame board.

.. image:: /images/eng-microgea-stm32mp1.png

Amarula Solutions has partnered with Engicam Srl and started a project
to push Engicam SOM's and Carrier board's BSP onto Mainline U-Boot,
Linux Kernel, Yocto/Buildroot, and Multimedia Open source projects.

We have supported PX30-Core in Mainline as posted before
`PX30-Core <https://wiki.amarulasolutions.com/news/engicam-px30-core-mainline.html>`_, now
we have another project-based `STMicroelectronics <https://www.st.com/content/st_com/en.html>`_
STM32MP1 SoM, `Engicam MicroGEAM STM32MP1 <https://www.engicam.com/vis-prod/101358>`_

For this specific SoM, Engicam is providing a `Capacitive Carrier board <https://www.engicam.com/vis-prod/101504>`_
and a `7" LVDS interfaced Open Frame board <https://www.engicam.com/vis-prod/101296>`_

Now, both these combinations are running Linux-5.10 and U-Boot-2021-01-rc2
and ready to send upstream patches.

U-Boot::

        git clone https://github.com/openedev/u-boot
        cd u-boot
        git checkout -b stm32mp1 stm32mp1/icore-microgea
        make stm32mp15_microgea_stm32mp1_defconfig
        make

Linux::

        git clone https://github.com/openedev/linux
        cd linux
        git checkout -b stm32mp1 stm32mp1/icore-microgea
        make ARCH=arm multi_v7_defconfig
        make ARCH=arm zImage dtbs -j 16

DTB::

        stm32mp157c-microgea-stm32mp1-cap.dtb
        stm32mp157c-microgea-stm32mp1-cap-of7.dtb

SD::

        sudo sgdisk -o /dev/sdx
        sudo sgdisk --resize-table=128 -a 1 \
        > -n 1:34:545 -c 1:fsbl1 \
        > -n 2:546:1057 -c 2:fsbl2 \
        > -n 3:1058:5153 -c 3:ssbl \
        > -n 4:5154: -c 4:rootfs \
        > -p /dev/sdx
        cd u-boot
        sudo dd if=spl/u-boot-spl.stm32 of=/dev/sdx1
        sudo dd if=spl/u-boot-spl.stm32 of=/dev/sdx2
        sudo dd if=u-boot.img of=/dev/sdx3
        sudo sync

extlinux::

        label Engicam MicroGEA STM32MP1 Linux-5.10
          kernel /boot/zImage
          devicetree /boot/stm32mp157c-microgea-stm32mp1-cap-of7.dtb
          append console=tty0 console=ttySTM0,115200n8 root=PARTUUID=8ed1d778-39ec-4a73-82f5-cbb3c5480e63 rootwait rw

.. Jagan Teki <jagan@amarulasolutions.com>
.. Friday 30 October 2020 04:43:22 PM IST

.. tip::
   Need mainline BSP support for STM32MP1-based products? Amarula Solutions
   provides U-Boot and Linux kernel mainlining, Yocto/Buildroot integration,
   and upstream-first development for STM32MP1 and STM32MP2 platforms.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
