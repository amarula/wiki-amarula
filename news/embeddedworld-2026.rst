Next-Generation Integrated Smart Thermostat & Weather Station
=============================================================

.. note:: **TL;DR**
   - Amarula Solutions presents a unified **Smart Thermostat and Weather Station** powered by **STM32MP2, Yocto Scarthgap, and Flutter** — with onboard temperature, humidity, and pressure sensors, CAN Bus connectivity, and cloud integration via OpenWeatherMap.
   - Demonstrates full-stack capability: **custom PCB design, 3D enclosure modeling, Linux BSP development, and Flutter GUI** — all presented at Embedded World 2026.

.. image:: /images/flyer_image.png
   :alt: Amarula Solutions Logo and Smart Thermostat Demo Overview

|
|

Amarula Solutions is proud to present our latest innovation: a fully integrated, all-in-one Smart Thermostat
and Weather Station. Evolving from our previous multi-board prototypes, this new showcase demonstrates our
comprehensive ability to design, build, and deploy complete embedded solutions from the bare metal to the final user interface.

.. image:: /images/ew2026-weather-station-4.png
   :alt: Front view of the unified Smart Thermostat

|
|

By consolidating powerful processing and environmental sensing into a single, beautifully designed custom
hardware enclosure, we are pushing the boundaries of what is possible with modern Graphical User Interfaces (GUIs) on STMicroelectronics platforms.

How did we evolve from a multi-board prototype to a unified design?
-------------------------------------------------------------------
Our previous iteration utilized separate boards to handle Linux-based UI tasks and RTOS-based sensor readings.
 Our new design brings everything under one roof.

Housed in a custom-designed, light blue mechanical enclosure with an integrated stand, the new system features
a bespoke PCB designed entirely in-house. Key hardware highlights include:

* **Centralized Processing:** Powered by the STM32MP2 microprocessor, handling complex tasks and fluid graphics effortlessly.
* **Onboard Environmental Sensing:** We have directly integrated sensors onto two small PCB—clearly mapped for
  **Temperature & Humidity**, and **Pressure**.
* **Robust Connectivity:** An onboard **CAN Bus** interface ensures the thermostat can seamlessly communicate with
  broader industrial or smart home networks.

How does the software stack enable smart functionality?
-------------------------------------------------------
Running on a robust Linux Board Support Package (BSP) built with the latest Yocto LTS release (Scarthgap), the
device boasts a stunning, highly responsive GUI powered by **Flutter**.

* **Real-Time Environment Control:** The system reads onboard sensor data instantly, designed to trigger dynamic
  adjustments for heating, cooling, or ventilation.
* **Cloud Integration:** The Flutter application seamlessly integrates real-time local weather forecasts using
  the OpenWeatherMap API, giving users a complete picture of both indoor and outdoor climates.

What is our end-to-end expertise?
---------------------------------
This unified design exemplifies Amarula Solutions' capability to act as a full-stack partner for custom embedded products. Our expertise spans:

* **Hardware & Mechanical Design:** Custom PCB layout, sensor integration, and 3D enclosure modeling.
* **Operating Systems Development:** Building highly tailored, secure, and optimized Yocto Linux images.
* **User Interface Design:** Crafting modern, fluid, and intuitive applications using Flutter.
* **Open Source Contribution:** Upstreaming patches for the Linux Kernel and Yocto project to ensure long-term stability and community support.

Where can you see the demo?
---------------------------
Experience the new integrated Smart Thermostat firsthand. Visit Amarula Solutions at **Hall 3 / Booth Number 3-336**.

Contact
-------
* **Web:** `www.amarulasolutions.com <https://www.amarulasolutions.com>`_
* **The Netherlands:** Joop Geesinkweg 125, 1114 AB Amsterdam
* **Italy (Treviso):** Via le Canevare 30, 31100 Treviso (TV)
* **Italy (Carpi):** Via Felice Cavallotti 25, 41012 Carpi (MO)

.. tip::
   Need a full-stack embedded product like this Smart Thermostat? Amarula Solutions
   delivers custom hardware design, Yocto BSPs, and Flutter UI development —
   from prototype to production.
   `Contact our engineering team <https://www.amarulasolutions.com/contact/>`_
