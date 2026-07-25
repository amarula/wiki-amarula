=========================================================
Centralized Build Artifacts with Gitea Artifact Manager
=========================================================

.. note:: **TL;DR**

   - **gitea-artifact-manager** is a Jenkins plugin by Amarula Solutions
     that stores build artifacts in the Gitea Generic Package Registry
     instead of the local filesystem.
   - Standard Jenkins pipeline steps like ``archiveArtifacts`` work
     transparently.

|

Why Move Artifacts to Gitea?
-------------------------------

Jenkins' default behavior stores build artifacts — compiled binaries,
test reports, firmware images — on the master's local disk. For the
kinds of embedded Linux builds Amarula runs (Yocto images, kernel
binaries, root filesystems, SDK installers), this presents real problems:

#. **Disk pressure** — a single Yocto build can produce gigabytes of
   artifacts. Jenkins' build rotation eventually deletes them.
#. **No audit trail** — which Jenkins build produced which binary that
   was shipped to a customer? Finding out means digging through
   ``$JENKINS_HOME/jobs/`` on disk.
#. **No off-master access** — other tools in the pipeline (test
   automation, flashing stations, release scripts) need to reach the
   artifacts but can't access the Jenkins filesystem.

Running a dedicated artifact server like JFrog Artifactory or Sonatype
Nexus adds operational overhead — another service to maintain, monitor,
and back up. For teams already using Gitea for Git hosting and code
review, the Generic Package Registry is already there, already backed
up, and already authenticated.

How It Works
--------------

The `gitea-artifact-manager <https://github.com/amarula/gitea-artifact-manager>`__
plugin acts as a translation layer between Jenkins' artifact management
API and Gitea's REST package API:

#. **Plugin intercepts** ``archiveArtifacts`` and ``stash``/``unstash`` steps.
#. **Maps** the Jenkins job name to a Gitea package name, and the build
   number to a package version.
#. **Uploads** each artifact as a file within that package version via
   Gitea's ``PUT`` API.
#. **Downloads** artifacts on demand when a downstream job or human
   requests them.

The result: your existing pipelines don't change — the plugin handles the
routing transparently.

Pipeline Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~

Because the plugin implements Jenkins' ``ArtifactManager`` extension
point, it works with any pipeline that uses standard steps:

.. code-block:: groovy

    archiveArtifacts artifacts: 'output/images/*.wic.gz'
    stash includes: 'build/conf/**', name: 'config'
    unstash 'config'

All three operate against Gitea packages rather than the local filesystem.

Configuration at Amarula
--------------------------

Amarula configures the plugin with:

- **Gitea Server URL** pointing to the internal Gitea instance.
- **Owner** set to an organization that groups all build artifacts
  (e.g., ``build-artifacts``).
- **API Token** scoped to ``read:package`` and ``write:package``,
  stored as a Jenkins credential.

Each build job automatically creates versioned packages under that
organization, with views accessible both through Jenkins and directly
in the Gitea web UI.

License
---------

- **License:** Apache License, Version 2.0 — Copyright 2026 Amarula Solutions
- **Repository:** `amarula/gitea-artifact-manager <https://github.com/amarula/gitea-artifact-manager>`__

.. tip::
   Interested in moving your Jenkins artifacts to Gitea or need help
   designing artifact management for embedded Linux CI/CD pipelines?
   Amarula Solutions provides consulting, deployment, and custom plugin
   development.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
