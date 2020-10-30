ENGICAM-PX30-CTOUCH2.0
======================

This is the tutorial for ENGICAM PX30-CTOUCH2.0 carrier board with PX30.Core SOM.

Hardware details and wiki `CTOUCH2.0 Starter Kit <https://www.engicam.com/vis-prod/101365>`_


Hardware Access
---------------

.. image:: /images/engicam-px30-ctouch2-0.jpeg

Program SD
----------

Assume the SD card detected in host via /dev/sda

Flashing::

        git clone https://github.com/amarula/bsp-rockchip.git
        cd bsp-rockchip
        sudo xzcat px30-core-ctouch2-of10-buildroot.img.xz | sudo dd of=/dev/sda
        sync

Insert the Micro SD card on the board microSD slot(J17)

Connect UART port on the board(J26).

Launch minicom at host wih 1152008N1

Power on the kit.

Check the board booting. and enter root at login prompt.

.. code-block:: none

        U-Boot TPL board init
        DDR4, 333MHz
        BW=32 Col=10 Bk=4 BG=2 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
        out

        U-Boot SPL 2020.10 (Oct 30 2020 - 02:55:08 +0530)
        Trying to boot from MMC2
        Card did not respond to voltage select!
        spl: mmc init failed with error: -95
        Trying to boot from MMC1
        NOTICE:  BL31: v2.3(release):
        NOTICE:  BL31: Built : 18:11:03, Oct 29 2020


        U-Boot 2020.10 (Oct 30 2020 - 02:55:08 +0530)

        Model: Engicam PX30.Core C.TOUCH 2.0 10.1" Open Frame
        DRAM:  2 GiB
        PMIC:  RK8090 (on=0x40, off=0x00)
        MMC:   dwmmc@ff370000: 1, dwmmc@ff390000: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial@ff160000
        Out:   serial@ff160000
        Err:   serial@ff160000
        Model: Engicam PX30.Core C.TOUCH 2.0 10.1" Open Frame
        Net:   eth0: ethernet@ff360000
        Hit any key to stop autoboot:  0
        switch to partitions #0, OK
        mmc0(part 0) is current device
        ** No partition table - mmc 0 **
        switch to partitions #0, OK
        mmc1 is current device
        Scanning mmc 1:3...
        Found /extlinux/extlinux.conf
        Retrieving file: /extlinux/extlinux.conf
        197 bytes read in 4 ms (47.9 KiB/s)
        1:      PX30.Core-EDIMM2.2 linux
        Retrieving file: /Image
        31070720 bytes read in 1303 ms (22.7 MiB/s)
        append: earlycon=uart8250,mmio32,0xff160000 root=PARTUUID=e605584d-2513-4fd1-ab25-90cccc9f8ed8 rw rootwait
        Retrieving file: /px30-px30-core-ctouch2-of10.dtb
        40987 bytes read in 5 ms (7.8 MiB/s)
        Moving Image from 0x280000 to 0x400000, end=2230000
        ## Flattened Device Tree blob at 08300000
        Booting using the fdt blob at 0x8300000
        Loading Device Tree to 000000007df28000, end 000000007df3501a ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd042]
        [    0.000000] Linux version 5.10.0-rc1-next-20201028 (ub@ub-XPS-13-9350) (aarch64-buildroot-linux-gnu-gcc.br_real (Buildroot 2020.08-844-g60a98501db) 9.3.0, GNU ld (GNU Binutils) 2
        .34) #1 SMP PREEMPT Thu Oct 29 20:46:48 IST 2020
        [    0.000000] Machine model: Engicam PX30.Core C.TOUCH 2.0 10.1" Open Frame

        Starting network: OK

        Welcome to PX30.Core C.TOUCH2 10.1" OF
        px30-core-ctouch-of10 login: root
        #

Program eMMC
------------

Connect USB otg cable A-type to host pc, Micro USB end to board.

Close Jumper JM5.

Boot the Kit with SD boot.

Program eMMC in U-Boot.

At Target::

        mmc dev 0
        gpt write mmc 0 $partitions
        fastboot 0

Copy boot images from /boot of rootfs partition of buildroot img.

At host::

        lsusb | grep 2207
        sudo fastboot -i 0x2207 flash loader1 idbloader.img
        sudo fastboot -i 0x2207 flash loader2 u-boot.itb

WIFI/BT
-------

Testing WiFi on the target.

.. code-block:: none

        # ifconfig -a | grep wlan0
        wlan0     Link encap:Ethernet  HWaddr 00:25:CA:2D:2E:91
                  BROADCAST MULTICAST  MTU:1500  Metric:1
                  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

        # ifconfig wlan0 up
        # iw dev wlan0 scan | grep SSID
                SSID: TP-Link_6DA4
                SSID: SiriVista501
                SSID: dlink-A430

        # wpa_passphrase "SSID name" "SSID Password" >> /etc/wpa_supplicant.conf

        # wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
        Successfully initialized wpa_supplicant
        # [  580.535821] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready

        # udhcpc -i wlan0
        udhcpc: started, v1.32.0
        udhcpc: sending discover
        udhcpc: sending select for 192.168.1.5
        udhcpc: lease of 192.168.1.5 obtained, lease time 86400
        deleting routers
        adding dns 192.168.1.1

        # ping 8.8.8.8
        PING 8.8.8.8 (8.8.8.8): 56 data bytes
        64 bytes from 8.8.8.8: seq=0 ttl=119 time=29.269 ms
        64 bytes from 8.8.8.8: seq=1 ttl=119 time=26.163 ms
        64 bytes from 8.8.8.8: seq=2 ttl=119 time=23.070 ms

