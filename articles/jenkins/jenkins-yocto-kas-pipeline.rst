Optimizing Yocto Builds with Jenkins and Resource Throttling
============================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


.. figure:: /images/yocto-pipeline.png
   :align: center

|
|

Amarula Solutions

This article dissects a Jenkins pipeline designed for building Yocto images, focusing on its structure,
optimization techniques, and the underlying build process. It explores the use of resource throttling,
containerized builds, and multi-configuration approaches to improve efficiency and maintainability.

Pipeline Overview
-----------------

The Jenkins pipeline presented automates the build process for multiple Yocto images using a configuration-driven approach.
It utilizes a dedicated "big-node" for resource-intensive tasks and employs the ``throttleJobProperty``
to manage concurrent builds, preventing system overload.
The core functionality is encapsulated within the ``runYoctoTargetBuild`` function,
which leverages a containerized build environment for consistency and reproducibility.

Pipeline Breakdown
------------------

1.  **Agent Configuration:**

    * ``agent { node { label 'big-node' } }``: This directive assigns the pipeline to execute on a Jenkins node labeled "big-node," indicating a machine with ample resources (CPU, memory, storage) suitable for Yocto builds.

2.  **Resource Throttling:**

    * ``options { throttleJobProperty(categories: ['heavy_job'], throttleEnabled: true, throttleOption: 'category') }``: This crucial section implements resource throttling. It categorizes the job as "heavy_job" and enables throttling based on this category. This prevents multiple Yocto builds from running concurrently, which could lead to system instability or performance degradation. This is very important for Yocto, as it is very resource intensive.

3.  **Stages:**

    * **Checkout Project:**

        * ``git branch: 'acme-multiconfig', credentialsId: 'acme-bitbucket', poll: false, url: 'https://bitbucket.org/acmegit/dummy'``: This stage retrieves the Yocto project source code from a Bitbucket repository. The ``poll: false`` option disables periodic polling for changes, which is suitable for trigger-based builds.

    * **Yocto Image, Yocto Recovery, Yocto Develop:**

        * These stages execute the actual Yocto builds for different target images (e.g., "bt-acme-image," "bt-acme-recovery-image," "bt-acme-develop-image"). Each stage calls the ``runYoctoTargetBuild`` function with specific target and configuration parameters.

4.  **``runYoctoTargetBuild`` Function:**

    * **Credential Handling:**

        * ``withCredentials([file(credentialsId: 'acme-kas', variable: 'credentials')])``: This section securely retrieves the necessary credentials (e.g., SSH keys) for accessing remote repositories.

    * **Containerized Build:**

        * ``kas_container_remote = "registry.amarulasolutions.com:443/kas-acme-builder"``: This defines the Docker image used for the build environment.
        * The ``sh`` block executes a shell script within the container.
        * ``mkdir -p ${HOME}/data``: Creates a directory for shared state (``sstate``) and downloads.
        * ``export SSTATE_DIR="${HOME}/data/bitbake.sstate"`` and ``export DL_DIR="${HOME}/data/bitbake.downloads"``: sets the download and sstate cache directories, this allows for faster rebuilds.
        * ``ssh-keyscan`` commands: adds the keys for the required git servers to the known_hosts file, this allows the container to clone from the git servers.
        * ``KAS_CONTAINER_IMAGE="$kas_container_remote" kas-container --runtime-args '-v /lib/modules:/lib/modules' --ssh-dir ssh-build-hosts --git-credential-store $credentials shell $config -c "bitbake $target"``: This command launches the ``kas-container`` with necessary runtime arguments, mounts the SSH directory, provides Git credentials, and executes the ``bitbake`` command to build the specified target using the provided configuration file.
        * The ``--runtime-args '-v /lib/modules:/lib/modules'`` argument is very important, it allows the docker container to access the host machines kernel modules. This is required for some yocto builds.

Key Optimization Techniques
---------------------------

* **Resource Throttling:** The ``throttleJobProperty`` prevents resource contention and ensures stable builds, particularly crucial for resource-intensive Yocto tasks.
* **Containerization:** The use of Docker containers provides a consistent and reproducible build environment, eliminating dependency conflicts and ensuring build consistency across different machines.
* **Shared State (SSTATE) and Downloads:** The pipeline utilizes shared SSTATE and download directories, enabling faster rebuilds by reusing previously built components.
* **Multi-Configuration:** The pipeline supports building multiple target images from a single configuration file, promoting code reuse and simplifying maintenance.
* **SSH Key Management:** The pipeline securely manages SSH keys for accessing remote repositories, ensuring secure access to source code.

Conclusion
----------

This Jenkins pipeline demonstrates a robust and efficient approach to building Yocto images. By leveraging resource throttling, containerization, and multi-configuration, it optimizes the build process, improves maintainability, and ensures consistent and reliable builds. This pipeline serves as a valuable template for organizations seeking to automate and streamline their Yocto development workflows.

Example of Jenkins pipeline
***************************

.. code-block:: groovy

    pipeline {
      agent {
        node {
          label 'big-node'
        }
      }
      options {
        throttleJobProperty(
          categories: ['heavy_job'],
          throttleEnabled: true,
          throttleOption: 'category'
        )
      }

      stages {
        stage('Checkout project')
        {
          steps {
            git branch: 'acme-multiconfig', credentialsId: 'acme-bitbucket', poll: false, url: 'https://bitbucket.org/acmegit/dummy'
          }
        }
        stage('Yocto Image') {
          steps {
            runYoctoTargetBuild("multiconfig:dummy:bt-acme-image", "kas/dummy.yml")
          }
        }
        stage('Yocto Recovery') {
          steps {
            runYoctoTargetBuild("multiconfig:dummy_recovery:bt-acme-recovery-image", "kas/dummy.yml")
          }
        }
        stage('Yocto Develop') {
          steps {
            runYoctoTargetBuild("multiconfig:dummy_develop:bt-acme-develop-image", "kas/dummy.yml")
          }
        }
      }
    }

    def runYoctoTargetBuild(String target, String config) {
      withCredentials([file(credentialsId: 'acme-kas', variable: 'credentials')]) {
        def kas_container_remote = "registry.amarulasolutions.com:443/kas-acme-builder"
        sh """
           #!/bin/bash -xe
           mkdir -p ${HOME}/data
           export SSTATE_DIR="${HOME}/data/bitbake.sstate"
           export DL_DIR="${HOME}/data/bitbake.downloads"
           mkdir -p ssh-build-hosts
           ssh-keyscan -p 38745 gitea.amarulasolutions.com > ssh-build-hosts/known_hosts
           ssh-keyscan github.com >> ssh-build-hosts/known_hosts
           ssh-keyscan bitbucket.org >> ssh-build-hosts/known_hosts
           KAS_CONTAINER_IMAGE="$kas_container_remote" kas-container \\
             --runtime-args '-v /lib/modules:/lib/modules' \\
             --ssh-dir ssh-build-hosts --git-credential-store $credentials shell --update $config -c \\
             "bitbake $target"
        """
      }
    }

.. figure:: /images/pipeline-console-yocto.png
   :align: center
