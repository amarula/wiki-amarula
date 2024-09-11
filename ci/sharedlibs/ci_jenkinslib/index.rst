CI Jenkins library
*******************

CI Jenkins Library is shared library for Jenkins that helps with common operations and generic builders for specific tasks. It simplifies some common tasks that we do in our Jenkins jobs.

source: https://gitea.amarulasolutions.com/i-tools/ci_jenkins_lib

source: https://gerrit-review.amarulasolutions.com/admin/repos/i-tools/ci_jenkins_lib

configured as:

-  name: ci_scripts
-  load implicitly: true
-  allow default version to be overridden: true

.. _CIJenkinslibrary-Installation:

Installation
============

.. _CIJenkinslibrary-AddtherepositorytoyourJenkinsinstanceasSharedlibrary::

Add the repository to your Jenkins instance as Shared library:
--------------------------------------------------------------

#. go to "Manage Jenkins" > "Configure System"
#. scroll down to "Global Pipeline Libraries" section
#. use "Add"

   #. Name: ci_scripts
   #. Default version: master
   #. Retrieval method → Modern SCM

      #. Source Code Management → Git
      #. Project Repository: ssh://gitea@gitea.amarulasolutions.com:38745/i-tools/ci_jenkins_lib.git

#. "Save"

.. _CIJenkinslibrary-Setconfigurationvariables:

Set configuration variables
---------------------------

#. go to "Manage Jenkins" > "Configure System"
#. scroll down to "Global properties" section
#. use the "Environment variables" option
#. define these variables (values are examples):

   -  DOCKER_REGISTRY_HTTPS_URL : "https://registry.amarulasolutions.com:443"
   -  DOCKER_REGISTRY_USER : "amarulabot"

      -  name of the credentials to use to authenticate with the registry
      -  the credentials are of type Username with password

   -  GERRIT_HOST : "`gerrit-review.amarulasolutions.com <http://gerrit-review.amarulasolutions.com>`__"
   -  GERRIT_USER_EMAIL : "amarulabot@\ `amarulasolutions.com <http://amarulasolutions.com>`__"
   -  GERRIT_USER_NAME : "amarulabot"
   -  JENKINS_GERRIT_REST_API_CREDENTIAL_ID : "jenkins_https@gerrit"

#. "Save"

.. _CIJenkinslibrary-Optionalinstallationsteps:

Optional installation steps
===========================

.. _CIJenkinslibrary-Mattermostendpointurl:

Mattermost endpoint url
~~~~~~~~~~~~~~~~~~~~~~~

Set "MATTERMOST_ENDPOINT_URL" global variable in Jenkins in form: https://mattermost.amarulasolutions.com/hooks/abc

.. _CIJenkinslibrary-MSTeamsendpointurl:

MS Teams endpoint url
~~~~~~~~~~~~~~~~~~~~~

Set "TEAMS_ENDPOINT" global variable in Jenkins in form: https://amarulasolutions.webhook.office.com/webhookb2/abc/IncomingWebhook/abc

.. _CIJenkinslibrary-Librarydescription:

Library description
===================

.. _CIJenkinslibrary-Steps:

Steps
-----

.. _CIJenkinslibrary-notification.monitoredStage:

notification.\ ``monitoredStage``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The monitoredStage wraps regular stage step with a try-catch and can notify when build fails.

.. _CIJenkinslibrary-notification.notifySuccess:

``notification.notifySuccess``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step should be used to notify that the build finished successfully.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         node() {
           notification.monitoredStage('Source sync') {
             // work
           }

           notification.monitoredStage('Build') {
             // work
           }

           notification.notifySuccess()
         }

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   .. container:: confluence-information-macro-body

      The notifications are sent to defined Mattermost and MS Teams endpoints and channels. Those are determined from the global environment variables: ``MATTERMOST_ENDPOINT_URL`` and ``TEAMS_ENDPOINT``.

.. _CIJenkinslibrary-notification.withMattermostEndpoint/notification.withTeamsEndpoint:

notification.\ ``withMattermostEndpoint`` / notification.\ ``withTeamsEndpoint``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allows to change the endpoints for notifications inside them.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         def mattermostEndpoint = 'x'
         def teamsEndpoint = 'y'

         node() {
           notification.withMattermostEndpoint(mattermostEndpoint, 'channel name') {
           notification.withTeamsEndpoint(teamsEndpoint) {
           notification.monitoredStage('Source sync') {
             // work
           }

           notification.monitoredStage('Build') {
             // work
           }

           } // end withTeamsEndpoint
           } // end withMattermostEndpoint

           notification.notifySuccess()
         }

.. _CIJenkinslibrary-Mainclasses:

Main classes
------------

This is only a brief description of the classes. See the specific class page for more details.

.. _CIJenkinslibrary-com.amarula.build.Build:

com.amarula.build.Build
~~~~~~~~~~~~~~~~~~~~~~~

Helper class that generalizes builds of git and repo managed projects. It checks the environment for variables set by Gerrit trigger plugin and synces the change(s). It can be set whether to checkout or cherry-pick the changes.

.. _CIJenkinslibrary-com.amarula.build.AndroidBuild:

com.amarula.build.AndroidBuild
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Helper class derived from Build that generalizes Android OS code sync and build steps.

.. _CIJenkinslibrary-com.amarula.build.Verification:

com.amarula.build.Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Helper class derived from Build that generalizes build verification of git and repo managed projects. It sends review to Gerrit to each change.

.. _CIJenkinslibrary-com.amarula.deploy.Archiva:

com.amarula.deploy.Archiva
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Archiva class provides methods for uploading files to the Archiva repository manager.

.. _CIJenkinslibrary-com.amarula.deploy.Sftp:

com.amarula.deploy.Sftp
~~~~~~~~~~~~~~~~~~~~~~~

This class handles common operations for uploading files to Sftp.

.. _CIJenkinslibrary-com.amarula.ui.Ui:

com.amarula.ui.Ui
~~~~~~~~~~~~~~~~~

This class is used to build parameters for a Jenkins job. It provides a builder pattern for adding various types of parameters to a job, such as boolean, string, choice, and password parameters.

.. _CIJenkinslibrary-Typicaluse:

Typical use
===========

.. _CIJenkinslibrary-Repoprojectverification:

Repo project verification
-------------------------

The example below show typical use-case of repo project build verification. The pipeline fetches all relevant changes and sets a review to them.

.. container:: expand-container conf-macro output-block
   :name: expander-93842874

   .. container:: expand-control
      :name: expander-control-93842874

       Click here to see the example code ...

   .. container:: expand-content expand-hidden
      :name: expander-content-93842874

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               import com.amarula.build.Verification
                
               node {
                 def dockerImage = 'system-x-builder:1.0'
                 def manifestUrl = "${GITEA_SSH_URL}/myAndroidProject/manifest.git"
                 def credentials = ['someCredentialId1', 'someCredentialId2']

                 def options = [dockerImage : dockerImage]

                 new Verification(this, env, credentials).repoBuild(manifestUrl, {
                     sh 'make'
                 }, options)
               }

.. _CIJenkinslibrary-Repoprojecttestbuild:

Repo project test build
-----------------------

The next example shows another typical use-case of test build with cherry-picking some changes.

.. container:: expand-container conf-macro output-block
   :name: expander-870278278

   .. container:: expand-control
      :name: expander-control-870278278

       Click here to see the example code ...

   .. container:: expand-content expand-hidden
      :name: expander-content-870278278

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               import com.amarula.build.Build

               node {
                 def dockerImage = 'system-x-builder:1.0'
                 def credentials = ['someCredentialId1', 'someCredentialId2']

                 Build systemXBuild = new Build(this, env, credentials)
                 systemXBuild.setSyncMethod(Build.CHERRYPICK)
                 systemXBuild.repoBuild("${GITEA_SSH_URL}/myAndroidProject/manifest.git", {
                     sh 'make'
                 }, [dockerImage: dockerImage,
                     gerritMultitopic: true])
               }
               
.. _contents: Table of contents


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   android_build_lib.rst
   jenkins_build_lib.rst
   verification_lib.rst
   archiva_lib.rst
   sftp_library.rst
   jenkins_ui_lib.rst
