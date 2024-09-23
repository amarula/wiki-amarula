com.amarula.build.Build
************************

Helper class that generalizes builds of git and repo managed projects. It checks the environment for variables set by Gerrit trigger plugin and synces the change(s). It can be set whether to checkout or cherry-pick the changes.

.. _com.amarula.build.Build-Constructors:

Constructors
============

.. _com.amarula.build.Build-Build(steps,environment,credentials):

Build(steps, environment, credentials)
--------------------------------------

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **credentials** Jenkins Credentials ID(s) for repository access (String or String Array)

.. _com.amarula.build.Build-Publicmethods:

Public methods
==============

.. _com.amarula.build.Build-setSyncMethod(SyncMethodmethod):

setSyncMethod(SyncMethod method)
--------------------------------

Set sync method to either Build.CHECKOUT or Build.CHERRYPICK. This determines the method used to pick a Gerrit change if it's set in the environment.

-  **method** One of Build.CHECKOUT or Build.CHERRYPICK

.. _com.amarula.build.Build-build(Stringurl,defbuildCode,defoptions=[:]):

build(String url, def buildCode, def options = [:])
---------------------------------------------------

Picks Gerrit Change defined from environment variables or given branch if the proper environment variables are not set. Executes given code inside repository directory and reports the results.

The method to pick Gerrit Change is determined by setSyncMethod(), checkout is used by default.

The environment variables checked are GERRIT_REFSPEC, GERRIT_CHANGE_NUMBER, GERRIT_PATCHSET_NUMBER. They are automatically set by the Gerrit Trigger Plugin.

-  **url** Repository url
-  **buildCode** Code to use to build project from inside the repository directory. The buildCode can be a multistage definition as a map: [Build : {code to execute}, Test : {test to execute}].
-  **options** Optional options

   -  **branch** Name of the branch to checkout, default is master
   -  **directory** directory where to checkout the content, default is repository name from given URL
   -  **dockerImage** Name of the docker image to use. By default, it searches Amarula's registry. To use an image on Docker Hub, use for example "`docker.io/gradle <http://docker.io/gradle>`__".
   -  **dockerOptions** Extra option to pass to docker container in order to mount volume or run in different mode
   -  **gerritRemoteUrl** Gerrit URL, default is from environment GERRIT_HOST
   -  **history** fetch full history (true), or only last commit (false), default is false
   -  **intermediateDocker** if we want to enable intermediate overlay (Use at your risk)
   -  **proxyCache** enable/disable proxy cache

.. _com.amarula.build.Build-repoBuild(StringmanifestUrl,defbuildCode,options=defaultRepoOptions):

repoBuild(String manifestUrl, def buildCode, options = defaultRepoOptions)
--------------------------------------------------------------------------

Checks out repo project from given manifest URL and gerrit changes defined from environment variable GERRIT_TOPIC. Method executes given code and reports the results.

-  **manifestUrl** Repository url with repo manifest
-  **buildCode** Code to use to build project from inside the root project directory. The buildCode can be a multistage definition as a map: [Build : {code to execute}, Test : {test to execute}].
-  **options** Optional options for repo and repopick.

   -  **archiveManifest** archive manifest snapshot, default is true
   -  **dockerImage** name of the docker image to use
   -  **dockerOptions** Extra option to pass to docker container in order to mount volume or run in different mode
   -  **gerritRemoteUrl** Gerrit URL, default is from the manifest
   -  **gerritMultitopic** true if topic can contain several topic separated by ','
   -  **repoInitOpts** additional options for repo during repo init
   -  **repoSyncOpts** additional options for repo during repo sync, '--force-sync' is always added

.. _com.amarula.build.Build-logBuild(StringbuildCmd,defoptions=null):

logBuild(String buildCmd, def options = null)
---------------------------------------------

Run given shell build command and log it using codechecker.

-  **buildCommand** Execute and record a build command. Build commands can be simple calls to 'g++' or 'clang++' or 'make', but a more complex command, or the call of a custom script file is also supported.

-  **options** Optional Map of options matching the long commandline options of the log command of CodeChecker (CodeChecker log --help).

.. _com.amarula.build.Build-analyzeBuild(Languagelang,List<Analyzer>analyzers,defoptions=null):

analyzeBuild(Language lang, List<Analyzer> analyzers, def options = null)
-------------------------------------------------------------------------

Use the previously created build logs created by logBuild method and perform static code analysis of the project. The analysis results of each change will be reported back to Gerrit.

-  **lang** Language of the project being analyzed. See com.amarula.codechecker.analysis.Language

-  **analyzers** List of Analyzers to use. Can be null or empty in which case the defaults are used. See com.amarula.codechecker.analysis.Analyzer

-  **options** Optional Map of options matching the long commandline options of the analyze command of CodeChecker (CodeChecker analyze --help).
