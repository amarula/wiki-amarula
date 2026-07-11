Continuous integration
======================

.. note:: **TL;DR**
   - Amarula Solutions' CI/CD documentation covering **Jenkins, Gerrit, Docker, SonarQube, Artifactory** — with guides on pipeline design, project organization, build throttling, shared libraries, Android application pipelines, and AOSP builds.
   - All pipelines leverage **Amarula Solutions' custom Groovy shared libraries** for consistent build verification, changelog generation, code analysis, and deployment across projects.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   jenkins.rst
   android/android
   aosp.rst
   docker.rst
   configure_gdsl_editor.rst
   gerrit_trigger.rst
   gerrit_repo_trigger.rst
   jenkins_global_variables.rst
   jenkins_credentials.rst
   jenkins_auto_complete_intellij.rst
   jenkins_project_organization.rst
   jenkins_script_console.rst
   jenkins_slave.rst
   pipeline_snippets.rst
   sharedlibs/index.rst
   sonarqube.rst
   build_throttling.rst

.. tip::
   Need a CI/CD pipeline for your embedded software team? Amarula Solutions
   designs and maintains Jenkins-based automation for Yocto, Android,
   firmware, and application builds.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
