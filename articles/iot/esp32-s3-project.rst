Firmware for a Remote Controller Based on ESP32
===============================================

About This
----------

This project consists in creating a firmware for a custom device based on an **ESP32-S3** module.
The designed device functions as a remote controller for the main industrial control system, communicating through digital I/Os and an infrared UART connection.

The firmware is built on the ESP-IDF framework, leveraging FreeRTOS as the operating system to provide a stable and scalable environment for device functionality.

One of the core components of the project is a sophisticated state machine, managing rules, commands, and system interactions.
Thanks to this approach, the device is capable of:

- Receiving and processing commands through various interfaces, such as web server, USB, MQTT, and UART.
- Managing Wi-Fi connections for remote controls and updates.
- Integrating Bluetooth Low Energy (BLE) for automatic detection of registered devices and activation of specific rules.

This project includes a web server, enabling system monitoring and configuration through an intuitive interface accessible from any browser.

Key endpoints include:

- Secure login for protected access.
- Monitoring the device's inputs and outputs.
- Sending customized commands.
- Viewing Wi-Fi, BLE, MQTT, UARTS configurations.
- Accessing status and configuration information of the industrial system.

This web interface makes the device user-friendly, reducing setup and management time for end users.

Commands
^^^^^^^^

Every command has its own syntax

Basic Commands
""""""""""""""

- **Output command**
- **Analog output command**: PWM
- **I/O gpio command**: Control GPIO
- **Send to COM port command**: Communicate with the UART.
- **HTTP request command**: Send HTTP requests, supporting both GET and POST methods.
- **Publish MQTT message command**
- **List BLE command**
- **Delete from BLE List command**

Configuration Commands
""""""""""""""""""""""

Configuration commands are used to set parameters of the device's features (Wi-Fi, BLE, MQTT, etc.), and are permanently stored in the **NVS**.
For instance:
- Wi-Fi access point configuration.
- BLE settings.
- MQTT settings.
- UARTs settings.
- Web server password and hostname configuration.

Command response
""""""""""""""""

Responses are sent using a command_response function, that sends the response based on where it is needed.

Web Server
----------

The WebServer allows the presentation of predefined or customized content via a browser. It starts when:
- Wi-Fi connectivity is activated.

Main Endpoints
^^^^^^^^^^^^^^

- **Login (POST)**: Authenticates users attempting to access the server.
- **Input/Outputs (GET)**: Retrieves the current status of the onboard inputs and outputs.
- **Send Commands (POST)**: Sends commands directly to the device.
- **Wi-Fi Settings (GET)**: Returns the current Wi-Fi configuration.
- **BLE Settings (GET)**: Returns BLE configuration and registered devices.
- **MQTT Settings (GET)**: Retrieves MQTT client settings.
- **Device Controller Status (GET)**: Extended status information from the infrared port.
- **Device Controller Configuration (GET)**: Returns the device configuration.

Project Structure
-----------------

The code is split into several libraries:

1. **Util**: Contains shared utility functions.
2. **HAL**: Hardware-dependent code.
3. **Lib**: Hardware-independent code utilizing HAL interfaces.

State Machine and Event Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The project is based on a **state machine** organized through a global context static struct (`sm_context`), which includes:
- **Event loop**: Managed by ESP-IDF.
- **Procedure queue**: Contains parsed procedures.
- **Actual state**: Updated during execution.

Parser
^^^^^^

Commands are parsed using **flex** (lexical analysis) and **bison** (syntactical analysis).

All commands have the prefix AT# followed by the command type.

- There can be a number of CONFIG_PROC_MAX_CMDS commands that can be parsed from a single string.
- Commands can have a maximum of MAX_ARGS arguments.
- Each command is parsed and stored into a struct.
- The struct contains the number of arguments of the command and an array of arguments of the command.

Furthermore, the parsing of the argument is done leveraging argument descriptors:

