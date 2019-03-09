RISC V
======

Testing RISC V under qemu
Build and Install

Building the full system emulator and the user mode emulator on Linux:

::

        git clone --recursive https://github.com/riscv/riscv-qemu.git
        cd riscv-qemu
        ./configure \
            --target-list=riscv64-softmmu,riscv32-softmmu,riscv64-linux-user,riscv32-linux-user
        make -j$(nproc)
        # last operation require root right, so possible that you need sudo make install
        make install
         
        # it will be installed under /usr/local/bin so you need to add your path if it's in the default one

Use a working buildroot environment

Download buildroot project for risc-v

::

        git clone https://github.com/riscv/riscv-buildroot.git
        git checkout origin/riscv-start

Build buildroot enviroment

::

        cd riscv-buildroot
        make qemu_riscv64_virt_defconfig
        make

This configuration let you work on version downloaded in the configuration

Use mainline kernel

::

        # create local.mk file inside your buildroot directory
         
        echo "LINUX_OVERRIDE_SRCDIR=linux-mainline" > local.mk
         
        git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git linux-mainline
         
        # checkout the mainline commit id or tag you need for example
        cd linux-mainline
        git checkout v4.20-rc7 -b devel-riscv
         
        # if you system is already build
        make linux-dirclean
        make
         
        # otherwise follow the instruction on previous section
        make qemu_riscv64_virt_defconfig
        make
         
         
        # configure the kernel
        make linux-menuconfig

Run your built image

Your output image are in output/images. In order to execute just run:

::

        qemu-system-riscv64 -M virt -kernel output/images/bbl -append "root=/dev/vda ro console=ttyS0" -drive file=output/images/rootfs.ext2,format=raw,id=hd0 -device virtio-blk-device,drive=hd0 -netdev user,id=net0 -device virtio-net-device,netdev=net0 -nographic
