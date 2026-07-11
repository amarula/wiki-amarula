com.amarula.repo.Repo
*********************

.. note:: **TL;DR**
   - Reference for the ``Repo`` class from Amarula Solutions' **repo_jenkins_lib** — provides repo tool operations for multi-repository projects (AOSP-style), including init, sync, and topic-based checkout/cherry-pick of Gerrit changes with cross-repository dependency handling.

.. _com.amarula.repo.Repo-:

.. _com.amarula.repo.Repo-Constructors:

Constructors
============

.. _com.amarula.repo.Repo-Repo(context,environment,StringmanifestUrl,Mapoptions=[:]):

Repo(context, environment, String manifestUrl, Map options = [:])
-----------------------------------------------------------------

Creates new instance for repo-managed projects.

-  **context** Jenkins pipeline context (this variable)
-  **environment** Jenkins environment (env variable)
-  **manifestUrl** URL of the repo manifest repository
-  **options** Optional map:
   -  **manifestBranch** branch of the manifest to use (default: master)
   -  **repoInitOpts** additional opts for ``repo init``
   -  **repoSyncOpts** additional opts for ``repo sync``

.. _com.amarula.repo.Repo-Methods:

Methods
=======

**init()** — Initializes the repo workspace.

**sync()** — Syncs all repositories according to the manifest.

**checkoutTopic(String topic)** — Checks out the latest changes for each project with the given Gerrit topic. Returns a list of ``GerritChange`` instances.

**checkoutTopicForManifest(String topic)** — Same as checkoutTopic but for the manifest repository.

**cherrypickTopic(String topic)** — Cherry-picks changes with the given Gerrit topic. Returns a list of ``GerritChange`` instances.

**cherrypickTopicForManifest(String topic)** — Same as cherrypickTopic but for the manifest repository.

.. tip::
   Need repo-managed multi-project CI/CD? Amarula Solutions provides
   repo_jenkins_lib for AOSP-style builds with cross-repository dependency
   handling and automated Gerrit verification.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
