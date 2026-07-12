com.amarula.build.Build
***********************

.. note:: **TL;DR**
   - Reference for the ``Build`` class from Amarula Solutions' **CI Jenkins shared library** (``ci_scripts``) — the core helper for building Git and repo-managed projects, with Gerrit change syncing (checkout or cherry-pick), Docker-based build environments, and credential management.

Helper class that generalizes builds of git and repo managed projects. It checks the environment for variables set by Gerrit trigger plugin and synces the change(s). It can be set whether to checkout or cherry-pick the changes.

.. _com.amarula.build.Build-Constructors:

Constructors
============

.. _com.amarula.build.Build-Build(steps,environment,credentials):

Build(steps, environment, credentials)
--------------------------------------

Creates new instance for building a specific project.

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **credentials** Jenkins Credentials ID(s) for repository access (String or String Array)

.. _com.amarula.build.Build-Publicmethods:

Public methods
==============

.. _com.amarula.build.Build-setSyncMethod():

setSyncMethod(String method)
----------------------------

Sets the sync method for receiving changes. Values: ``Build.CHECKOUT`` or ``Build.CHERRYPICK``.

.. _com.amarula.build.Build-setBuildDescription():
--------------------------------------------------
setBuildDescription()
---------------------

Sets unique Jenkins build description.

.. _com.amarula.build.Build-build():

build(String repoUrl, Closure buildCode, Map options = [:])
-----------------------------------------------------------

Runs build inside docker image (if specified). It performs repository sync, checkout of Gerrit changes (according to sync method), and runs the provided build closure.

-  **repoUrl** Repository url of the project
-  **buildCode** Closure with build steps to execute
-  **options** Optional Map of options:
   -  **branch** branch to sync (default: master)
   -  **history** perform unshallow fetch for changelog (default: false)
   -  **dockerImage** name of the docker image to use for the build
   -  **dockerOptions** additional docker options
   -  **gerritProject** Gerrit project name for cherry-pick
   -  **gerritMultitopic** allow cherry-picking changes from multiple topics

.. _com.amarula.build.Build-repoBuild():

repoBuild(String manifestUrl, Closure buildCode, Map options = [:])
------------------------------------------------------------------

Same as build() but for repo-managed projects (like AOSP).

.. _com.amarula.build.Build-logBuild():

logBuild(String command)
------------------------

Logs the build command execution.

.. tip::
   Need standardized build pipelines for your projects? Amarula Solutions
   provides the Build class and shared library infrastructure for Git and
   repo-managed embedded software CI/CD.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
