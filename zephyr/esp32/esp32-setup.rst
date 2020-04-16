ESP32 Zephyr setup
##################

This tutorial shows you have to set up the ESP32 Wrover development board for use with zephyr on Linux.

First time board configuration
==============================

The first time the board is used you should set the correct jumper configuration for using JTAG. This only needs to be done once per board. See the figure for the correct jumper settings.

.. image:: wrover.jpg

ESP32 Tools
===========

Follow steps 1, 2 and 3 from `espressif <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html>`_ to install the required tools, download the sdk, and install the ESP32 toolchain.

Zephyr Tools
============

Follow :ref:`these <zephyr-setup>` steps to download and set up zephyr and its build tools.

Environment
===========

In order to build zephyr for ESP32 the following environment variables should be set.
The value for `ESPRESSIF_TOOLCHAIN_PATH` depends on where you installed it during the tool instalation step. The value for `ESP_IDF_PATH` depends on where you downloaded it during the tool instalation step.

.. code-block:: none

   export ZEPHYR_TOOLCHAIN_VARIANT="espressif"
   export ESPRESSIF_TOOLCHAIN_PATH="${HOME}/.espressif/tools/xtensa-esp32-elf/esp-2019r2-8.2.0/xtensa-esp32-elf/"
   export ESP_IDF_PATH="${HOME}/esp/esp-idf"

Put these commands in a script somewhere and source it at the start of your development session.

Build and run
=============

In order to build and run zephyr on the board use the following commands:

.. code-block:: none

   cd ~/zephyrproject
   west build -b esp32 -s zephyr/samples/hello_world/
   west flash
