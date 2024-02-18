Sandbox
#######


Sandbox is good example to familiar with U-Boot and related functionalities.

Build
*****
::

        $ git clone git://git.denx.de/u-boot.git
        $ cd u-boot
        $ make sandbox_defconfig all NO_SDL=1

Run
***
::

        $ ./u-boot

        U-Boot 2017.09-00364-g05eb54a-dirty (Oct 04 2017 - 23:12:50 +0530)


        DRAM:  128 MiB

        MMC:   

        Using default environment


        In:    serial

        Out:   serial

        Err:   serial

        SCSI:  Net:   No ethernet found.

        IDE:   Bus 0: not available  

        => bdinfo

        boot_params = 0x00000000

        DRAM bank   = 0x00000000

        -> start    = 0x00000000

        -> size     = 0x08000000

        ethaddr     = 00:00:11:22:33:44

        IP addr     = 1.2.3.4

With Sandbox approach, we can further emulate the SPI, Disk, I2C etc., See board/sandbox/README.sandbox for more details.
        
Test
****
Sandbox drivers can be available in each peripheral area for basic sanity, below is the procedure to test the same.
        
Configure
=========
::

        $ cd /path/to/u-boot
        $ sudo apt-get install python python-virtualenv
        $ virtualenv venv
        $ . ./venv/bin/activate
        $ pip install pytest

To test sandbox

::

        $ ./test/py/test.py --bd sandbox --build

        To test driver model test in sandbox

        $ ./test/py/test.py --bd sandbox --build -k ut_dm