Testing Bluetooth on the target.

.. code-block:: none

        # hciconfig -a
        [  605.701708] Bluetooth: Core ver 2.22
        [  605.709923] NET: Registered protocol family 31
        [  605.718930] Bluetooth: HCI device and connection manager initialized
        [  605.729967] Bluetooth: HCI socket layer initialized
        [  605.739499] Bluetooth: L2CAP socket layer initialized
        [  605.749121] Bluetooth: SCO socket layer initialized

        # hciattach /dev/ttyUSB0 bcm43xx 921600
        bcm43xx_init
        Set Controller UART speed to 921600 bit/s
        Flash firmware /lib/firmware/brcm/BCM43430A1.hcd
        Set Controller UART speed to 921600 bit/s
        [  627.490432] Bluetooth: HCI UART driver ver 2.3
        [  627.499424] Bluetooth: HCI UART protocol H4 registered
        [  627.509078] Bluetooth: HCI UART protocol LL registered
        [  627.519087] Bluetooth: HCI UART protocol Broadcom registered
        [  627.529106] Bluetooth: HCI UART protocol QCA registered
        Device setup complete

        # hciconfig hci0 up piscan
        # hciconfig -a
        hci0:   Type: Primary  Bus: UART
                BD Address: 00:25:CA:2D:2E:92  ACL MTU: 1021:8  SCO MTU: 64:1
                UP RUNNING PSCAN ISCAN
                RX bytes:1377 acl:0 sco:0 events:73 errors:0
                TX bytes:867 acl:0 sco:0 commands:73 errors:0
                Features: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
                Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3
                Link policy: RSWITCH SNIFF
                Link mode: SLAVE ACCEPT
                Name: 'BCM4343WA1 37.4MHz Laird Linux BT4.2-0119'
                Class: 0x000000
                Service Classes: Unspecified
                Device Class: Miscellaneous,
                HCI Version: 4.2 (0x8)  Revision: 0x1d8
                LMP Version: 4.2 (0x8)  Subversion: 0x2209
                Manufacturer: Broadcom Corporation (15)

        # hcitool scan
        Scanning ...
                BC:9F:EF:F2:2F:CB       Arya_iPhone

        # /usr/libexec/bluetooth/bluetoothd &
        # [  764.238352] NET: Registered protocol family 38

        # bt-adapter -d
        Searching...
        [11:9F:23:F2:F5:AH]
        Name: Arya_iPhone
        Alias: Arya_iPhone
        Address: 11:9F:23:F2:F5:AH
        Icon: phone
        Class: 0x7a020c
        LegacyPairing: 0
        Paired: 0
        RSSI: -37

        # bt-device -c 11:9F:23:F2:F5:AH
        Connecting to: 11:9F:23:F2:F5:AH
        Device: Arya_iPhone (11:9F:23:F2:F5:AH)
        Confirm passkey: 567321 (yes/no)? yes
        connected

Linux USB OTG
-------------

Connect USB otg cable A-type to host pc, Micro USB end to board.

Close Jumper JM5.

At Target::

        # fdisk -l
        Disk /dev/mmcblk0: 3796 MB, 3980394496 bytes, 7774208 sectors
        121472 cylinders, 4 heads, 16 sectors/track
        Units: sectors of 1 * 512 = 512 bytes

        Device       Boot StartCHS    EndCHS        StartLBA     EndLBA    Sectors  Size Id Type
        /dev/mmcblk0p1 *  2,10,9      6,30,24          32768      98303      65536 32.0M  c Win95 FAT32 (LBA)
        /dev/mmcblk0p2    0,0,2       0,0,34               1         33         33 16896 ee EFI GPT

        Partition table entries are not in disk order
        Disk /dev/mmcblk2: 7456 MB, 7818182656 bytes, 15269888 sectors
        238592 cylinders, 4 heads, 16 sectors/track
        Units: sectors of 1 * 512 = 512 bytes

        Disk /dev/mmcblk2 doesn't contain a valid partition table

        # echo /dev/mmcblk2 > /sys/devices/platform/ff300000.usb/gadget/lun0/file

        # [   55.912084] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.030006] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.042477] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 0)
        [   56.055034] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.174016] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.186105] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 0)
        [   56.199436] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.318007] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.329719] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 0)
        [   56.341557] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.458056] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 1)
        [   56.469340] dwc2 ff300000.usb: dwc2_hsotg_ep_sethalt(ep 0000000006ae2021 ep1in, 0)


At Host::

        $ sudo fdisk -l

        Disk /dev/sdb: 7.3 GiB, 7818182656 bytes, 15269888 sectors
        Units: sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes

On host /dev/mmcblk2 will be detected as a storage device.
