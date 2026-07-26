=========================================================
Centralized Build Artifacts with Gitea Artifact Manager
=========================================================

.. note:: **TL;DR**

   - **gitea-artifact-manager** is a Jenkins plugin by Amarula Solutions that allows Jenkins to offload build artifacts directly to your existing Gitea Git server, turning it into a dedicated artifact repository.
   - Standard Jenkins pipeline steps like ``archiveArtifacts`` work transparently; your CI/CD pipeline stays fully on-premise with no extra infrastructure.

|

The Problem It Solves
======================

If your organization relies on self-hosted infrastructure, you know the
challenge of keeping your entire CI/CD pipeline localized and
cost-effective.

**This plugin specifically solves on-premise artifact storage** by
allowing Jenkins to seamlessly offload build artifacts directly to
your already-installed Gitea Git server. You can now use Gitea as your
dedicated artifact repository, eliminating the need to deploy and
maintain a separate, heavy third-party artifact manager.

Running a dedicated artifact server like JFrog Artifactory or Sonatype
Nexus adds operational overhead — another service to maintain, monitor,
and back up. For teams already using Gitea for Git hosting and code
review, the Generic Package Registry is already there, already backed
up, and already authenticated.

|

How It Enhances Your Workflow
===============================

**True On-Premise Control**
   Keeps your codebase and your binary artifacts tightly unified within
   your secure, self-hosted Jenkins and Gitea environment. No external
   services, no cloud dependencies.

**Overcomes Bottlenecks**
   Built to help teams bypass the typical friction points of the testing
   and artifact-publishing phases. Artifacts flow directly from Jenkins
   to Gitea's versioned package registry.

**Improves Quality**
   Automates the artifact lifecycle to enhance overall software
   reliability and traceability. Each build's artifacts become immutable,
   versioned Gitea packages keyed by build number — you always know
   which binary came from which build.

**Highly Adaptable**
   Designed to adapt to your most difficult challenges, whether your
   company develops embedded systems or complex cloud architectures.
   The plugin implements Jenkins' ``ArtifactManager`` extension point,
   so it works with any pipeline using standard steps.

|

Amarula's Use Case
====================

Amarula Solutions runs Jenkins-based CI/CD for embedded Linux builds —
Yocto images, kernel binaries, root filesystems, SDK installers. These
produce gigabytes of artifacts that need to be retained, auditable, and
accessible to flashing stations and release scripts.

Gitea was already part of Amarula's infrastructure for Git hosting and
code review. Leveraging its Generic Package Registry for artifacts
eliminated the need for a separate artifact server, reducing operational
complexity while providing the versioning and retention needed for
embedded development workflows.

|

How It Works
---------------

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
