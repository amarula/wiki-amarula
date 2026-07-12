=======================
CI/CD & Test Automation
=======================

.. note:: **TL;DR**
   - Hub for **Jenkins CI/CD infrastructure** at Amarula Solutions — covering pipeline design for embedded projects (Yocto, Android, firmware), Gerrit-triggered verification, static analysis (CodeChecker), memory checking (Valgrind), hardware-in-the-loop testing (Labgrid), and shared Groovy libraries for pipeline standardization.

Jenkins Pipeline Documentation
==============================

Our CI/CD documentation covers the full pipeline lifecycle:

- **Jenkins overview** — architecture, folder organization, pipeline creation, job triggering, credentials.
  See `ci/jenkins <ci/jenkins.html>`_.

- **Gerrit trigger** — automated verification on patchset creation, Verified label management.
  See `ci/gerrit_trigger <ci/gerrit_trigger.html>`_.

- **Gerrit trigger for repo projects** — multi-repository dependency handling (AOSP-style).
  See `ci/gerrit_repo_trigger <ci/gerrit_repo_trigger.html>`_.

Embedded Build Pipelines
========================

Production pipeline patterns for specific build systems:

- **Yocto builds with kas-container and resource throttling** — `articles/jenkins/jenkins-yocto-kas-pipeline <articles/jenkins/jenkins-yocto-kas-pipeline.html>`_

- **Yocto with Mend SCA security scanning** — `articles/jenkins/jenkins-mend-pipeline <articles/jenkins/jenkins-mend-pipeline.html>`_

- **OS build + Labgrid hardware testing** — `articles/jenkins/how-validate-os-build-labgrid-testing <articles/jenkins/how-validate-os-build-labgrid-testing.html>`_

- **Android CI with S3 build caching (25% faster)** — `articles/jenkins/jenkins-mobile-build-time <articles/jenkins/jenkins-mobile-build-time.html>`_

- **DSL pipeline for Espressif firmware verification** — `articles/jenkins/jenkins-dsl-gerrit-trigger <articles/jenkins/jenkins-dsl-gerrit-trigger.html>`_

Code Quality & Security Scanning
================================

- **CodeChecker static analysis** with Jenkins Warnings NG — `articles/jenkins/warning-ng-jenkins-codechecker <articles/jenkins/warning-ng-jenkins-codechecker.html>`_

- **Valgrind memory leak detection** with quality gates — `articles/jenkins/warning-ng-jenkins-valgrind <articles/jenkins/warning-ng-jenkins-valgrind.html>`_

- **CodeNarc for Groovy shared libraries** — `articles/jenkins/jenkins-groovy-codenarc <articles/jenkins/jenkins-groovy-codenarc.html>`_

- **SonarQube integration** — `ci/sonarqube <ci/sonarqube.html>`_

- **Docker build dependency caching** — `ci/docker <ci/docker.html>`_

Shared Libraries
================

Amarula Solutions' reusable Groovy pipeline components:

- **ci_scripts** — Build, Verification, AndroidBuild, Ui, Archiva, Sftp classes.
- **repo_jenkins_lib** — Git, Gerrit, GerritChange, Repo for multi-repo projects.
- **codechecker_jenkins_lib** — CodeChecker static analysis wrapper.
- **changelog_lib** — Automated changelog generation.

See `ci/sharedlibs/index <ci/sharedlibs/index.html>`_ for complete documentation.

Android CI/CD
=============

- **Android app pipeline** — `ci/android/android_app_pipeline <ci/android/android_app_pipeline.html>`_
- **APK signing and AAB signing** — `ci/android/android_app_signing <ci/android/android_app_signing.html>`_
- **Emulator testing in Docker** — `ci/android/android_emulator_in_jenkins <ci/android/android_emulator_in_jenkins.html>`_
- **Google Play upload automation** — `ci/android/upload_android_app <ci/android/upload_android_app.html>`_
- **AOSP build project** — `ci/aosp <ci/aosp.html>`_

.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   ci/index
   articles/jenkins/index

.. tip::
   Need a CI/CD pipeline for your embedded software team? Amarula Solutions
   designs and maintains Jenkins-based automation for Yocto, Android,
   firmware, and application builds with Gerrit integration and
   hardware-in-the-loop testing.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
