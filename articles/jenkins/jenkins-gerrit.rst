Jenkins Checks Plugin: Enhanced Reporting and Proxy
===================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


.. figure:: /images/jenkins-gerrit.png
   :align: center
|
|


Overview
--------

The recent update to the Jenkins integration for the Gerrit Checks plugin transforms it from a basic status reporter into a deep integration tool. It surfaces specific compiler warnings, static analysis issues, and test failures directly within the Gerrit UI.

Plugin Repositories
-------------------

The source code for the Jenkins Checks plugin and its associated components can be found at the following locations:

* **Main Plugin Repository**: The frontend and backend proxy logic are hosted at `gerrit-checks-jenkins <https://gerrit.googlesource.com/plugins/checks-jenkins/>`_.
* **Jenkins API Plugin**: The required Jenkins-side component is available at `gerrit-checks-api-plugin <https://github.com/jenkinsci/gerrit-checks-api-plugin>`_.
* **Amarula Solutions Check Jenkins Gerrit Fork**: The gerrit plugin is available at `Check Jenkins Gerrit plugin <https://github.com/amarula/check-jenkins>`_

Key Features
------------

* **Backend Proxying**: Securely handles authenticated requests to Jenkins via a new Gerrit-side servlet.
* **Static Analysis Integration**: Supports the Jenkins ``warnings-ng`` plugin, displaying issues with color-coded severity tags and inline code pointers.
* **Test Result Reporting**: Parses JUnit-style test reports to display failed test cases as check results.
* **Authenticated API Access**: Supports Jenkins API tokens for private instances.

Configuration
-------------

To enable these features, update your configuration in ``gerrit.config`` or ``project.config``.

Required Parameters
-------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Parameter
     - Description
   * - ``jenkins.url``
     - The base URL of your Jenkins instance.
   * - ``jenkins.user``
     - The Jenkins username for API authentication.
   * - ``jenkins.token``
     - The Jenkins API token required for the proxy.

Example Configuration
---------------------

.. code-block:: ini

   [jenkins "my-instance"]
       url = https://jenkins.example.com
       user = gerrit-bot
       token = 118db87784346782390abcde

Technical Implementation
------------------------

The Proxy Servlet (Java)
------------------------

The ``JenkinsProxyServlet`` is registered at the ``/proxy-trigger`` endpoint. It handles ``POST`` requests by extracting Jenkins server details and credentials from custom headers (``X-Jenkins-Auth``, ``X-Jenkins-Server``) and forwarding the request using Basic Authentication.

Analysis and Result Fetching (TypeScript)
-----------------------------------------

The frontend fetcher now performs a multi-stage process to build report results:

1. **Status Retrieval**: Gets the basic check run status from the Gerrit-Checks Jenkins endpoint.
2. **Analysis Reports**: Queries ``/warnings-ng/api/json`` to find active analysis tools (e.g., Checkstyle, Pylint).
3. **Issue Mapping**: Maps individual issues to Gerrit ``CheckResult`` objects, providing summary messages and code pointers for inline highlighting.
4. **Test Reports**: Scans ``/testReport/api/json`` to identify ``FAILED`` tests and appends them as Error results.

Severity and Categorization
---------------------------

The plugin maps Jenkins analysis severities to Gerrit UI visual cues to help developers prioritize fixes.

Severity Color Mapping
----------------------

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Jenkins Severity
     - Color
     - Context
   * - ``ERROR``
     - ``PURPLE``
     - Critical blockers or compilation errors.
   * - ``HIGH``
     - ``BROWN``
     - High-priority warnings.
   * - ``NORMAL``
     - ``YELLOW``
     - Standard linting or code style issues.
   * - ``LOW``
     - ``PINK``
     - Low-priority advisories.

Result Categories
-----------------

The overall result category is determined by tool-specific thresholds:

* **ERROR**: Triggered if total issues meet or exceed the ``errorSize`` threshold.
* **WARNING**: Triggered if issues meet or exceed the ``highSize`` threshold.
* **INFO**: Triggered if issues meet or exceed the ``normalSize`` threshold.
* **SUCCESS**: Applied if no thresholds are met.

Troubleshooting
---------------

* **502 Errors**: Usually indicates a failure in the proxy communication. Verify that the ``user`` and ``token`` are correct and that the Gerrit server can reach the Jenkins URL.
* **Missing Warnings**: Ensure the **Warnings Next Generation** plugin is active on the Jenkins job and that the user has API access to the ``warnings-ng`` endpoints.
* **Test Summaries**: The fetcher looks specifically for ``FAILED`` statuses in the JUnit JSON; passed or skipped tests are not imported as results.
