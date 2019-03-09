SPL HABv4
=========

Since, the i.MX6 Secure Boot used u-boot-dtb.imx but this tutorial describe the Secure Boot(HAB) for SPL as well as a singable version of the U-Boot image.

The signature can be verified through High Assurance Boot (HAB).

    Build
    Generate Signed SPL
    Generate U-Boot-IVT
    Write on SD
    Read e-FUSE
    Write e-FUSE
    Close device

Build

::

        bash> git clone https://github.com/openedev/u-boot-amarula.git -b falcon-hab

        bash> cd u-boot-amarula

        bash> make imx6dl_icore_mmc_defconfig

        bash> make


        bash> cat SPL.log

        Image Type:   Freescale IMX Boot Image

        Image Ver:    2 (i.MX53/6/7 compatible)

        Mode:         DCD

        Data Size:    53248 Bytes = 52.00 KiB = 0.05 MiB

        Load Address: 00907420

        Entry Point:  00908000

        HAB Blocks:   00907400 00000000 0000ac00

        DCD Blocks:   00910000 0000002c 00000004

        bash> cat u-boot-ivt.img.log

        Image Name:   U-Boot 2017.05-00002-g5ab54f3 fo

        Created:      Tue Jul  4 13:55:05 2017

        Image Type:   ARM U-Boot Firmware with HABv4 IVT (uncompressed)

        Data Size:    417728 Bytes = 407.94 KiB = 0.40 MiB

        Load Address: 17800000

        Entry Point:  00000000

        HAB Blocks:   0x177fffc0   0x0000   0x00064020

Generate Signed SPL

First create PKI keys from here and proceed with below steps

::

        bash> cd ~/cst-2.3.2/linux64

        # Create csf
        bash> cat SPL.CSF

        [Header]

        Version = 4.1

        Security Configuration = Open

        Hash Algorithm = sha256

        Engine Configuration = 0

        Certificate Format = X509

        Signature Format = CMS

        Engine = CAAM


        [Install SRK]

        File = "../crts/SRK_1_2_3_4_table.bin"

        Source index = 0


        [Install CSFK]

        File = "../crts/CSF1_1_sha256_2048_65537_v3_usr_crt.pem"


        [Authenticate CSF]


        [Install Key]

        # Key slot index used to authenticate the key to be installed

        Verification index = 0


        # Key to install

        Target index = 2

        File = "../crts/IMG1_1_sha256_2048_65537_v3_usr_crt.pem"


        [Authenticate Data]

        Verification index = 2

        Blocks = 0x00907400 0x0 0x0ac00 "SPL"


        # Create csf bin
        bash> ./cst --o SPL_CSF.bin --i SPL.CSF

        CSF Processed successfully and signed data available in SPL_CSF.bin

        # Attach the 0x2000 pad
        bash> objcopy -I binary -O binary --pad-to 0x2000 --gap-fill=0x00 SPL_CSF.bin SPL_CSF_pad.bin

        # Create signed SPL
        bash> cat SPL SPL_CSF_pad.bin > SPL-signed

Generate U-Boot-IVT

::

        bash> cd ~/cst-2.3.2/linux64

        # Create csf
        bash> cat u-boot-ivt.CSF

        [Header]

        Version = 4.1

        Security Configuration = Open

        Hash Algorithm = sha256

        Engine Configuration = 0

        Certificate Format = X509

        Signature Format = CMS

        Engine = CAAM


        [Install SRK]

        File = "../crts/SRK_1_2_3_4_table.bin"

        Source index = 0


        [Install CSFK]

        File = "../crts/CSF1_1_sha256_2048_65537_v3_usr_crt.pem"


        [Authenticate CSF]


        [Install Key]

        # Key slot index used to authenticate the key to be installed

        Verification index = 0


        # Key to install

        Target index = 2

        File = "../crts/IMG1_1_sha256_2048_65537_v3_usr_crt.pem"


        [Authenticate Data]

        Verification index = 2

        Blocks = 0x177fffc0 0x0 0x00064020 "u-boot-ivt.img"


        # Create csf bin
        bash> ./cst --o u-boot-ivt_CSF.bin --i u-boot-ivt.CSF

        CSF Processed successfully and signed data available in u-boot-ivt_CSF.bin

        # Attach the 0x2000 pad
        bash> objcopy -I binary -O binary --pad-to 0x2000 --gap-fill=0x00 u-boot-ivt_CSF.bin u-boot-ivt_CSF_pad.bin

        # Create signed U-Boot
        bash> cat u-boot-ivt.img u-boot-ivt_CSF_pad.bin > u-boot-ivt-signed.img

Write on SD

