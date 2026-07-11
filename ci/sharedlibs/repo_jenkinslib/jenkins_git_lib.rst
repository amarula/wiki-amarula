com.amarula.git.Git
********************

.. note:: **TL;DR**
   - Reference for the ``Git`` class from Amarula Solutions' **repo_jenkins_lib** — provides Git repository operations including sync, checkout, and cherry-pick of Gerrit changes, with credential management and Gerrit REST API integration.

Helper class that generalizes Git operations for Jenkins pipelines.

.. _com.amarula.git.Git-Constructors:

Constructors
============

.. _com.amarula.git.Git-Git(context,environment,Stringurl,Mapoptions=[:]):

Git(context, environment, String url, Map options = [:])
--------------------------------------------------------

Creates new instance for Git operations.

-  **context** Jenkins pipeline context (this variable)
-  **environment** Jenkins environment (env variable)
-  **url** Repository URL
-  **options** Optional map:
   -  **history** perform unshallow fetch
   -  **gerritRemoteUrl** URL of the Gerrit instance for review operations

.. _com.amarula.git.Git-Methods:

Methods
=======

**sync(String ref = 'master')** — Syncs the repository to the given branch or tag.

**checkoutChange(String refspec)** — Checks out a Gerrit change and returns a ``GerritChange`` instance.

**cherrypickChange(String refspec)** — Cherry-picks a Gerrit change and returns a ``GerritChange`` instance.

**getDirectory()** — Returns the working directory of the repository.

.. tip::
   Need Git operations integrated with Gerrit in your CI/CD? Amarula
   Solutions provides repo_jenkins_lib for automated repository management,
   change fetching, and review labeling in Jenkins pipelines.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
