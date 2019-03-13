Olimex A64-Olinuxino
=====================

This tutorial will show the details of Olimex A64-Olinuxino board mainline support and other needed details, for more information about hardware and linux-sunxi

Hardware Access

.. image:: /images/a64-olin.jpeg

BSP Build
Manual Build
ATF
U-Boot
Linux
Buildroot
Booting
SD Boot
Linux
USB OTG
Peripheral
Host
RTL8723BS Wifi
Hardware Access
Serial debug and Power connections



BSP Build
Manual Build
Image building need host to ready with all necessary tools ready, refer here

Below are the details of Image build for Olimex A64-Olinuxino board.

ATF

::

        git clone https://github.com/apritzel/arm-trusted-firmware.git
        cd arm-trusted-firmware
        make PLAT=sun50iw1p1 bl31
        export BL31=/path/to/arm-trusted-firmware/build/sun50iw1p1/release/bl31.bin
        
U-Boot

::

        git clone git://git.denx.de/u-boot.git
        cd u-boot
        make a64-olinuxino_defconfig
        make

Linux

::

        git clone git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        cd linux-next
        make mrproper
        ARCH=arm64 make defconfig
        ARCH=arm64 make -j 4 Image dtbs
        ARCH=arm64 make modules && ARCH=arm64 make modules_install

Buildroot
It's easy to build entire system using buildroot and mainline supported a64-olinuxino already. See read this readme.txt for more info.

::

        git clone git://git.busybox.net/buildroot
        cd buildroot
        make olimex_a64_olinuxino_defconfig
        make

Booting
SD Boot
Prepare SD

Linux
USB OTG
Here, we can take mass storage as gadget function and will show how it can work with 'host' and 'peripheral' modes

Build otg mass storage as statically linked module with

`CONFIG_USB_MASS_STORAGE=yi`

Append bootargs with 'g_mass_storage.removable=1 g_mass_storage.luns=1'

Peripheral
Plug USB otg cable A-type to host pc and B-type to bananapi

::

        [    1.952386] usb_phy_generic usb_phy_generic.0.auto: usb_phy_generic.0.auto supply vcc not found, using dummy regulator
        [    1.952954] musb-hdrc musb-hdrc.1.auto: MUSB HDRC host driver
        [    1.952965] musb-hdrc musb-hdrc.1.auto: new USB bus registered, assigned bus number 5
        [    1.957274] hub 5-0:1.0: USB hub found
        [    1.957303] hub 5-0:1.0: 1 port detected
        [    1.961702] Mass Storage Function, version: 2009/09/11
        [    1.961708] LUN: removable file: (no medium)
        [    1.961761] LUN: removable file: (no medium)
        [    1.961764] Number of LUNs=1
        [    1.972523] g_mass_storage gadget: Mass Storage Gadget, version: 2009/09/11
        [    1.972527] g_mass_storage gadget: userspace failed to provide iSerialNumber
        [    1.972530] g_mass_storage gadget: g_mass_storage ready
        # cat /proc/cmdline
        console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p1 rootwait g_mass_storage.removable=1 g_mass_storage.luns=1
        # fdisk -l
        Disk /dev/mmcblk0: 15 GB, 15931539456 bytes, 31116288 sectors
        486192 cylinders, 4 heads, 16 sectors/track
        Units: cylinders of 64 * 512 = 32768 bytes

        Device       Boot StartCHS    EndCHS        StartLBA     EndLBA    Sectors  Size Id Type
        /dev/mmcblk0p1    320,0,1     815,3,16         20480   31116287   31095808 14.8G 83 Linux
        # echo /dev/mmcblk0 > /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/gadget/lun0/file

Access the disk at host pc and write and umount
Host
Plug USB host cable where A-type connect with USB stick and B-type connect to bananapi and

See USB stick detection on bananapi

