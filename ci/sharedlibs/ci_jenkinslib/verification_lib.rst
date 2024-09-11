com.amarula.build.Verification
*******************************

.. container:: toc-macro client-side-toc-macro conf-macro output-block

Helper class derived from Build that generalizes build verification of git and repo managed projects. It sends review to Gerrit to each change.

.. _com.amarula.build.Verification-Constructors:

Constructors
============

.. _com.amarula.build.Verification-Verification(steps,environment,credentials):

Verification(steps, environment, credentials)
---------------------------------------------

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **credentials** Jenkins Credentials ID(s) for repository access (String or String Array)

.. _com.amarula.build.Verification-Publicmethods:

Public methods
==============

.. _com.amarula.build.Verification-build(Stringurl,defbuildCode,dockerImage):

build(String url, def buildCode, dockerImage)
---------------------------------------------

Picks Gerrit Change defined from environment variables or fails if the proper environment variables are not set. Executes given code inside repository directory and reports the results.

The environment variables checked are GERRIT_REFSPEC, GERRIT_CHANGE_NUMBER, GERRIT_PATCHSET_NUMBER. They are automatically set by the Gerrit Trigger Plugin.

-  **url** Repository url
-  **buildCode** Code to use to build project from inside the repository directory
-  **dockerImage** Name of the docker image to use. By default, it searches Amarula's registry. To use an image on Docker Hub, use for example "`docker.io/gradle <http://docker.io/gradle>`__".

.. _com.amarula.build.Verification-repoBuild(StringmanifestUrl,defbuildCode,options=defaultRepoOptions):

repoBuild(String manifestUrl, def buildCode, options = defaultRepoOptions)
--------------------------------------------------------------------------

Checks out repo project from given manifest URL and gerrit changes defined from environment variable GERRIT_TOPIC. Method executes given code and reports the results.

-  **manifestUrl** Repository url with repo manifest
-  **buildCode** Code to build project from inside the root project directory
-  **options** Optional options for repo and repopick.

   -  **archiveManifest** archive manifest snapshot, default is false
   -  **dockerImage** name of the docker image to use
   -  **repoInitOpts** additional options for repo during repo init
   -  **repoSyncOpts** additional options for repo during repo sync, '--force-sync' is always added

.. _com.amarula.build.Verification-staticAnalysis(Mapargs):

staticAnalysis(Map args)
------------------------

Run analysis of Gerrit changes by building and analyzing each change. The results are reported back to Gerrit.

-  **args**

   -  **analyzers** List of Analyzers to use. Can be null or empty in which case the defaults are used. See com.amarula.codechecker.analysis.Analyzer
   -  **buildCommand** Execute and record a build command. Build commands can be simple calls to 'g++' or 'clang++' or 'make', but a more complex command, or the call of a custom script file is also supported.
   -  **dockerImage** Name of the docker image to use. By default, it searches Amarula's registry. To use an image on Docker Hub, use for example "`docker.io/gradle <http://docker.io/gradle>`__".
   -  **dockerOptions** Extra option to pass to docker container in order to mount volume or run in different mode
   -  **lang** Language of the project being analyzed. See com.amarula.codechecker.analysis.Language
   -  **url** Repository url
