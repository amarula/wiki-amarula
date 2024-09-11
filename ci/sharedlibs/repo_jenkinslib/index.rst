Repo Jenkins library
*********************

Rebo jenkins lib is shared library for Jenkins that helps with basic operations with Gerrit over git and repo managed projects.

source: https://gitea.amarulasolutions.com/i-tools/repo_jenkins_lib

source: https://gerrit-review.amarulasolutions.com/admin/repos/i-tools/repo_jenkins_lib

configured as:

-  name: repo_jenkins_lib
-  load implicitly: true
-  allow default version to be overridden: true

.. _RepoJenkinslibrary-Installation:

Installation
============

.. _RepoJenkinslibrary-AddtherepositorytoyourJenkinsinstanceasSharedlibrary::

Add the repository to your Jenkins instance as Shared library:
--------------------------------------------------------------

#. go to "Manage Jenkins" > "Configure System"
#. scroll down to "Global Pipeline Libraries" section
#. use "Add"

   #. Name: repo_jenkins_lib
   #. Default version: master
   #. Retrieval method → Modern SCM

      #. Source Code Management → Git
      #. Project Repository: ssh://gitea@gitea.amarulasolutions.com:38745/i-tools/repo_jenkins_lib.git

#. "Save"

.. _RepoJenkinslibrary-GeneratepasswordforGerritRESTAPI:

Generate password for Gerrit REST API
-------------------------------------

Create password for your Gerrit bot user and add it to Jenkins. You can use gerrit REST API to generate the password:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         curl -X PUT \
             --user <admin username>:<admin password> \
             --header "Content-Type: application/json; charset=UTF-8" \
             -d "{\"generate\": true}" \
             https://gerrit-review.amarulasolutions.com/a/accounts/<gerrit bot user id>/password.http

Add the credentials to Jenkins:

#. go to "Credentials" -> "System"
#. use "Add Credentials"

   -  Kind: "Username with password"
   -  Username: gerrit bot username
   -  Password: gerrit bot REST API password
   -  ID: e.g. jenkins-builder-amarula_gerrit-rest-api
   -  Description: ...

#. "Save"

.. _RepoJenkinslibrary-Optionalinstallationsteps:

Optional installation steps
===========================

Optionally you can fork repo tool and use your own stable version by defining "REPO_URL" and "REPO_BRANCH" in Jenkins Global Variables.

.. _RepoJenkinslibrary-Librarydescription:

Library description
===================

.. _RepoJenkinslibrary-Mainclasses:

Main classes
------------

This is only a brief description of the classes. See the specific class page for more details.

.. _RepoJenkinslibrary-com.amarula.git.Git:

com.amarula.git.Git
~~~~~~~~~~~~~~~~~~~

Helper class for basic git operations. It can sync given tag/branch or checkout/cherry-pick Gerrit change from the given parameters.

.. _RepoJenkinslibrary-com.amarula.gerrit.Gerrit:

com.amarula.gerrit.Gerrit
~~~~~~~~~~~~~~~~~~~~~~~~~

Helper class for basic Gerrit operations. It is used internally to query changes and set review labels in Gerrit.

.. _RepoJenkinslibrary-com.amarula.gerrit.GerritChange:

com.amarula.gerrit.GerritChange
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents single Gerrit change with enough information to fetch the change or set review labels.

.. _RepoJenkinslibrary-com.amarula.repo.Repo:

com.amarula.repo.Repo
~~~~~~~~~~~~~~~~~~~~~

Helper class for repo managed projects. It is used to sync projects including checkout/cherry-pick of Gerrit changes or Gerrit topics.

.. _RepoJenkinslibrary-Typicaluse:

Typical use
===========

.. _RepoJenkinslibrary-Repoprojectverification:

Repo project verification
-------------------------

The example below show typical use-case of repo project verification. The pipeline fetches all relevant changes with the same topic and sets a review to them.

The variable 'env.GERRIT_TOPIC' used in the example below is automatically set by Gerrit Trigger Plugin or can be set as Job Parameter.

.. container:: expand-container conf-macro output-block
   :name: expander-1903968565

   .. container:: expand-control
      :name: expander-control-1903968565

       Click here to see the example code ...

   .. container:: expand-content expand-hidden
      :name: expander-content-1903968565

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               @Library('repo_jenkins_lib')
               import com.amarula.gerrit.GerritChange
               import com.amarula.repo.Repo

               node {
                 stage('Repo init and sync') {
                   def changes = []
                   def value = GerritChange.FAILURE
                   sh "git config --global user.email ${env.GERRIT_USER_EMAIL}"
                   sh "git config --global user.name ${env.GERRIT_USER_NAME}"
                   withCredentials([usernamePassword(
                       credentialsId: 'jenkins-builder-amarula_gerrit-rest-api',
                       passwordVariable: 'GERRIT_RESTAPI_PASS',
                       usernameVariable: 'GERRIT_RESTAPI_USER')]) {
                     try {
                       def repo = new Repo(this, env,
                           'ssh://gitea@gitea.amarulasolutions.com:38745/myAndroidProject/manifest.git')
                       sshagent(['someCredentialId1', 'someCredentialId2']) {
                         // repo init
                         repo.init()

                         // checkout topic changes for manifest (OPTIONAL: default manifest will be used to sync)
                         changes.addAll(repo.checkoutTopicForManifest(env.GERRIT_TOPIC))

                         // repo sync
                         repo.sync()

                         // checkout topic changes for projects (OPTIONAL)
                         changes.addAll(repo.checkoutTopic(env.GERRIT_TOPIC))

                         // build project
                         sh 'make'

                         value = GerritChange.SUCCESS
                       }
                     } finally {
                       for (change in changes) {
                         change.setVerified(value)
                       }
                     }
                   }
                 } /* END 'Repo init and sync' */
               }

