com.amarula.build.Verification
******************************

.. note:: **TL;DR**
   - Reference for the ``Verification`` class from Amarula Solutions' **CI Jenkins shared library** — extends ``Build`` with automated Gerrit review label posting (Verified +1/-1) based on build success or failure.
   - Used as the standard pattern for Gerrit-triggered verification pipelines.

Helper class derived from Build that generalizes build verification of git and repo managed projects. It sends review to Gerrit to each change.

.. _com.amarula.build.Verification-Constructors:

Constructors
============

.. _com.amarula.build.Verification-Verification(steps,environment,credentials):

Verification(steps, environment, credentials)
---------------------------------------------

Creates new instance for build verification of a specific project.

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **credentials** Jenkins Credentials ID(s) for repository access (String or String Array)

.. _com.amarula.build.Verification-Publicmethods:

Public methods
==============

.. _com.amarula.build.Verification-verifyBuild():

verifyBuild(String credentialsId, String repoUrl, Closure buildCode, Map options = [:])
---------------------------------------------------------------------------------------

Shorthand for verification of git-managed projects.

.. _com.amarula.build.Verification-isTriggeredByGerrit():

isTriggeredByGerrit()
---------------------

Returns true if the build was triggered by a Gerrit event.

.. _com.amarula.build.Verification-analyzeBuild():

analyzeBuild(Language lang, List<Analyzer> analyzers, Map options = [:])
------------------------------------------------------------------------

Runs CodeChecker static analysis on the project. Returns a CodeCheckerAnalysis object.

.. _com.amarula.build.Verification-Exampleusage:

Example usage
=============

::

   import com.amarula.build.Verification

   node {
     def dockerImage = 'system-x-builder:1.0'
     def manifestUrl = "${GITEA_SSH_URL}/myAndroidProject/manifest.git"
     def credentials = ['someCredentialId1', 'someCredentialId2']

     new Verification(this, env, credentials).repoBuild(manifestUrl, {
         sh 'make'
     }, [dockerImage: dockerImage])
   }

.. tip::
   Need Gerrit-integrated build verification? Amarula Solutions provides
   the Verification class and pipeline templates for automated review
   labeling in embedded software CI/CD.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
