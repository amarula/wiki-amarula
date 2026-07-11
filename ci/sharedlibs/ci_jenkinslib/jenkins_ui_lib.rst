com.amarula.ui.UI
*****************

.. note:: **TL;DR**
   - Reference for the ``Ui`` class from Amarula Solutions' **CI Jenkins shared library** — a builder-pattern class for creating parameterized Jenkins job UIs with boolean, string, choice, multiline string, and password parameters.
   - Enables consistent, self-documenting build forms across all Amarula pipelines.

.. _com.amarula.ui.UI-Overview:

Overview
--------

This class is used to build parameters for a Jenkins job. It provides a builder pattern for adding various types of parameters to a job, such as boolean, string, choice, and password parameters.

.. _com.amarula.ui.UI-UiClass:

Ui Class
--------

The ``Ui.Builder`` class provides the following methods:

-  **addStringParameter(name, defaultValue, description)** — Adds a string input parameter
-  **addBooleanParameter(name, defaultValue, description)** — Adds a checkbox parameter
-  **addChoiceParameter(name, choices, description)** — Adds a dropdown selection parameter
-  **addMultilineStringParameter(name, defaultValue, description)** — Adds a multiline text area
-  **addPasswordParameter(name, defaultValue, description)** — Adds a masked password input
-  **build()** — Returns the built UI configuration

Example usage:

.. code-block:: groovy

   import com.amarula.ui.Ui

   def ui = new Ui.Builder(this)
       .addStringParameter("BRANCH", 'master', "The branch to build from")
       .addBooleanParameter("KEEP_BUILD", false, "Keep build artifacts")
       .addBooleanParameter("ENABLE_MEND", false, "Run Mend security analysis")
       .build()

.. tip::
   Need consistent parameterized build UIs for your Jenkins pipelines?
   Amarula Solutions provides Ui builder integration for self-documenting,
   user-friendly pipeline parameter forms.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
