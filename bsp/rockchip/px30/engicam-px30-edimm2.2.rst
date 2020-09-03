ENGICAM-PX30-EDIMM2.2
=====================

This is the tutorial for ENGICAM PX30-EDIMM2.2 carrier board with PX30.Core SOM.

Hardware details and wiki `EDIMM2.2 Starter Kit <https://www.engicam.com/vis-prod/101366>`_


Hardware Access
---------------

.. image:: /images/engicam-px30-edimm2-2.jpeg

Download Images
---------------

::
        $ git clone https://github.com/amarula/bsp-rockchip.git


SD/EMMC Boot
------------

From the bsp-rockchip directory, flash engicam-edimm22-br.img.xz on to micro sd

::

	$ sudo xzcat engicam-edimm22-br.img.xz | sudo dd of=/dev/devicefile status=progress (devicefile => sudo fdisk -l)
	$ sync

Put the micro-SD card onto the carrier board slot with jumper JM1 closed, power the board. Boot log is as follows:


::

        MMC:   dwmmc@ff370000: 1, dwmmc@ff390000: 0
        Loading Environment from MMC... *** Warning - bad CRC, using default environment

        In:    serial@ff160000
        Out:   serial@ff160000
        Err:   serial@ff160000
        Model: Engicam PX30.Core EDIMM2.2 Starter Kit
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
        245 bytes read in 4 ms (59.6 KiB/s)
        1:      Engicam_CTOUCH2.0 linux
        Retrieving file: /Image
        30880256 bytes read in 1298 ms (22.7 MiB/s)
        append: earlycon=uart8250,mmio32,0xff160000 root=PARTUUID=0A343564-BD2C-4F74-AD16-B44209B9A821 rw rootwait g_mass_storage.removable=1 g_mass_st
        orage.luns=1
        Retrieving file: /px30-px30-core-edimm2.2.dtb
        40987 bytes read in 5 ms (7.8 MiB/s)
        Moving Image from 0x280000 to 0x400000, end=2200000
        ## Flattened Device Tree blob at 08300000
           Booting using the fdt blob at 0x8300000
           Loading Device Tree to 000000007df3d000, end 000000007df4a01a ... OK

        Starting kernel ...

        [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd042]
        [    0.000000] Linux version 5.8.0-rc1 (suniel@suniel-P5WE0) (aarch64-buildroot-linux-uclibc-gcc.br_real (Buildroot 2020.08-rc1-108-g51a8edc) 9
        .3.0, GNU ld (GNU Binutils) 2.33.1) #4 SMP PREEMPT Wed Sep 2 21:42:26 IST 2020
        [    0.000000] Machine model: Engicam PX30.Core EDIMM2.2 Starter Kit
        [    0.000000] earlycon: uart8250 at MMIO32 0x00000000ff160000 (options '')
        [    0.000000] printk: bootconsole [uart8250] enabled
        [    0.000000] efi: UEFI not found.
        [    0.000000] cma: Reserved 32 MiB at 0x000000007e000000
        [    0.000000] NUMA: No NUMA configuration found
        [    0.000000] NUMA: Faking a node at [mem 0x0000000000200000-0x000000007fffffff]
        [    0.000000] NUMA: NODE_DATA [mem 0x7dbbd100-0x7dbbefff]
        [    0.000000] Zone ranges:
        [    0.000000]   DMA      [mem 0x0000000000200000-0x000000003fffffff]
        [    0.000000]   DMA32    [mem 0x0000000040000000-0x000000007fffffff]
        [    0.000000]   Normal   empty
        .........
        .........
        .........
        .........
        [    4.681736] libphy: stmmac: probed
        [    4.688282] mdio_bus stmmac-0:00: attached PHY driver [unbound] (mii_bus:phy_addr=stmmac-0:00, irq=POLL)
        [    4.729925] rk808-rtc rk808-rtc: registered as rtc0
        [    4.741500] rk808-rtc rk808-rtc: setting system clock to 2017-08-05T09:00:08 UTC (1501923608)
        [    4.797317] cfg80211: Loading compiled-in X.509 certificates for regulatory database
        [    4.860334] cfg80211: Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
        [    4.913118] brcmfmac: brcmf_fw_alloc_request: using brcm/brcmfmac43430-sdio for chip BCM43430/1
        [    4.931532] usbcore: registered new interface driver cp210x
        [    4.940912] usbserial: USB Serial support registered for cp210x
        [    4.951208] cp210x 2-1.7:1.0: cp210x converter detected
        [    4.963892] usb 2-1.7: cp210x converter now attached to ttyUSB0
        Initializing random number generator: OK
        Saving random seed: [    5.008456] random: dd: uninitialized urandom read (512 bytes read)
        OK
        Starting system message bus: [    5.072978] random: dbus-uuidgen: uninitialized urandom read (12 bytes read)
        [    5.084575] random: dbus-uuidgen: uninitialized urandom read (8 bytes read)
        [    5.084762] brcmfmac: brcmf_fw_alloc_request: using brcm/brcmfmac43430-sdio for chip BCM43430/1
        [    5.112855] brcmfmac: brcmf_c_preinit_dcmds: Firmware: BCM43430/1 wl0: Oct 22 2019 01:57:42 version 7.45.98.94 (r723000 CY) FWID 01-73a5ed62
        done
        Starting network: [    5.251914] NET: Registered protocol family 10
        [    5.262230] Segment Routing with IPv6
        udhcpc: started, v1.32.0
        [    5.302920] rk_gmac-dwmac ff360000.ethernet eth0: PHY [stmmac-0:00] driver [Generic PHY] (irq=POLL)
        [    5.329666] rk_gmac-dwmac ff360000.ethernet eth0: No Safety Features support found
        [    5.341991] rk_gmac-dwmac ff360000.ethernet eth0: PTP not supported by HW
        [    5.353425] rk_gmac-dwmac ff360000.ethernet eth0: configuring for phy/rmii link mode
        udhcpc: sending discover
        [    8.224853] dwc2 ff300000.usb: new device is high-speed
        [    8.305259] dwc2 ff300000.usb: new device is high-speed
        [    8.373704] dwc2 ff300000.usb: new address 84
        udhcpc: sending discover
        udhcpc: sending discover
        udhcpc: no lease, forking to background
        OK
        Starting ntpd: OK

        Welcome to ENGICAM-DIMM2.2..!!
        engicam-dimm2.2 login: root
        #

use root for login.

WIFI/BT Test:
------------

::

        # ifconfig -a

        eth0      Link encap:Ethernet  HWaddr 6A:E6:D0:1A:73:9C
                  UP BROADCAST MULTICAST  MTU:1500  Metric:1
                  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
                  Interrupt:19

        lo        Link encap:Local Loopback
                  inet addr:127.0.0.1  Mask:255.0.0.0
                  inet6 addr: ::1/128 Scope:Host
                  UP LOOPBACK RUNNING  MTU:65536  Metric:1
                  RX packets:384 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:384 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:28416 (27.7 KiB)  TX bytes:28416 (27.7 KiB)

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

Plug USB otg cable A-type to host pc, Micro USB end to carrier board OTG port and close Jumper JM5. Power on the board

::

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

On host /dev/mmcblk2 will be detected as a storage device.

::

        $ sudo fdisk -l

        Disk /dev/sdb: 7.3 GiB, 7818182656 bytes, 15269888 sectors
        Units: sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
