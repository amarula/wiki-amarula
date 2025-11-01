==================================================
SCA Layer for Yocto with Mend Support
==================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


Introduction
------------

The ``meta-mend`` layer provides seamless integration of Mend Software Composition Analysis (SCA) into the Yocto Project build process. This enables developers to identify and address open-source vulnerabilities within their embedded Linux distributions during development. Leveraging Mend's comprehensive vulnerability database and analysis capabilities, this layer enhances the security posture of Yocto-based products.

Our specialization in security and our commitment to helping companies comply with emerging regulations like the Cyber Resilience Act (CRA) in Europe drive the development of this layer. By incorporating SCA directly into the build pipeline, we empower organizations to proactively manage software risks and build more secure products.

Usage
-----

This layer introduces a BitBake class (`mend.bbclass`) that facilitates the application of Mend checks to your Yocto build. The Mend analysis requires a Java runtime environment on the host system. To simplify setup, we provide a custom `kas-container` image that includes the necessary Java installation.

Download
--------

You can download the ``meta-mend`` layer from its GitHub repository:

.. code-block:: text

        https://github.com/amarula/meta-mend

You can clone the repository using Git:

.. code-block:: bash

        git clone https://github.com/amarula/meta-mend

Configuration
-------------

To enable Mend SCA analysis in your Yocto build, you need to inherit the `mend` class and configure the required Mend API credentials. This configuration is typically done in your ``conf/local.conf`` file or within the ``local_conf_header`` section of your ``kas`` configuration file.

.. code-block:: text

        INHERIT += " mend"

        WS_USERKEY = "<your_mend_user_key>"
        WS_APIKEY = "<your_mend_api_key>"
        WS_WSS_URL = "<your_mend_wss_url>"
        WS_PRODUCTNAME = "<your_product_name>"
        WS_PRODUCTTOKEN = "<your_product_token>"

.. note::
   Replace the placeholder values (``<...>``) with your actual Mend API credentials and project details. Contact Mend for your specific keys and URLs.

Using with ``kas-container``
----------------------------

To utilize the provided `kas-container` image with Java, follow these steps:

1. **Download the Docker Image:** Download the container image from the provided Google Drive link: https://drive.google.com/file/d/1gMtveXMFtlW_pdADBy5-ARqEu4dgyN7p

2. **Load the Docker Image:** Load the downloaded Docker image into your local Docker environment using the following command:

.. code-block:: bash

        docker load <path_to_downloaded_image>

3. **Run ``kas-container`` with the Custom Image:** When executing your ``kas-container`` commands, prepend the ``KAS_CONTAINER_IMAGE`` environment variable to specify the custom image:

.. code-block:: bash

        KAS_CONTAINER_IMAGE=amarula/kas-java:latest kas-container <your_kas_command>

        For example:

        KAS_CONTAINER_IMAGE=amarula/kas-java:latest kas-container build -b <your_board> <your_image>.bb

Alternative using ``docker-compose``
------------------------------------

Alternatively, you can leverage ``docker-compose`` to manage the container.

1. **Navigate to the Docker Directory:** Change your current directory to the ``docker`` subdirectory within the ``meta-mend`` layer.

.. code-block:: bash

        cd docker

2. **Build the Docker Compose Service:** Build the Docker Compose service. You may need to adjust the Docker registry and the ``KAS_CONTAINER_IMAGE`` within the ``docker-compose.yml`` file to match your specific setup.

.. code-block:: bash

        docker compose build

Integration with Cyber Resilience Act (CRA)
-------------------------------------------

We understand the increasing importance of cybersecurity regulations like the upcoming Cyber Resilience Act (CRA) in Europe. The ``meta-mend`` layer is a crucial tool in helping companies meet the security requirements outlined in the CRA. By proactively identifying and mitigating open-source vulnerabilities during the development lifecycle, organizations can build more resilient and compliant products. Our expertise in security ensures that this layer is designed with these evolving regulatory landscapes in mind.

Further Development
-------------------

We are continuously working to enhance the ``meta-mend`` layer with new features and improvements. Future developments may include more granular control over Mend analysis parameters, integration with reporting tools, and enhanced support for different Yocto workflows.

Contributing
------------

Contributions to the ``meta-mend`` layer are welcome! Please refer to the contribution guidelines for more information on how to contribute patches, bug reports, or feature requests.

License
-------

The ``meta-mend`` layer is licensed under the MIT License. See the ``LICENSE`` file for more details.
