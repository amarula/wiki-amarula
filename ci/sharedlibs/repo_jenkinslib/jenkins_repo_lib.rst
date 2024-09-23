com.amarula.repo.Repo
**********************

.. _com.amarula.repo.Repo-:

.. _com.amarula.repo.Repo-Constructors:

Constructors
============

.. _com.amarula.repo.Repo-Repo(context,environment,StringmanifestUrl,Mapoptions=[:]):

Repo(context, environment, String manifestUrl, Map options = [:])
-----------------------------------------------------------------

Creates new instance for handling operations over a specific repo project.

-  **context** Jenkins steps ('this' in pipeline context)
-  **environment** Jenkins environment variables ('env' variable in pipeline context)
-  **manifestUrl** URL of git repository with repo manifest
-  **options** Optional map of options for repo commands

   -  **repoInitOpts** additional options for repo during repo init, '-u URL' is always added
   -  **repoSyncOpts** additional options for repo during repo sync, '--force-sync --detach' is always added
   -  **gerritRemoteUrl** Gerrit URL, default is from the manifest

.. _com.amarula.repo.Repo-Publicmethods:

Public methods
==============

.. _com.amarula.repo.Repo-Repoinit():

Repo init()
-----------

Initializes new repo project and fetches latest manifest version. This behaviour can be changed using repoInitOpts option in constructor. E.g. to fetch the manifest based on tag or a branch.

.. _com.amarula.repo.Repo-Reposync(archiveManifest=true):

Repo sync(archiveManifest = true)
---------------------------------

Performs sync on already initialized project. Behaviour can be changed using repoSyncOpts option. E.g. to change default number of threads to use.

-  **archiveManifest** Archive manifest snapshot, default is true

.. _com.amarula.repo.Repo-checkoutTopic(Stringtopic):

checkoutTopic(String topic)
---------------------------

Checkouts latest topic change for each project.

-  **topic** Gerrit topic to checkout

Returns: list of changes with given topic

.. _com.amarula.repo.Repo-GerritChangecheckoutChange(GerritChangechange=null):

GerritChange checkoutChange(GerritChange change = null)
-------------------------------------------------------

Checkouts given change or a change defined from env variables if change not given. The env variables used is either GERRIT_REFSPEC or GERRIT_CHANGE_NUMBER with GERRIT_PATCHSET_NUMBER. Values are expected the same as Gerrit Trigger plugin sets them. If GERRIT_PATCHSET_NUMBER is not set or is 0, the latest patchset is picked.

-  **change** Change to checkout in its project or manifest

Returns: the change or null if change was not found

.. _com.amarula.repo.Repo-cherrypickTopic(Stringtopic):

cherrypickTopic(String topic)
-----------------------------

Cherry-picks changes with given gerrit topic.

-  **topic** Gerrit topic to cherry-pick

Returns: list of changes with given topic

.. _com.amarula.repo.Repo-GerritChangecherrypickChange(GerritChangechange=null):

GerritChange cherrypickChange(GerritChange change = null)
---------------------------------------------------------

Cherry-picks given change or a change defined from env variables if change not given. The env variables used is either GERRIT_REFSPEC or GERRIT_CHANGE_NUMBER with GERRIT_PATCHSET_NUMBER. Values are expected the same as Gerrit Trigger plugin sets them. If GERRIT_PATCHSET_NUMBER is not set or is 0, the latest patchset is picked.

-  **change** Change to cherry-pick in its project or manifest

Returns: the change or null if change was not found

.. _com.amarula.repo.Repo-checkoutTopicForManifest(Stringtopic):

checkoutTopicForManifest(String topic)
--------------------------------------

Checkouts latest topic change for repo manifest.

-  **topic** Gerrit topic to checkout

Returns: list of changes with given topic

.. _com.amarula.repo.Repo-cherrypickTopicForManifest(Stringtopic):

cherrypickTopicForManifest(String topic)
----------------------------------------

Cherry-picks changes with given gerrit topic for repo manifest.

-  **topic** Gerrit topic to cherry-pick

Returns: list of changes with given topic

| 
