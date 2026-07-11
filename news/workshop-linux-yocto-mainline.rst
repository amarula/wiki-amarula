Proposal: Boot the board up with latest linux mainline
======================================================

.. note:: **TL;DR**
   - Practical workshop challenges for **mainline kernel bring-up** on **SpacemiT K1 RISC-V** (Banana Pi CM6, Orange Pi R2S) — covering device tree authoring, b4 patch submission, Yocto with meta-riscv, and upstream contribution workflows.
   - Achievements include kernel dependency fixes, meta-riscv pull requests, and upstream collaboration with RISC-V maintainers.

**Banana Pi CM6 - SoC: SpacemiT K1**
------------------------------------
0. Find an image to boot the board (tipically from Banana Pi)
1. Compile the mainline kernel and try to boot it with a device tree from a similar board (same SoC)
2. Write a basic device tree for it
3. Boot it up
4. Find a way to have a clean implementation of the device tree (reusing stuff from banana Pi f3)
5. Check what is supported
6. Prepare a patch and send it (tool: b4)
7. Build an image with yocto using meta-risc V
8. Send a patch for meta-risc V

**R2S board support (Orange pi R2S) - SoC: SpacemiT K1 Risc-V**
----------------------------------------------------------------
1. build an image with yocto using meta Risc-V
2. modify the device tree to add PCI Express support
3. check that the 2.5 gb Interfaces are available
4. test the performances with iPerf 3
5. submit the patches to the upstream kernel maintainers
6. send the patch to meta risc-v for yocto

What were the achievements?
---------------------------
1. We add it our Tested By and reported a possible missing dependencies: https://lore.kernel.org/linux-riscv/CA+Xcp4nY9GVMOmtMG-PNhY2vqP4Cc_amAMSa+M3vuDjWUkuCHw@mail.gmail.com/. We noticed that it only works when CONFIG_I2C_K1 is enabled because it's necessary to enable the regulators used by the mmc controller. We proposed to add the dependency between CONFIG_MMC_SDHCI_OF_K1 and CONFIG_I2C_K1.
2. Pull request from Eduardo to meta-riscv https://github.com/riscv/meta-riscv/pull/629 to fix the server issue for yocto builds. Previously it was using the chinese server gitee which is slow or inaccessible from us. We proposed a fix by using amarula's github.
3. All the k1 board that use mainline kernel have a small issue which is that in yocto recipe for mainline kernel, there are two configuration fragments for CONFIG_IC2_K1 used both as module (=m) but also as built in (=y). We sent a patch to fix this contraddiction. https://github.com/riscv/meta-riscv/pull/630
4. We obtained a reply from Iker, it can be checked at this link

.. tip::
   Want to bring up mainline Linux on your custom hardware? Amarula Solutions
   offers RISC-V and ARM mainline kernel porting, device tree development,
   and Yocto BSP integration services.
   `Contact our BSP team <https://www.amarulasolutions.com/contact/>`_
