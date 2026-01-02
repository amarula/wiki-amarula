Welcome to Amarula Wiki!
========================

.. _contents: Table of contents

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   news/index
   about/about.rst
   articles/index
   opensource/index
   ci/index
   security/index
   found/index
   bsp/index
   hw/index


.. include:: reports/report-01-2026.rst
.. include:: reports/report-12-2025.rst
.. include:: reports/report-11-2025.rst
.. include:: reports/report-10-2025.rst
.. include:: reports/report-09-2025.rst
.. include:: reports/report-08-2025.rst

Amarul  Solutions Open source Contributions - March/April 2025
--------------------------------------------------------------

Amarula Solutions new contribuitions in opensource project

Contribuitions
------------------------

Patches
^^^^^^^
Buildroot Patch Updates

This page summarizes recent patch updates for the Buildroot project.

Adam Duskett
""""""""""""

  * **package/mender-update-modules: new package** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250225133829.2888663-1-adam.duskett@amarulasolutions.com/])
  * **package/mender-update-modules: enable docker, rpm, and script modules** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250225133829.2888663-2-adam.duskett@amarulasolutions.com/])

Dario Binacchi
""""""""""""""
  * **configs/stm32mp157*_dk*: bump TF-A to 2.10, Linux to 6.12.13 and U-Boot to 2025.01** (Link: [https://patchwork.ozlabs.org/project/buildroot/patch/20250214114612.3682462-1-dario.binacchi@amarulasolutions.com/])
  * **Add TF-A lts-v2.12.x selection** (Link: [https://patchwork.ozlabs.org/project/buildroot/patch/20250303170245.3657781-1-dario.binacchi@amarulasolutions.com/])
  * **package/linux-firmware:** Bump to 20250311 (Link: [https://patchwork.ozlabs.org/project/buildroot/list/?series=450826])
  * **package/ufs-utils:** New package (Link: [https://patchwork.ozlabs.org/project/buildroot/patch/20250401160957.4020794-1-dario.binacchi@amarulasolutions.com/])
  * **package/armadillo:** bump to version 14.4.1 (Link: [https://patchwork.ozlabs.org/project/buildroot/patch/20250401160957.4020794-1-dario.binacchi@amarulasolutions.com/])
  * **package/mmc-utils:** bump to version 2aef4cd9a84d	(Link: [https://patchwork.ozlabs.org/project/buildroot/patch/20250402074153.4038837-1-dario.binacchi@amarulasolutions.com/])
  * **package/apr:** bump to version 1.7.5 [(https://patchwork.ozlabs.org/project/buildroot/patch/20250406150929.691964-1-dario.binacchi@amarulasolutions.com/])
  * **boot/uboot:** bump to version v2025.04 [(https://patchwork.ozlabs.org/project/buildroot/patch/20250408072500.1771475-1-dario.binacchi@amarulasolutions.com/)]
  * **configs/stm32f469_disco_{sd, xip}: bump Linux to 5.15.179** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250409061736.2335242-1-dario.binacchi@amarulasolutions.com/])
  * **configs/stm32f429_disco_xip: bump Linux to 6.1.133** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250410161623.1940341-1-dario.binacchi@amarulasolutions.com/])
  * **configs/stm32f769_disco_sd: bump Linux to 5.15.179 and U-Boot to 2025.04** [(https://patchwork.ozlabs.org/project/buildroot/patch/20250411061818.2643355-1-dario.binacchi@amarulasolutions.com/])
  * **package/azure-iot-sdk-c: bump to version LTS_03_2025** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250411144739.3957036-1-dario.binacchi@amarulasolutions.com/])
  * **boot/ti-k3-boot-firmware: bump to version 11.00.10** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250412091936.1251605-1-dario.binacchi@amarulasolutions.com/])
  * **configs/imx6ulz_bsh_smm_m2: bump Linux to 6.1.134 and U-Boot to 2025.04**	([https://patchwork.ozlabs.org/project/buildroot/patch/20250417152425.3248986-1-dario.binacchi@amarulasolutions.com/])
  * **configs/beaglebone: bump Linux to 6.12.17-ti-arm32-r9 and U-Boot to 2025.04** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250417174106.4091085-1-dario.binacchi@amarulasolutions.com/])
  * **configs/imx8mn_bsh_smm_s2[_pro]: bump Linux to 6.12.23 and U-Boot to 2025.04** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250418153146.151159-1-dario.binacchi@amarulasolutions.com/])

Meena Murphy
""""""""""""
  * **[v4] configs/engicam_px30_core_defconfig: new defconfigi** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250401095407.488618-2-meena.murthy@amarulasolutions.com/])
  * **configs/engicam_px30_core: bump Linux to 6.12.22 and U-Boot to 2025.04** ([https://patchwork.ozlabs.org/project/buildroot/patch/20250409073750.1561127-2-meena.murthy@amarulasolutions.com/])


Other patches
^^^^^^^^^^^^^

Jenkins, Linux kernel and meta-codechecker

Dario Binacchi
""""""""""""""

  * **clk: stm32f4: fix an uninitialized variable** ([https://patchwork.kernel.org/project/linux-clk/patch/20250124111711.1051436-1-dario.binacchi@amarulasolutions.com/])
  * **ARM: dts: stm32: use IRQ_TYPE_EDGE_FALLING on stm32mp157c-dk2** ([https://lore.kernel.org/linux-arm-kernel/20250301115116.2862353-1-dario.binacchi@amarulasolutions.com/T/])
  * **Drop custom compatible from stm32f** ([https://patchwork.ozlabs.org/project/uboot/patch/20250224183931.313491-3-dario.binacchi@amarulasolutions.com/])
  * **Support NT35510 panel contrroller on stm32f769i-disco board** ([https://patchwork.ozlabs.org/project/uboot/list/?series=449785])
  * **doc: release_cycle: fix next relase version** ([https://patchwork.ozlabs.org/project/uboot/patch/20250408062847.1520368-1-dario.binacchi@amarulasolutions.com/])

Michael Trimarchi
"""""""""""""""""

  * **Support warning-ng format** ([https://github.com/dl9pf/meta-codechecker/pull/21])
  * **Update codechecker version to the latest** ([https://github.com/dl9pf/meta-codechecker/pull/20])
  * **Support CLANGSA** ([https://github.com/dl9pf/meta-codechecker/pull/23])
  * **Crumb fix and BitbucketSCM support** ([https://github.com/jenkinsci/bitbucket-plugin/pull/114])


Amarula Solutions Open Source Contributions - February 2025
-----------------------------------------------------------

Amarula Solutions is at the forefront of IoT innovation, actively contributing to open-source projects like
The Zephyr Project and Espressif Systems. This commitment to collaborative development allows us to deliver
cutting-edge solutions while strengthening the open-source community.

IoT Project Contributions
-------------------------

Merged Patches
^^^^^^^^^^^^^^

Flavia Caforio
""""""""""""""

* zephyr driver counter fix (`<https://github.com/zephyrproject-rtos/zephyr/pull/64979>`_)
* esp-mqtt fix workflows (`<https://github.com/espressif/esp-mqtt/pull/297>`_)
* esp-mqtt parse disconnect packet (`<https://github.com/espressif/esp-mqtt/pull/295>`_)

Dario Binacchi
""""""""""""""

* dts: arm: st: re-enable master can gating clock for can2 (`<https://github.com/zephyrproject-rtos/zephyr/pull/84503>`_)
* boards: stm32f769i_disco: drop led_4 node (`<https://github.com/zephyrproject-rtos/zephyr/pull/85367>`_)

Margherita Milani
"""""""""""""""""

* drivers: sensor: si7006: fix redundant include in si7006 (`<https://github.com/zephyrproject-rtos/zephyr/pull/73420>`_)
* drivers: sensor: add apds9253 driver (`<https://github.com/zephyrproject-rtos/zephyr/pull/73164>`_) (with Michael Trimarchi)

Michael Nazzareno Trimarchi
"""""""""""""""""""""""""""

* drivers: sensor: add apds9253 driver (`<https://github.com/zephyrproject-rtos/zephyr/pull/73164>`_) (with Margherita Milani)

Pending/Review Patches
^^^^^^^^^^^^^^^^^^^^^^

Michael Nazzareno Trimarchi and Margherita Milani
"""""""""""""""""""""""""""""""""""""""""""""""""

* drivers: sensor: apds9253: Add set attributes (`<https://github.com/zephyrproject-rtos/zephyr/pull/85132>`_)

**#iot #zephyr #espressif #opensource #embedded**

Buildroot and Yocto contribuitions
----------------------------------

Amarula Solutions has made contributions to the Buildroot project and Yocto Project,
demonstrating their commitment to the development and maintenance of this open-source
embedded Linux build system. We We are active contributors from Amarula Solutions,
and we have submitted various patches that enhance the functionality and stability
of Buildroot and Yocto

Merged Patches
^^^^^^^^^^^^^^

Dario Binacchi
""""""""""""""

* package/uuu: bump to version 1.5.201 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250114091520.529839-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/stm32f769_disco_sd: bump Linux to 5.15.176 and U-Boot to 2025.01 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250120183422.3342199-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/stm32f746_disco_sd: bump Linux to 5.15.176 and U-Boot to 2025.01 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250120183641.3343055-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/stm32f469_disco_{sd, xip}: bump Linux to 5.15.176 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250120183827.3343737-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/stm32f429_disco_xip: bump Linux to 6.1.126 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250120183958.3344525-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/ti_am62x_sk: bump Linux to 6.12.11 and U-Boot to 2025.01 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250126131716.2663079-1-dario.binacchi@amarulasolutions.com/>`_)

* package/uboot-bootcount: bump to version 3.1.0 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250130105931.2096913-1-dario.binacchi@amarulasolutions.com/>`_)

* board/stmicroelectronics/common/stm32mp157: restore Linux hash (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250207232035.3953972-1-dario.binacchi@amarulasolutions.com/>`_)

* package/pkg-download: don't export the download command variables (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250213180908.3963679-1-dario.binacchi@amarulasolutions.com/>`_)

* package/armadillo: bump to version 14.2.3 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250214092808.2372973-1-dario.binacchi@amarulasolutions.com/>`_)

* package/armadillo: bump to version 14.4.0 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250224184532.314335-1-dario.binacchi@amarulasolutions.com/>`_)

Pending/Review Patches
^^^^^^^^^^^^^^^^^^^^^^

Dario Binacchi
""""""""""""""

* board/stm32f769-disco: speed up U-Boot bootup (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250214113158.3584398-1-dario.binacchi@amarulasolutions.com/>`_)

* board/stm32f469-disco: speed up U-Boot bootup (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250214114612.3682462-1-dario.binacchi@amarulasolutions.com/>`_)

* configs/stm32mp157*_dk*: bump TF-A to 2.10, Linux to 6.12.13 and U-Boot to 2025.01 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250213175656.3857792-1-dario.binacchi@amarulasolutions.com/>`_)

Adam Duskett
""""""""""""

* board/mender/x86_64/post-build.sh: fix device_type location (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250225100912.1623970-1-adam.duskett@amarulasolutions.com/>`_)

* board/mender/x86_64/post-image-efi.sh: fix bootstrap creation (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250225100912.1623970-2-adam.duskett@amarulasolutions.com/>`_)

* package/mender-update-modules: new package (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250225133829.2888663-1-adam.duskett@amarulasolutions.com/>`_)

* package/mender-update-modules: enable docker, rpm, and script modules (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250225133829.2888663-2-adam.duskett@amarulasolutions.com/>`_)

* package/systemd: enable tmpfs kernel option (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250226090108.1007137-1-adam.duskett@amarulasolutions.com/>`_)

* flutter 3.29.0 updates (`<https://patchwork.ozlabs.org/project/buildroot/list/?series=446543>`_)

Andrea Ricchi
"""""""""""""

* [meta-oe] asyncmqtt: add recipe (`<https://patchwork.yoctoproject.org/project/oe/patch/20241031092222.16328-1-andrea.ricchi@amarulasolutions.com/>`_)

* [v2,1/1] package/cutekeyboard: bump version to 1.3.0 (`<https://patchwork.ozlabs.org/project/buildroot/patch/20250207150149.15505-1-andrea.ricchi@amarulasolutions.com/>`_)


**#linux #buildroot #yocto #opensource #embedded**

Linux kernel and U-boot contribuitions
--------------------------------------

Amarula Solutions has made contributions to the Linux kernel project and U-boot Project,
demonstrating their commitment to the development and maintenance of this open-source
embedded Linux build system. We We are active contributors from Amarula Solutions,
and we have submitted various patches that enhance the functionality and stability
of those project

Merged Patches
^^^^^^^^^^^^^^

Dario Binacchi
""""""""""""""

* Add usr3 led to stm32f769-disco (`<https://patchwork.kernel.org/project/linux-arm-kernel/patch/20250217114513.1098844-2-dario.binacchi@amarulasolutions.com/>`_)

* Add buttons and leds to stm32f746-disco (`<https://patchwork.kernel.org/project/linux-arm-kernel/patch/20250217114332.1098482-2-dario.binacchi@amarulasolutions.com/>`_)

Pending/Review Patches
^^^^^^^^^^^^^^^^^^^^^^

Dario Binacchi
""""""""""""""

* Drop custom compatible from stm32f (`<https://patchwork.ozlabs.org/project/uboot/patch/20250224183931.313491-3-dario.binacchi@amarulasolutions.com/>`_)


**#linux #u-boot #opensource #embedded**


Other opensource contribuitions
-------------------------------

Merged Patches
^^^^^^^^^^^^^^

Andrea Calabrese
""""""""""""""""

* Remove copy operations from classes in Kompute (`<https://github.com/KomputeProject/kompute/pull/412>`_)

* Add noexcept to all constructors to explicitly state no exception thrown (`<https://github.com/KomputeProject/kompute/pull/411>`_)

Michael Trimarchi
"""""""""""""""""

* Rewrite rebuild actions using javascript java injection (`<https://github.com/jenkinsci/pipeline-graph-view-plugin/pull/580>`_)

#jenkins #kompute #opensource #linux
