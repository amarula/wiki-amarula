==========================================================================
Building a Custom I2C Peripheral for Embedded Linux: From VHDL to Yocto
==========================================================================

.. note:: **TL;DR**

   - We built a custom **I2C** on a **Xilinx Zynq** FPGA to emulate
     I2C peripherals and a **Kernel Linux Driver** to forward transactions
     directly to userspace.
   - The real challenge was not the I2C alone, but integrating
     heterogeneous elements — **VHDL** logic, an hardware design,
     a **Linux kernel driver**, a **Yocto BSP** and **automated hardware
     tests** — and keeping them aligned.

|


Overview: FPGA-Based Test I2C Devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A custom test I2C device is implemented on a Xilinx Zynq FPGA, integrating
programmable logic with ARM processor cores running embedded Linux. The
device processes bus transactions in hardware and forwards them through a
dedicated Linux kernel driver directly to userspace. This architecture
allows software applications to control device interactions and generate
responses dynamically.


Key Capabilities of the Test Device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Software-Driven Operation:** The test I2C device routes bus events to
  userspace software, where transaction handling and response logic are
  determined.
- **Deterministic Clock Stretching:** The device manages bus timing by
  holding the clock line low until userspace supplies a response,
  preventing bus protocol violations.
- **Multi-Instance Support:** Multiple independent test I2C devices can be
  instantiated on a single FPGA board. Each instance operates with its own
  interrupt line and is exposed to Linux as a distinct character device.
- **Strict Timing Coordination:** The hardware state machine aligns
  sampling between the FPGA clock and bus signal transitions to ensure
  reliable start, stop, and data handling.


System Architecture and Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **VHDL Core:** Defines the test I2C device state machine and provides an
  AXI4-Lite register interface linked to the ARM processing system.
- **Kernel Driver:** Translates hardware interrupts from the test device
  into userspace events and writes software responses back to hardware
  registers.
- **Simulation Verification:** Multi-layered testbenches running in VUnit
  and GHDL validate state transitions, clock stretching behavior, and
  register transactions prior to synthesis.
- **Automated Hardware Testing:** Physical bus transactions through the
  test device are verified directly on the board using automated suites
  driven by pytest and labgrid.


.. tip::
   Amarula Solutions designs custom FPGA IP cores, Linux kernel drivers,
   and Yocto BSPs for embedded products. Need a custom peripheral brought
   up end-to-end, from VHDL to userspace?
   `Contact our embedded team <https://www.amarulasolutions.com/contact/>`_