::

        # cat /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/mode
        b_peripheral
        # echo host > /sys/devices/platform/soc/1c19000.usb/musb-hdrc.1.auto/mode
        [   19.231613] phy phy-1c19400.phy.0: Changing dr_mode to 1
        # [  451.961240] usb 1-1: new high-speed USB device number 2 using ehci-platform
        [  452.133893] usb-storage 1-1:1.0: USB Mass Storage device detected
        [  452.140884] scsi host0: usb-storage 1-1:1.0
        [  453.151349] scsi 0:0:0:0: Direct-Access     Generic  Flash Disk       8.07 PQ: 0 ANSI: 4
        [  453.161156] sd 0:0:0:0: [sda] 15728640 512-byte logical blocks: (8.05 GB/7.50 GiB)
        [  453.169900] sd 0:0:0:0: [sda] Write Protect is off
        [  453.175770] sd 0:0:0:0: [sda] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
        [  453.191292]  sda: sda1
        [  453.197283] sd 0:0:0:0: [sda] Attached SCSI removable disk
        
RTL8723BS Wifi
Enable custom configuration and build buildroot

Build the Linux with `CONFIG_RTL8723BS=m`

Prepare SD card from SD Boot

Clone linux-firmware and copy rtlwifi into rootfs lib/firmware

Insert SD card and power-on

::

        # modprobe -a r8723bs
        [    9.105532] cfg80211: Loading compiled-in X.509 certificates for regulatory database
        [    9.146445] cfg80211: Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
        [    9.154195] platform regulatory.0: Direct firmware load for regulatory.db failed with error -2
        [    9.162867] cfg80211: failed to load regulatory.db
        [   11.397622] r8723bs: module is from the staging directory, the quality is unknown, you have been warned.
        [   11.419119] RTL8723BS: module init start
        [   11.423079] RTL8723BS: rtl8723bs v4.3.5.5_12290.20140916_BTCOEX20140507-4E40
        [   11.430140] RTL8723BS: rtl8723bs BT-Coex version = BTCOEX20140507-4E40
        [   11.437219] pnetdev = ffff80003d222000
        [   11.489920] RTL8723BS: rtw_ndev_init(wlan0)
        [   11.495399] RTL8723BS: module init ret =0

        # ifconfig -a
        lo        Link encap:Local Loopback 
                  inet addr:127.0.0.1  Mask:255.0.0.0
                  inet6 addr: ::1/128 Scope:Host
                  UP LOOPBACK RUNNING  MTU:65536  Metric:1
                  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

        wlan0     Link encap:Ethernet  HWaddr CC:D2:9B:78:F4:52 
                  BROADCAST MULTICAST  MTU:1500  Metric:1
                  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

        # ifconfig wlan0 up
        [   28.884993] rtl8723bs: acquire FW from file:rtlwifi/rtl8723bs_nic.bin
        [   29.080937] random: crng init done
        [   30.219787] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready

        # wpa_passphrase Ji-Fi >> /etc/wpa_supplicant.conf
        (type password and enter)

        # wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf -B
        Successfully initialized wpa_supplicant
        # [   48.465226] RTL8723BS: rtw_set_802_11_connect(wlan0)  fw_state = 0x00000008
        [   48.681824] RTL8723BS: start auth
        [   48.686931] RTL8723BS: auth success, start assoc
        [   48.697104] RTL8723BS: rtw_cfg80211_indicate_connect(wlan0) BSS not found !!
        [   48.704164] RTL8723BS: assoc success
        [   48.711402] RTL8723BS: send eapol packet
        [   48.739960] RTL8723BS: send eapol packet
        [   48.744078] RTL8723BS: set pairwise key camid:4, addr:48:00:33:98:95:1f, kid:0, type:AES
        [   48.744495] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
        [   48.759105] RTL8723BS: set group key camid:5, addr:48:00:33:98:95:1f, kid:1, type:AES

        # udhcpc -i wlan0
        udhcpc: started, v1.27.2
        udhcpc: sending discover
        udhcpc: sending select for 192.168.0.25
        udhcpc: lease of 192.168.0.25 obtained, lease time 604800
        deleting routers
        adding dns 202.88.174.6
        adding dns 202.88.174.8
        # ping google.com
        PING google.com (172.217.26.174): 56 data bytes
        64 bytes from 172.217.26.174: seq=0 ttl=55 time=24.710 ms
        64 bytes from 172.217.26.174: seq=1 ttl=55 time=24.677 ms
