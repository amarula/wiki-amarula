Amarula Solutions: Smart Thermostat Demo
========================================

.. note:: **TL;DR**
   - Dual-board prototype combining **Yocto Scarthgap on STM32MP257** (Flutter GUI) and **Zephyr 4.0.0 on STM32F429I-DISC1** (LVGL GUI, I2C sensors) — communicating over **CAN Bus**.
   - Showcases **end-to-end embedded systems development**: sensor integration, real-time communication, cross-platform GUI design, and upstream-first methodology.

.. image:: /images/flyer_image.png
   :alt: Amarula Solutions Logo and Smart Thermostat Demo Overview

|
|

Amarula Solutions presented a demo showcasing a smart thermostat powered by a combination of cutting-edge technologies: Yocto, Zephyr, Flutter, and LVGL. This demo highlights their expertise in developing embedded systems with modern Graphical User Interfaces (GUIs) on ST platforms, utilizing the latest Long Term Support (LTS) Board Support Packages (BSPs).

How is the dual-board hardware architected?
-------------------------------------------
The demo utilizes two ST boards:

* **STM32MP257 Board:** This board runs a Flutter application on a Linux BSP built with the latest Yocto LTS release (Scarthgap).
* **STM32F429I-DISC1 Board:** This board reads humidity, pressure, and temperature sensors via I2C and runs a GUI powered by LVGL on Zephyr OS (4.0.0).

How do the boards communicate and what functionality do they provide?
---------------------------------------------------------------------
The two boards communicate via CAN, creating a prototype of a smart thermostat with integrated weather station functionality. Sensor data is displayed on both GUIs. The system is designed for dynamic adjustments to heating, cooling, or ventilation based on real-time data.  The Flutter application also integrates a real-time weather forecast page using OpenWeatherMap.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
What expertise does Amarula Solutions bring?
--------------------------------------------
Amarula Solutions offers comprehensive embedded systems development, including:

* Custom Sensor Board & CAN Hardware Setup
* Operating Systems Development
* User Interface Design & Programming
* Upstreaming Patches for Zephyr, Kernel, and Yocto

This demo exemplifies Amarula's ability to deliver end-to-end embedded solutions for custom products.

Where can you find us?
----------------------
Visit Amarula Solutions at Hall 3, Booth 3-336.

Contact
-------
www.amarulasolutions.com
Joop Geesinkweg 125, 1114 AB Amsterdam, The Netherlands
Via le Canevare 30, 31100 Treviso (TV), Italy
Via Felice Cavallotti 25, 41012 Carpi (MO), Italy

.. tip::
   Interested in multi-platform embedded solutions combining Linux and RTOS?
   Amarula Solutions specializes in Yocto/Zephyr integration, CAN bus communication,
   and custom GUI development with Flutter and LVGL.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
