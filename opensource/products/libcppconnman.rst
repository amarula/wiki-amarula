Amarula Libcppconnman
=====================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


.. |Amarula| replace:: `Amarula Solutions <https//www.amarulasolutions.com>`__
.. |libcppconnman| replace:: `Libcppconnman <https://github.com/amarula/libcppconnman>`__
.. |ConnMan| replace:: ConnMan

    
|Amarula| is an engineering company specializing in :strong:`embedded systems`, with a deep focus on :strong:`Linux` 
and :strong:`open-source software`. Founded in Amsterdam in 2009, the company provides comprehensive engineering 
services, including software development, hardware design, and consulting. Their expertise spans areas like Linux 
kernel porting, driver development, operating system optimization, and user interface development using frameworks 
like :strong:`Qt` and :strong:`Flutter`. They are active contributors to open-source projects such as the Linux 
kernel, Yocto Project, Buildroot, and Zephyr RTOS, adhering to a philosophy of contributing their solutions to 
mainline open-source communities.

Project Overview
----------------

|libcppconnman| is an open-source project maintained by |Amarula|, as listed on their GitHub profile. It is a 
:strong:`C++ library` designed to provide a high-level, object-oriented interface for interacting with the 
:strong:`|ConnMan|` daemon.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Attribute
     - Detail
   * - **Project Name**
     - ``libcppconnman``
   * - **Maintainer**
     - |Amarula|
   * - **Language**
     - C++
   * - **License**
     - LGPL-2.1
   * - **Purpose**
     - C++ library for interacting with the ConnMan daemon.
   * - **Status**
     - Publicly available on GitHub

ConnMan Context
---------------

The library's main function is to facilitate communication with **|ConnMan|**, which is a :strong:`network connection manager` 
for Linux-based devices, particularly those running embedded systems. |ConnMan| is typically used in devices that 
require streamlined, robust, and automatic network configuration management, such as automotive systems, smart 
appliances, or industrial equipment.

|libcppconnman| provides a C++ layer over |ConnMan|'s existing D-Bus interface, allowing developers to integrate 
network management functionality into their C++ applications without directly handling the low-level D-Bus 
communication details. This simplifies tasks such as:

* Scanning for available network services (Wi-Fi, Ethernet, Cellular).
* Connecting to or disconnecting from a network.
* Monitoring connection status and changes.
* Managing network technologies.

|Amarula|'s Open Source Contribution
------------------------------------

The development of |libcppconnman| aligns with |Amarula|'s core business, which heavily involves :strong:`embedded Linux` 
and :strong:`open-source technology`. By providing such a library, they support developers working on devices that 
utilize |ConnMan| for network connectivity, easing the development of robust C++ applications for their embedded 
products. This commitment to open-source contributions reflects their value of transparency and their deep 
involvement in the embedded technology community.
