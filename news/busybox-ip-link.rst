Support the `ip link set' command for CAN interface in Busybox
==============================================================

With the addition of support for the `ip link set' command for the CAN interface in BusyBox, the last missing patch needed to fully interact with a CAN interface on MMU-less systems has finally been merged:
https://www.mail-archive.com/busybox@busybox.net/msg29248.html

So, summarizing, even for MMU-less systems, we can now use the `ip link' command to configure and activate a CAN interface, and the candump and cansend commands to receive and transmit data:

* ip link set can1 type can bitrate 125000 loopback on listen-only on
* ip link set up can1
* candump can1 -L &
* cansend can1 300#AC.AB.AD.AE.75.49.AD.D1

At this point, I should therefore fix and update the slides of my presentation at FOSDEM 2024 following this latest news:
https://fosdem.org/2024/events/attachments/fosdem-2024-2864-linux-can-upstreaming-on-mmu-less-systems/slides/22435/Linux_CAN_upstreaming_on_MMU_less_systems_N5WZk7u.pdf

Meanwhile, I am eager to update and extend my thanks to everyone who made it possible to review and merge all the patches necessary to interact with a CAN interface on MMU-less systems:

Marc Kleine-Budde, Krzysztof Kozłowski, Rob Herring, Vincent Mailhol, Lee Jones, Alexandre Torgue, Simon Horman, Stephen Rothwell, Jakub Kicinski, Paolo Abeni and the kernel test robot :) for **Linux kernel**, Marc Klein-Budde for **can-utils**, Nikolaus Voss, Bernhard Reutner-Fischer and Denys Vlasenko for **busybox**, Florian Westphal and Pablo Neira Ayuso for **libmnl**, Giulio Benetti, Yann E. Morin and Thomas Petazzoni for **buildroot**.

Long live open source!