.. _RepoJenkinslibrary-Repoprojecttestbuild:

Repo project test build
-----------------------

The next example shows another typical use-case of test build with cherry-picking some changes.

.. container:: expand-container conf-macro output-block
   :name: expander-1005801308

   .. container:: expand-control
      :name: expander-control-1005801308

       Click here to see the example code ...

   .. container:: expand-content expand-hidden
      :name: expander-content-1005801308

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               @Library('repo_jenkins_lib')
               import com.amarula.gerrit.GerritChange
               import com.amarula.repo.Repo

               node {
                 stage('Repo init and sync') {
                   def changes = []
                   sh "git config --global user.email ${env.GERRIT_USER_EMAIL}"
                   sh "git config --global user.name ${env.GERRIT_USER_NAME}"
                   withCredentials([usernamePassword(
                       credentialsId: 'jenkins-builder-amarula_gerrit-rest-api',
                       passwordVariable: 'GERRIT_RESTAPI_PASS',
                       usernameVariable: 'GERRIT_RESTAPI_USER')]) {

                     def repo = new Repo(this, env,
                         'ssh://gitea@gitea.amarulasolutions.com:38745/myAndroidProject/manifest.git')
                     sshagent(['someCredentialId1', 'someCredentialId2']) {
                       // repo init
                       repo.init()

                       // cherry-pick topic changes for manifest (OPTIONAL: default manifest will be used to sync)
                       changes.addAll(repo.cherrypickTopicForManifest(env.GERRIT_TOPIC))

                       // repo sync
                       repo.sync()

                       // cherry-pick topic changes for projects (OPTIONAL)
                       changes.addAll(repo.cherrypickTopic(env.GERRIT_TOPIC))

                   echo "Building with topic: ${env.GERRIT_TOPIC}"
                   echo "Applied changes: ${changes}"

                       // build project
                       sh 'make'
                     }
                   }
                 } /* END 'Repo init and sync' */
               }

.. _RepoJenkinslibrary-Gitprojecttestbuild:

Git project test build
----------------------

This example shows usage of the Git class. The example shows how to checkout a specific Gerrit change given by env.GERRIT_REFSPEC from myProject repository and checkout repository with support tools myProjectSupportTools in one line.

The GERRIT_REFSPEC is initialized by the Gerrit Trigger Plugin or can be set from Job Parameters.

.. container:: expand-container conf-macro output-block
   :name: expander-219122963

   .. container:: expand-control
      :name: expander-control-219122963

       Click here to see the example code ...

   .. container:: expand-content expand-hidden
      :name: expander-content-219122963

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               @Library('repo_jenkins_lib')
               import com.amarula.gerrit.GerritChange
               import com.amarula.git.Git

               node {
                 def change
                 def myProject

                 stage('Project sync') {
                   sh "git config --global user.email ${env.GERRIT_USER_EMAIL}"
                   sh "git config --global user.name ${env.GERRIT_USER_NAME}"
                   withCredentials([usernamePassword(
                       credentialsId: 'jenkins-builder-amarula_gerrit-rest-api',
                       passwordVariable: 'GERRIT_RESTAPI_PASS',
                       usernameVariable: 'GERRIT_RESTAPI_USER')]) {
                     myProject = new Git(this, env,
                         'ssh://gitea@gitea.amarulasolutions.com:38745/myProject',
                         [gerritRemoteUrl:'https://gerrit-review.amarulasolutions.com'])

                     sshagent(['someCredentialId1', 'someCredentialId2']) {
                       change = myProject.checkoutChange(env.GERRIT_REFSPEC)

                       new Git(this, env, 'ssh://gitea@gitea.amarulasolutions.com:38745/myProjectSupportTools').sync()
                     }
                 }

                 stage('Build') {
                   def result = GerritChange.FAILURE
                   try {
                     dir(myProject.getDirectory()) {
                       sh 'make'
                     }
                     result = GerritChange.SUCCESS
                   } finally {
                     withCredentials([usernamePassword(
                         credentialsId: 'jenkins-builder-amarula_gerrit-rest-api',
                         passwordVariable: 'GERRIT_RESTAPI_PASS',
                         usernameVariable: 'GERRIT_RESTAPI_USER')]) {
                       change.setVerified(result)
                     }
                   }
                 }
               }
               
.. _contents: Table of contents


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   jenkins_gerrit_lib.rst
   jenkins_git_lib.rst
   jenkins_repo_lib.rst
