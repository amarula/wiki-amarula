MIPI DSI
########

More details at, https://mipi.org/specifications/dsi

`Allwinner MIPI-DSI Pipeline <https://static.linaro.org/connect/lvc21f/presentations/LVC21F-223.pdf>`_

Allwinner MIPI-DSI Pipeline
This is sample demo work for running Allwinner A64 MIPI-DSI panel on Mainline Linux-4.19.0-rc5.
 
Bananapi S070WV20-CT16 MIPI-DSI DSI panel connected via board DSI port with
- DC1SW as AVDD supply
- DCDC1 as DVDD supply
- PD6 gpio for reset pin
- PD5 gpio for backlight enable pin
- PD7 gpio for backlight vdd supply
Initial patch version is submitted to Linux mailing-list https://lkml.org/lkml/2018/9/27/750

.. image:: /images/mipi.jpg

