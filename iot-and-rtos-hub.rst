==========================
IoT Firmware & RTOS Development
==========================

.. note:: **TL;DR**
   - Hub aggregating **IoT and RTOS documentation** — covering **Zephyr RTOS** (ESP32, STM32, TI CC3220SF), **ESP32 firmware projects** (ESP-IDF, FreeRTOS, MQTT, BLE), and **CI/CD for IoT firmware** (Gerrit, Jenkins, Unity, Valgrind, CodeChecker).

Zephyr RTOS
===========

Amarula Solutions contributes to the Zephyr Project with board support and drivers.

**Platform guides:**

- **ESP32 setup** — getting started with Zephyr on Espressif ESP32.
  See `opensource/thirdparty/zephyr/esp32/esp32-setup <opensource/thirdparty/zephyr/esp32/esp32-setup.html>`_.

- **TI CC3220SF** — Zephyr on Texas Instruments SimpleLink Wi-Fi SoC.
  See `opensource/thirdparty/zephyr/ti/CC3220SF <opensource/thirdparty/zephyr/ti/CC3220SF.html>`_.

- **Zephyr setup overview** — `opensource/thirdparty/zephyr/zephyr <opensource/thirdparty/zephyr/zephyr.html>`_.

ESP32 Firmware Development
==========================

Production firmware projects built on ESP-IDF and FreeRTOS:

- **ESP32-S3 Remote Controller** — state machine architecture, AT-command parser (flex/bison), MQTT5, NimBLE BLE, web server, CI/CD with Unity/Valgrind/LCOV.
  See `articles/iot/esp32-s3-project <articles/iot/esp32-s3-project.html>`_.

- **ESP32 Camera Bridge** — Ethernet-Wi-Fi bridge for IP camera RTSP streaming via ESP32 access point.
  See `articles/iot/esp32-camera <articles/iot/esp32-camera.html>`_.

Firmware CI/CD
==============

- **DSL Pipeline for Espressif Firmware Verification** — Gerrit-triggered Jenkins pipeline with clang-format, cmake-lint, Valgrind, unit tests.
  See `articles/jenkins/jenkins-dsl-gerrit-trigger <articles/jenkins/jenkins-dsl-gerrit-trigger.html>`_.

- **CodeChecker static analysis for C/C++ firmware** — `articles/jenkins/warning-ng-jenkins-codechecker <articles/jenkins/warning-ng-jenkins-codechecker.html>`_

- **Valgrind memory leak detection** — `articles/jenkins/warning-ng-jenkins-valgrind <articles/jenkins/warning-ng-jenkins-valgrind.html>`_

Workshop Challenges
===================

- **Zephyr Frontiers** — support a new architecture on Zephyr.
- **ESP32 firmware bring-up** — from bootloader to application.

See `news/workshop <news/workshop.html>`_ for more workshop challenges.

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   opensource/thirdparty/zephyr/index
   articles/iot/index

.. tip::
   Building an IoT product on ESP32 or need Zephyr RTOS integration?
   Amarula Solutions provides firmware architecture, BLE/MQTT/Wi-Fi
   connectivity, sensor driver development, and CI/CD for IoT firmware.
   `Contact our IoT team <https://www.amarulasolutions.com/contact/>`_
