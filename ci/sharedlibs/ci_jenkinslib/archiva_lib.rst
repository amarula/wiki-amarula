com.amarula.deploy.Archiva
***************************

.. note:: **TL;DR**
   - Reference for the ``Archiva`` class from Amarula Solutions' **CI Jenkins shared library** — provides methods for uploading build artifacts to the Archiva Maven repository manager.

.. _com.amarula.deploy.Archiva-DocumentationforArchivaclass:

Documentation for Archiva class
===============================

The ``Archiva`` class provides methods for uploading files to the Archiva repository manager. This document explains how to use the class and its methods.

.. _com.amarula.deploy.Archiva-ImportingtheArchivaclass:

Importing the Archiva class
---------------------------

::

   import com.amarula.deploy.Archiva

.. _com.amarula.deploy.Archiva-Constructors:

Constructors
============

.. _com.amarula.deploy.Archiva-Archiva():

Archiva(steps, environment, url, credentialsId)
-----------------------------------------------

Creates new instance for uploading artifacts to Archiva.

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **url** Archiva repository URL
-  **credentialsId** Jenkins Credentials ID for Archiva authentication

.. _com.amarula.deploy.Archiva-Methods:

Methods
=======

upload(String filePath, String repository, String groupId, String artifactId, String version, String packaging)
---------------------------------------------------------------------------------------------------------------

Uploads a file to the Archiva repository.

.. tip::
   Need artifact management in your CI/CD pipeline? Amarula Solutions
   provides Archiva integration, artifact upload automation, and
   repository management for embedded software builds.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
