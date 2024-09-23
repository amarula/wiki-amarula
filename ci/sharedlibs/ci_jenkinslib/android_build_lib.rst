com.amarula.build.AndroidBuild
*******************************

Helper class that generalizes Android Build steps.

.. _com.amarula.build.AndroidBuild-Constructors:

Constructors
============

.. _com.amarula.build.AndroidBuild-AndroidBuild(steps,environment,credentials,StringlunchPrefix):

AndroidBuild(steps, environment, credentials, String lunchPrefix)
-----------------------------------------------------------------

Creates new instance for building a specific Android project.

-  **steps** Jenkins steps (this variable in pipeline context)
-  **environment** Jenkins environment variables (env variable in pipeline context)
-  **credentials** Jenkins Credentials ID(s) for repository access (String or String Array)
-  **lunchPrefix** Lunch prefix matching 'lunch ${lunchPrefix}-${env.BUILD_ANDROID_VARIANT}'

.. _com.amarula.build.AndroidBuild-Publicmethods:

Public methods
==============

.. _com.amarula.build.AndroidBuild-setBuildDescription():

setBuildDescription()
---------------------

Sets unique Jenkins build description.

.. _com.amarula.build.AndroidBuild-repoBuild(StringmanifestUrl,Stringscript=':',Closureclosure={},options=[:]):

repoBuild(String manifestUrl, String script = ':', Closure closure = {}, options = [:])
---------------------------------------------------------------------------------------

Runs build inside docker image. Performs 'make clean', 'make' and 'make otapackage'. Specific make options can be passed using env.BUILD_ANDROID_MAKEOPTS variable.

-  **manifestUrl** Repository url with repo manifest
-  **script** Optional bash script to be executed after 'make' and 'make otapackage'
-  **closure** Optional actions to run after 'script' still inside the docker image
-  **options** Optional Map of options for repo and repopick.

   -  **archiveManifest** archive manifest snapshot, default is true
   -  **dockerImage** name of the docker image to use
   -  **repoInitOpts** additional options for repo during repo init
   -  **repoSyncOpts** additional options for repo during repo sync, '--force-sync' is always added

.. _com.amarula.build.AndroidBuild-deploy(Closureclosure={}):

deploy(Closure closure = {})
----------------------------

Prepares 'out' variable pointing to Android output directory and 'artifactBasename' variable containing unique build identificator.

.. _com.amarula.build.AndroidBuild-Exampleusage:

Example usage
=============

::

         import com.amarula.build.AndroidBuild

         node() {
           def customerCredentialsId = '2fe8'
           def gerritCredentialsId = '9af8'

           env.BUILD_TOPIC = 'TEST_MANIFEST_AND_REPO, TEST_ONLY_REPO, TEST_ONLY_MANIFEST'

           def androidBuild = new AndroidBuild(this, env,
               [customerCredentialsId, gerritCredentialsId],
               'aosp_sunfish')
           androidBuild.setBuildDescription()
           androidBuild.repoBuild("${GITEA_SSH_URL}/aosp/manifest",
               { echo "Custom shell script" },
               { echo "Post-build actions" },
               [dockerImage: 'android11-builder'])

           androidBuild.deploy() {
             echo out
             echo artifactBasename
             archiveArtifacts "${out}/*[-_]ota[-_]*.zip"
           }
         }
