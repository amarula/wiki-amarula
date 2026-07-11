Enhancing RX/TX Statistics in Linux CAN Drivers
===============================================

.. note:: **TL;DR**
   - Patch series by Dario Binacchi accepted into **Linux kernel 6.13** — fixing RX/TX statistics counter inaccuracies across multiple CAN drivers for improved reliability in **industrial, automotive, and embedded applications**.

We are pleased to announce that a patch series authored by Dario Binacchi, embedded Linux and kernel engineer at `Amarula Solutions <https://www.amarulasolutions.com>`_, has been accepted into the Linux kernel.
The series addresses inaccuracies in the RX (receive) and TX (transmit) statistics counters across multiple CAN drivers,
ensuring proper functionality and reliability in these critical metrics.

The changes enhance the robustness and reliability of the Linux kernel, particularly in industrial, automotive, and
embedded applications, where precise error counter management is crucial for monitoring and diagnostics.

The series [1] will be included in the Linux kernel 6.13 release.

[1] https://lore.kernel.org/lkml/20241122221650.633981-8-dario.binacchi@amarulasolutions.com/T/#m57226fdb513812d28cc85c4492fba48f42a30e05

#LinuxKernel #CANProtocol #EmbeddedSystems #Automotive #IndustrialAutomation #OpenSource #AmarulaSolutions

.. tip::
   Need Linux kernel driver development or CAN bus integration for your
   embedded product? Amarula Solutions provides upstream-first kernel
   engineering for industrial and automotive applications.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
