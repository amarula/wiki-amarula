==================================
Gitea Artifact Manager for Jenkins
==================================

.. note:: **TL;DR**

   - A **Jenkins plugin** by Amarula Solutions that uses the Gitea
     Generic Package Registry as a storage backend for Jenkins build
     artifacts, replacing local filesystem storage.
   - Licensed under **Apache 2.0**; standard steps like
     ``archiveArtifacts`` work transparently.

.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

What is gitea-artifact-manager?
---------------------------------

`gitea-artifact-manager <https://github.com/amarula/gitea-artifact-manager>`__
is a Jenkins plugin built by Amarula Solutions that **replaces Jenkins'
local filesystem artifact storage with Gitea's Generic Package Registry**.

In a standard Jenkins setup, build artifacts — compiled binaries, test
reports, container images — are stored on the Jenkins master's local
filesystem. This creates several problems:

#. **Limited retention** — artifacts are pruned with build history, or
   the disk fills up.
#. **No built-in versioning** — finding an artifact from a specific build
   requires navigating Jenkins' internal directory structure.
#. **Fragility** — if the Jenkins master is lost, so are all artifacts.

By routing artifacts through Gitea's package API instead, each build's
artifacts become **immutable, versioned packages** tied to the build number,
stored in a Git-backed repository that your team already manages and backs up.

How It Works
--------------

The plugin maps Jenkins build concepts directly onto the Gitea Generic
Package API:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Gitea Concept
     - Jenkins Equivalent
     - Description
   * - ``{owner}``
     - Global config
     - Gitea user or organization owning the package
   * - ``{package_name}``
     - Job/Pipeline name
     - One package per Jenkins job
   * - ``{package_version}``
     - Build number
     - Each build creates a new version
   * - ``{filename}``
     - Artifact path
     - Relative path within the workspace

The plugin handles three operations:

- **Upload** — ``PUT /api/packages/{owner}/generic/{package_name}/{package_version}/{filename}``
- **Download** — ``GET /api/packages/{owner}/generic/{package_name}/{package_version}/{filename}``
- **Delete** — ``DELETE /api/packages/{owner}/generic/{package_name}/{package_version}``

Once configured, standard Jenkins pipeline steps like ``archiveArtifacts``
and ``stash`` / ``unstash`` work transparently — the plugin intercepts them
and routes data to Gitea instead of the local filesystem.

Pipeline Example
~~~~~~~~~~~~~~~~~

.. code-block:: groovy

    pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    sh 'make'
                    archiveArtifacts artifacts: 'target/*.jar'
                }
            }
        }
    }

The ``archiveArtifacts`` step automatically uploads matching files to the
configured Gitea instance. No changes to your existing pipeline code are needed.

Getting Started
-----------------

Requirements
~~~~~~~~~~~~~

- **Java** 17 or higher
- **Maven** 3.8 or higher (for building from source)
- **Jenkins** 2.479.3 or later
- A **Gitea instance** with Generic Package support enabled

Build from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    git clone https://github.com/amarula/gitea-artifact-manager.git
    cd gitea-artifact-manager
    mvn clean package

The packaged plugin is output as ``target/gitea-artifactory.hpi``.

Local Testing
~~~~~~~~~~~~~~

.. code-block:: none

    mvn hpi:run

Jenkins starts at ``http://localhost:8080/unsecured`` with the plugin loaded.

Installation
~~~~~~~~~~~~

#. Upload the ``.hpi`` file via **Manage Jenkins → Manage Plugins →
   Advanced → Upload Plugin**.
#. Restart Jenkins.

Configuration
~~~~~~~~~~~~~~

Navigate to **Manage Jenkins → Configure System → Artifact Management
for Builds**:

#. Choose **Gitea Artifact Manager** from the dropdown.
#. Set three values:

   - **Gitea Server URL** — base URL of your Gitea instance (e.g.,
     ``https://gitea.example.com``).
   - **Owner** — the Gitea user or organization that will own the packages.
   - **API Token** — a Jenkins credential containing a Gitea personal
     access token.

The Gitea token must have at minimum **``read:package``** and
**``write:package``** scopes.

Why Amarula Built This
------------------------

Amarula Solutions runs Jenkins-based CI/CD pipelines for embedded Linux
builds — kernel compilation, Yocto image generation, Buildroot firmware
builds. These produce large artifacts (kernel images, root filesystems,
SD card images) that:

- Need to be **retained across builds** for regression testing and
  release tracking.
- Should be **auditable** — which build produced which binary.
- Benefit from being stored in a **Git-backed repository** alongside
  the source code they were built from.

Gitea was already part of Amarula's infrastructure for Git hosting and
code review. Leveraging its Generic Package Registry for artifacts
eliminated the need for a separate artifact server like Artifactory or
Nexus, reducing operational complexity while providing the versioning and
retention needed for embedded development workflows.

License and Attribution
-------------------------

- **License:** Apache License, Version 2.0 — Copyright 2026 Amarula Solutions
- **Repository:** `amarula/gitea-artifact-manager <https://github.com/amarula/gitea-artifact-manager>`__

.. tip::
   Running Jenkins CI/CD for embedded Linux or Android builds? Amarula
   Solutions provides Jenkins pipeline design, plugin development, and
   artifact management consulting for teams adopting Gitea-based
   infrastructure.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
