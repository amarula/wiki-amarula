Changelog library
*****************

.. note:: **TL;DR**
   - Amarula Solutions' **Changelog Jenkins library** — a Groovy wrapper around the **Git Changelog plugin** that generates formatted changelog reports using **mustache** HTML templates.
   - Simple API: ``new Changelog().generate(steps, options)`` with ``from`` and ``to`` tag/ref parameters.

This library is a wrapper on top of Jenkins changelog plugin. Jenkins changelog plugin needs to be installed before using this library. The library uses \ **mustache**\  template embedded in html for formatting data.

.. _com.amarula.changelog.Changelog-PREREQUISITES:

**PREREQUISITES**
-----------------

-  Git Changelog Plugin \ https://plugins.jenkins.io/git-changelog/

.. _com.amarula.changelog.Changelog-Scriptusage:

**Script usage**
----------------

|

First add **Jenkins changelog library** in your Jenkins shared library.

Now, to generate changelog use the \ **generate**\  method from \ **changelog.groovy**\  script file.  **new C**\ **hangelog().generate(steps, options)**

.. _com.amarula.changelog.Changelog-ExampleUsage:

**Example Usage**
-----------------

::

   import com.amarula.changelog.Changelog

   node {
       def options = [from: "v1.0", to: "master"]
       stage('Example') {
           git branch: 'master',
               credentialsId: 'github_credential_id',
               url: 'https://github.com/example.git'
           new Changelog().generate(this, options)
       }
   }

.. _com.amarula.changelog.Changelog-Parameters:

Parameters
~~~~~~~~~~

-  **steps**\  Context of current pipeline(this)
-  **options**\  Map containing \ ``from``\  and \ ``to``\  value. Here \ ``from``\  and \ ``to``\  is a tag or ref for which the changelog needs to be generated.

|

.. tip::
   Need automated changelog generation in your CI/CD pipeline? Amarula
   Solutions configures changelog generation with Git Changelog plugin
   and custom HTML templates for embedded software releases.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