- `ARGUMENT_DESCRIPTOR_STRING`
- `ARGUMENT_DESCRIPTOR_STRING_OPTIONAL`
- `ARGUMENT_DESCRIPTOR_ENUM`
- `ARGUMENT_DESCRIPTOR_ENUM_OPTIONAL`
- `ARGUMENT_DESCRIPTOR_INT`
- `ARGUMENT_DESCRIPTOR_INT_OPTIONAL`
- `ARGUMENT_DESCRIPTOR_IP`
- `ARGUMENT_DESCRIPTOR_IP_OPTIONAL`

Procedure Queue
^^^^^^^^^^^^^^^

Commands are executed sequentially in a **FIFO** queue. Until the first command finishes, the next ones are queued.
The procedure queue has a limited number of procedures it can schedule.


MQTT
^^^^

The protocol used is the MQTT5 one.
The device is able to connect to a broker through a command and publish on topics.
In this way  the device can exchange real-time data with centralized management systems.

Bluetooth
^^^^^^^^^

The configuration of the bluetooth is done using the esp-idf library that will start a ble thread. In this project we chose to use the **NimBLE** stack.

Through the BLE command we can switch-on the bluetooth of the device and filter the result selecting a minimum required signal that means that we
can set the further signal in which searching for the ble devices in the LBLE list.

Quality Assurance
-----------------

To ensure firmware reliability, were employed:

- Unit Testing using the Unity library
- Use of mocks to simulate hardware during tests (the ones provided by espressif).
- Valgrind to identify memory leaks.
- Code Coverage monitored with tools like LCOV, enabling us to achieve high coverage for core functionalities.
- Use of Gerrit and Jenkins pipelines.

Unit Testing
^^^^^^^^^^^^

Tests are implemented using the **Unity** library and ESP-IDF mocks.
**CMock** is used for hardware-specific mock generation.

Code Coverage
^^^^^^^^^^^^^

**lcov** is used for monitoring code coverage and integrates with VSCode during local development.

In visual studio the coverage gutters plug-in is used:

.. figure:: /images/esp32-vscode-coverage.png
   :align: center

This shows at the bottom that 62% of the playtone file (buzzer) is tested. In green the covered parts, in red not covered.

.. figure:: /images/jenkins_code_coverage.png

This show the jenkins code coverage in CI using coverage plugin

Memory Leak Detection
^^^^^^^^^^^^^^^^^^^^^

**Valgrind** is used to detect memory leaks.

.. code-block:: console

    valgrind --leak-check=full --xml=yes --xml-file="$(PROJECT_TEST_BUILD_DIR)/memcheck.xml"
             "$(PROJECT_TEST_BUILD_DIR)/test_***_host.elf"

Valgrind checks on the terminal (summary):

.. figure:: /images/esp32-valgrind.png
   :align: center

Valgrind jenkins results:

.. figure:: /images/valgrind-warning.png

Gerrit and Jenkins
^^^^^^^^^^^^^^^^^^

The development is done using Gerrit and Jenkins together for code review and automated CI.

This can be summarized in 4 steps:

1. Developer Submits Patch:
   - Developer writes code, commits changes, and uploads a patch to Gerrit.

2. Code Review in Gerrit:

   - Reviewers inspect, comment, and approve (+1/+2) or request changes.
   - Developer updates the patch if needed.

3. Jenkins Validates Patch:

   - Gerrit triggers Jenkins to run automated tests (in this project: build, unit tests, documentation, c-lang checks and valgrind checks).
   - Jenkins reports results back to Gerrit as Verified +1 (pass) or Verified -1 (fail).

4. Merge Patch:

   - If approved (Code-Review +2 and Verified +1), the patch is merged into the target branch.

Key Benefits
------------

- **Quality**: Automated testing ensures reliability.
- **Efficiency**: Collaboration in Gerrit with CI/CD via Jenkins streamlines the process.

