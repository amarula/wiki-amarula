Mender over MCU: a FreeRTOS experience
=======================================

.. note:: **TL;DR**
   - Implementation of Mender updates over Mender-mcu. Our setup is an AM263x board from TI, using FreeRTOS.
   - A general overview of the challenges of MbedTLS and using FreeRTOS
   - Detils on how to initialize Mender-MCU


The goal
--------

One of our customers needs to update the firmware of their boards quickly, and this could be needed for many boards of the same family.

One solution for this is using Mender, and our job is to integrate it with the current firmware.

What is Mender?
---------------

Mender is a software, composed by a server and a client, to provide over-the-air updates.
While the server is standard, the client needs to be implemented, as it is supposed to be used by embedded
devices, whose capabilities and API may vary quite vastly. In practice, the client software should answer the following questions:

- What to do when we connect to the network?
- What to do when we disconnect from the network?
- How do I identify my board?
- What are the server parameters?

While answering those questions is a must, there is an infrastructure below that needs to be set up (after all,
who do we answer this to?).
This, let me introduce you: `Mender-MCU <https://github.com/mendersoftware/mender-mcu>`_ This project allows us
to use a pre-determined infrastructure, and all we have to do is to implement the methods answering the questions
above.

Mender-MCU
----------

As mentioned above, Mender-MCU is a library that allows us to have a pre-defined infrastructure to make the
Mender integration seamless.
It supports mainly the Zephyr RTOS, Posix systems, the esp-idf system and, partially, FreeRTOS.
The "partially" clause, however, is not a fault of Mender-MCU itself: FreeRTOS does not offer much to work
with, as it reembles more a set of libraries than an entire kernel itself. Thus, integration is mostly on
our side, with some facilities, however, offered by Mender-MCU itself.

Moreover, Mender-MCU is backed up by `MbedTLS <https://github.com/Mbed-TLS/mbedtls>`_. Mbed-TLS is a quick
and reliable solution to get TLS working on embedded devices, without re-implementing the wheel (a very
complex wheel, I might add). Mbed-TLS, also, needs some questions answered inside our code. Luckily, those are few, and
can be answered by knowing the hardware and/or looking at the documentation:

- How do we generate a random number?
- How do we seed a random number generator?

This is used to generate keys that can be accepted by Mender for identifying the device.

.. figure:: /images/mender-mcu.png
   :align: center

   Mender-MCU and Mender interaction

The Hardware Security Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start, then, the implementation from the last questions: what looks like two questions can actually be transformed in one,
since the seeding can be performed as an initialization of the random number generator.
In our hardware, there is a HSM (Hardware Security Module) available. This can be used to generate good random numbers and communicate
them to the main CPU.

APIs can vary, but it's mostly a matter of initialization needed to make it work, and then using it to generate good random numbers. The
key takeaway for this is that the code should be very short and very quick to execute, given the possible latency times.

Answering Mender-MCU
^^^^^^^^^^^^^^^^^^^^^

Answeing Mender-MCU is a matter of implementing a few callbacks and filling a few structures.

First, a configuration structure: we need to know the evice type, the artifact name, the host (server) and a few more data.
This is to be able to connect with Mender. This includes the server parameters, like the HOST, and the device type, which
is used to be identifyed in a macro-category on the server
::

  mender_client_config_t mender_client_config = {
      .artifact_name = CONFIG_MENDER_INITIAL_ARTIFACT_NAME,
      .device_type = CONFIG_MENDER_DEVICE_TYPE,
      .host = CONFIG_MENDER_SERVER_HOST,
      .device_tier = "micro",
      .update_poll_interval = PROJECT_MENDER_POLL_INTERVAL,
      .inventory_update_interval = PROJECT_MENDER_INVENTORY_INTERVAL,
  };


Then, the client callbacks: those answer the questions we had in the beginning.

::

  mender_client_callbacks_t eris_mender_client_callbacks = {
      .network_connect = mender_network_connect_cb,
      .network_release = mender_network_release_cb,
      .deployment_status = mender_deployment_status_cb,
      .restart = mender_restart_cb,
      .get_identity = mender_get_identity_cb,
      .get_user_provided_keys = nullptr,
  };
 
Then, we pass some few configurations to support A/B partitioning during flashing. This is not the focus of this article, but it could still be useful if you need to do safe firmware updates.

::

  constexpr freertos_update_module_settings_t freertos_update_module_settings =
      {
          .artifact_type = CONFIG_MENDER_ARTIFACT_TYPE,
          .requires_reboot = true,
          .supports_rollback = true,
      };

  constexpr freertos_mender_slot_info_t freertos_mender_slot_info = {
      .addr = BOOT_SLOT_A_ADDR,
      .size = BOOT_SLOT_B_ADDR - BOOT_SLOT_A_ADDR,
  };

Then, for the initialization, the code will look like this:

::

  auto retval =
      mender_client_init(&mender_client_config, &eris_mender_client_callbacks);
  // Manage errors
  mender_freertos_image_set_flash_backend(&mender_image_flash_backend);

  retval = mender_freertos_image_register_update_module(
      freertos_update_module_settings, &freertos_mender_slot_info);
  // Manage errors
  retval = mender_inventory_add_callback(persistent_inventory_cb, true);
  // Manage errors

  retval = mender_client_activate();

This fully initializes Mender and, in the end, starts the client. From now on,
Mender-MCU will do everything on its own, asking the server for updates and connecting.

A few things I skipped
-----------------------

Something I did not mention here is he use of the desired MbedTLS. As said before, Mender-MCU
is used in tandem with MbedTLS. However, MbedTLS should be provided by the project itself, and
is not included by Mender-MCU.

Giving for granted that MbedTLS is available saves us a bit of trouble: the MbedTLS configuration.
This could be a topic for another day, however, as, in this project, one of the difficulties was
upgrading from MbedTLS 2.x to MbedTLS 4.2.0.

.. tip::
   Want to enable auto-updates on your IOT devices? Amarula Solutions
   provides firmware architecture, state machine design, Mender
   integration and updates over-the-air, and automated CI/CD with Gerrit and Jenkins.
   `Contact our IoT firmware team <https://www.amarulasolutions.com/contact/>`_