::

        bash> DEV=/dev/mmcblk0
        bash> sudo dd if=/dev/zero of=$DEV count=1 bs=1M oflag=sync status=none && sync
        bash> sudo dd if=SPL-signed of=$DEV bs=1K seek=1 oflag=sync status=none && sync
        bash> sudo dd if=u-boot-ivt-signed.img of=$DEV bs=1K seek=69 oflag=sync status=none && sync

Read e-FUSE

::

        bash> cd ~/cst-2.3.2/crts

        bash> hexdump -e '/4 "0x"' -e '/4 "%X""\n"' < SRK_1_2_3_4_fuse.bin

        0xBB64EF1F

        0x7C21ED82

        0x7D9E255A

        0xD9D3A409

        0x879E0CFB

        0xB3D7202D

        0xEC8D7223

        0xEA226AAD

Write e-FUSE

::

        U-Boot SPL 2017.05-00002-g5ab54f3 (Jul 04 2017 - 13:54:49)

        >>spl:board_init_r()

        spl_early_init()

        Trying to boot from MMC1

        spl: payload image: U-Bo load addr: 0x177fffc0 size: 417792

        Jumping to U-Boot

        loaded - jumping to U-Boot...

        hab fuse not enabled


        U-Boot 2017.05-00002-g5ab54f3 (Jul 04 2017 - 13:54:49 +0530)


        CPU:   Freescale i.MX6SOLO rev1.3 at 792MHz

        CPU:   Industrial temperature grade (-40C to 105C) at 38C

        Reset cause: POR

        Model: Engicam i.CoreM6 DualLite/Solo Starter Kit

        DRAM:  256 MiB

        MMC:   FSL_SDHC: 0

        *** Warning - bad CRC, using default environment


        No panel detected: default to Amp-WD

        Display: Amp-WD (800x480)

        In:    serial

        Out:   serial

        Err:   serial

        Net:   

        Error: ethernet@02188000 address not set.

        No ethernet found.

        Hit any key to stop autoboot:  0

        icorem6qdl> fuse prog -y 3 0 0xBB64EF1F

        Programming bank 3 word 0x00000000 to 0xbb64ef1f...

        icorem6qdl> fuse prog -y 3 1 0x7C21ED82

        Programming bank 3 word 0x00000001 to 0x7c21ed82...

        icorem6qdl> fuse prog -y 3 2 0x7D9E255A

        Programming bank 3 word 0x00000002 to 0x7d9e255a...

        icorem6qdl> fuse prog -y 3 3 0xD9D3A409

        Programming bank 3 word 0x00000003 to 0xd9d3a409...

        icorem6qdl> fuse prog -y 3 4 0x879E0CFB

        Programming bank 3 word 0x00000004 to 0x879e0cfb...

        icorem6qdl> fuse prog -y 3 5 0xB3D7202D

        Programming bank 3 word 0x00000005 to 0xb3d7202d...

        icorem6qdl> fuse prog -y 3 6 0xEC8D7223

        Programming bank 3 word 0x00000006 to 0xec8d7223...

        icorem6qdl> fuse prog -y 3 7 0xEA226AAD

        Programming bank 3 word 0x00000007 to 0xea226aad...

Close device

::

        icorem6qdl> hab_status

        Secure boot disabled

        HAB Configuration: 0xf0, HAB State: 0x66

        No HAB Events Found!

        icorem6qdl> fuse prog 0 6 0x2

        Programming bank 0 word 0x00000006 to 0x00000002...

        Warning: Programming fuses is an irreversible operation!

                 This may brick your system.

                 Use this command only if you are sure of what you are doing!


        Really perform this fuse programming? <y/N>

        y

        icorem6qdl> reset

        resetting ...


        U-Boot SPL 2017.05-00002-g5ab54f3 (Jul 04 2017 - 13:54:49)

        >>spl:board_init_r()

        spl_early_init()

        Trying to boot from MMC1

        spl: payload image: U-Bo load addr: 0x177fffc0 size: 417792

        Jumping to U-Boot

        loaded - jumping to U-Boot...


        Authenticate image from DDR location 0x177fffc0...


        U-Boot 2017.05-00002-g5ab54f3 (Jul 04 2017 - 13:54:49 +0530)


        CPU:   Freescale i.MX6SOLO rev1.3 at 792MHz

        CPU:   Industrial temperature grade (-40C to 105C) at 60C

        Reset cause: POR

        Model: Engicam i.CoreM6 DualLite/Solo Starter Kit

        DRAM:  256 MiB

        MMC:   FSL_SDHC: 0

        *** Warning - bad CRC, using default environment


        No panel detected: default to Amp-WD

        Display: Amp-WD (800x480)

        In:    serial

        Out:   serial

        Err:   serial

        Net:   

        Error: ethernet@02188000 address not set.

        No ethernet found.

        Hit any key to stop autoboot:  0

        icorem6qdl> hab_status


        Secure boot enabled


        HAB Configuration: 0xcc, HAB State: 0x99

        No HAB Events Found!

