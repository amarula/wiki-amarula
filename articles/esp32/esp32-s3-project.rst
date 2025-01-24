Firmware for a Remote Controller Based on ESP32
===============================================

About This
----------

This project consists in creating a firmware modem-like for a custom device based on an **ESP32-S3-WROOM-1-N16R8V** module.
The designed device functions as a remote controller for the main burner control system, communicating through digital I/Os and an infrared UART connection.

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
 - Accessing status and configuration information of the burner system.

This web interface makes the device user-friendly, reducing setup and management time for end users.
The web pages are retrieved from an sdcard.

Commands
--------

Every command has its own syntax, but they always follow the pattern `AT#<command_name>,<data>`.

### Basic Commands

- **Output command**
- **Play tone command**
- **Analog output command**: PWM
- **Wait command**: Delay in ms
- **Send to COM port command**: Communicate with the UART.
- **HTTP request command**: Send HTTP requests, supporting both GET and POST methods.
- **Publish MQTT message command**
- **Send UDP message command**
- **Send TCP message command**
- **Append to BLE List command**: Adds a new UID/name pair to the BLE observer list.
- **List BLE command**
- **Delete from BLE List command**
- **Firmware Upgrade command**: (not yet implemented)

### Configuration Commands

Configuration commands are used to set parameters of the device's features (Wi-Fi, BLE, MQTT, etc.), and are permanently stored in the **NVS**.  
For instance:
- Wi-Fi access point configuration.
- BLE settings.
- MQTT settings.
- UARTs settings.
- Web server password and hostname configuration.

### Rules Commands

- **READ RULE**
- **EDIT/DELETE RULE**

### Command response

Responses are sent using a command_response function, that sends the response based on where it is needed.
For example if the command was sent though usb, the response will be on the usb. Same for the web server.
To do that, the command response has a context where is specified where the function to be used for the specific
interface.


Web Server
----------

The WebServer allows the presentation of predefined or customized content via a browser. It starts when:
- Wi-Fi connectivity is activated.
- The SD card containing the `httpdocs` folder is found.

### Main Endpoints

- **Login (POST)**: Authenticates users attempting to access the server.
- **Input/Outputs (GET)**: Retrieves the current status of the onboard inputs and outputs.
- **Send Commands (POST)**: Sends commands directly to the device.
- **Message Area (GET)**: Returns the contents of the message area (up to 1024 bytes).
- **Wi-Fi Settings (GET)**: Returns the current Wi-Fi configuration.
- **BLE Settings (GET)**: Returns BLE configuration and registered devices.
- **MQTT Settings (GET)**: Retrieves MQTT client settings.
- **Burner Controller Status (GET)**: Extended status information from the infrared port.
- **Burner Controller History (GET)**: Logs or records of past events.
- **Burner Controller Configuration (GET)**: Returns the device configuration.

Project Structure
-----------------

The code is split into several libraries:

1. **Util**: Contains shared utility functions.
2. **HAL**: Hardware-dependent code.
3. **Lib**: Hardware-independent code utilizing HAL interfaces.

### State Machine and Event Handler

The project is based on a **state machine** organized through a global context static struct (`sm_context`), which includes:
- **Event loop**: Managed by ESP-IDF.
- **Procedure queue**: Contains parsed procedures.
- **Actual state**: Updated during execution.
- **Rule database**: Memorizes active rules to handle events.

### Rule database

Rules are stored in the database for event matching and command execution. They can be:

- Edited by index
- Read by index
- Matched against events

### Parser

Commands are parsed using **flex** (lexical analysis) and **bison** (syntactical analysis).  

All commands have the prefix AT# followed by the command type.
- There can be a number of CONFIG_***_PROC_MAX_CMDS commands that can be parsed from a single string.
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

### Procedure Queue

Commands are executed sequentially in a **FIFO** queue. Until the first command finishes, the next ones are queued.
The procedure queue has a limited number of procedures it can schedule.


### MQTT

The protocol used is the MQTT5 one.
The device is able to connect to a broker through a command and publish on topics.
In this way  the device can exchange real-time data with centralized management systems.

### Bluetooth

The configuration of the bluetooth is done using the esp-idf library that will start a ble thread. In this project we chose to use the **NimBLE** stack.

Through the BLE command we can swicth-on the bluetooth of the device and filter the result selecting a minimum required signal that means that we
can set the further signal in which searching for the ble devices in the LBLE list.

When a device is found in the selected range the ble rule is triggered, such as proximity-based automation.

The devices to detect must be beacons, iBeacon or Eddystone, with uuids of 16 bytes. In the case of Eddystone the uuid in the list must match the
namespace ID + instance ID of the beacon (32 bits in total). iBeacon has already an uid of 32 bits.

Quality Assurance
=================

To ensure firmware reliability, were employed:

 - Unit Testing using the Unity library
 - Use of mocks to simulate hardware during tests (the ones provided by espressif).
 - Valgrind to identify memory leaks.
 - Code Coverage monitored with tools like LCOV, enabling us to achieve high coverage for core functionalities.
 - Use of Gerrit and Jenkins pipelines.


### Unit Testing

Tests are implemented using the **Unity** library and ESP-IDF mocks.  
**CMock** is used for hardware-specific mock generation.

### Code Coverage

**lcov** is used for monitoring code coverage and integrates with VSCode during local development.

In visual studio the coverage gutters plug-in is used:

.. figure:: /images/esp32-vdcode-coverage.png
   :align: center

This shows at the bottom that 62% of the playtone file (buzzer) is tested. In green the covered parts, in red not covered.

### Memory Leak Detection

**Valgrind** is used to detect memory leaks.
 ```
 valgrind --leak-check=full --xml=yes --xml-file="$(CONTRIVE_TEST_BUILD_DIR)/memcheck.xml"
 "$(CONTRIVE_TEST_BUILD_DIR)/test_***_host.elf"
 ```

Valgrind checks on the terminal (summary):

.. figure:: /images/esp32-valgrind.png
   :align: center

### Gerrit and Jenkins

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

## Key Benefits

   - **Quality**: Automated testing ensures reliability.
   - **Efficiency**: Collaboration in Gerrit with CI/CD via Jenkins streamlines the process.

