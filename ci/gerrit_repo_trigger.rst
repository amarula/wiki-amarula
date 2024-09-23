Gerrit trigger for repo projects
*********************************

Some projects are composed of several git repositories that are dependent in some way. These repositories are usually managed using \`\ ``repo``\ \` tool. Typical example of such project is Android open-source project (AOSP).

.. _Gerrittriggerforrepoprojects-Challengesofverificationbuilds:

Challenges of verification builds
=================================

One change in one repository may need another change in a different repository in order to be complete and the whole project working without errors. These inter-repository dependencies complicate verification builds. Meaning that fetching just one change is not enough to successfully complete a verification build.

.. _Gerrittriggerforrepoprojects-Recognizerelatedchanges:

Recognize related changes
-------------------------

It is up to the author of the patches to recognize dependencies between repositories and mark related patches with the same topic. The easiest way to do that is using :literal:`\`repo start <TOPIC> projectA projectB`\ \` and \`\ ``repo upload -t --br=<TOPIC> projectA projectB``\ \`. This will automatically add Gerrit topic to all the uploaded changes based on the development branch name.

.. _Gerrittriggerforrepoprojects-Triggeronlyonebuild:

Trigger only one build
----------------------

Each uploaded change triggers one build. We can't do anything about that if we want to keep the trigger automatic. But Gerrit Trigger plugin configuration has a feature for stopping builds that have the same topic. It means that when a new verification build for related changes is started, the already running build (if there is one) is stopped.

This can be configured in 'Manage Jenkins' → 'Gerrit Trigger' → 'Abort patch sets with same topic':

.. image:: /images/gerrit_trigger_for_repo.png

It is also recommended to change value of 'Build Schedule Delay' to at least 10 seconds. This option is located also in 'Gerrit Trigger' configuration under 'Advanced ...' → 'Miscellaneous'.

.. _Gerrittriggerforrepoprojects-Fetchchanges:

Fetch changes
-------------

All related changes have the same topic, which makes it easier to fetch. The topic is stored in 'GERRIT_TOPIC' environment variable. The goal is to checkout the latest change for each project.

We use Gerrit REST API \`\ :literal:`GET /changes/?q=...`.`

https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes

::

         curl --user "jenkins-builder:${GERRIT_JENKINSBUILDER_PASSWORD}" "https://${GERRIT_URL}/a/changes/?q=topic:\"${GERRIT_TOPIC}\"+status:open+parentproject:${PARENT_PROJECT}&o=CURRENT_REVISION&o=CURRENT_COMMIT"

The response contains all Gerrit changes with given ``GERRIT_TOPIC`` that are open and their project's parent is ``PARENT_PROJECT``. We parse the response into a map \`\ ``PROJECT : [ GerritChange, GerritChange ]``\ \`.

Now for each project we find the latest change by finding the one that is descendant of all the changes. We use git to compare the relation between two commits:

::

         # git merge-base --is-ancestor <maybe-ancestor-commit> <descendant-commit>
         git -C ${PROJECT_PATH} merge-base --is-ancestor ${COMMIT_A} ${COMMIT_B}

We checkout the one that is descendant of the other commits:

::

         # repo download {[project] change[/patchset]}
         repo download ${PROJECT_NAME} ${LATEST_CHANGENUMBER}/${LATEST_CURRENT_PATCHSET}

.. _Gerrittriggerforrepoprojects-Set'Verified'flag:

Set 'Verified' flag
-------------------

The build is triggered for only one specific change, so only that one receives automatically the review. We have to set review for all the changes that we used. We can keep a list of changes from the 'Fetch changes' section and set review for each one using Gerrit REST API \`\ ``POST /changes/{change-id}/revisions/{revision-id}/review``\ \`.

https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-review

::

         curl -X POST --user "jenkins-builder:${GERRIT_JENKINSBUILDER_PASSWORD}" --header "Content-Type: application/json; charset=UTF-8" -d "{ \"labels\": { \"Verified\": 1 } }" "https://${GERRIT_URL}/a/changes/${GERRIT_CHANGE_ID}/revisions/${GERRIT_REVISION_COMMIT_ID}/review"

The response contains changes in review made to the change with change ID ``GERRIT_CHANGE_ID`` ("Change-Id:" in commit message) and patchset identified by its commit ID ``GERRIT_REVISION_COMMIT_ID``.

.. _Gerrittriggerforrepoprojects-ImplementationinRepoJenkinsLibrary:

Implementation in Repo Jenkins Library
======================================

https://gitea.amarulasolutions.com/i-tools/repo_jenkins_lib

.. _Gerrittriggerforrepoprojects-Mainclasses:

Main classes
------------

.. container:: expand-container conf-macro output-block
   :name: expander-1809469218

   .. container:: expand-control
      :name: expander-control-1809469218

       com.amarula.gerrit.Gerrit

   .. container:: expand-content expand-hidden
      :name: expander-content-1809469218

      Create new instance per gerrit remote, query changes and set review to them. It is expected that usage is surrounded with credential use in env variables GERRIT_RESTAPI_USER and GERRIT_RESTAPI_PASS.

.. container:: expand-container conf-macro output-block
   :name: expander-1376837707

   .. container:: expand-control
      :name: expander-control-1376837707

       com.amarula.gerrit.GerritChange

   .. container:: expand-content expand-hidden
      :name: expander-content-1376837707

      Represents one gerrit change. Returned from Gerrit class. Enables to get some basic information about the change, set review and to get list of related changes.

.. container:: expand-container conf-macro output-block
   :name: expander-2124064004

   .. container:: expand-control
      :name: expander-control-2124064004

       com.amarula.repo.Manifest

   .. container:: expand-content expand-hidden
      :name: expander-content-2124064004

      Represents parsed manifest of repo project. It offers to get Project by name/path and so to enable name-to-path/path-to-name resolution.

.. container:: expand-container conf-macro output-block
   :name: expander-807011084

   .. container:: expand-control
      :name: expander-control-807011084

       com.amarula.repo.Repo

   .. container:: expand-content expand-hidden
      :name: expander-content-807011084

      Create new instance per repo project. Init, sync, cherry-pick/checkout topics for projects or manifest.

.. _Gerrittriggerforrepoprojects-Exampleusageoflibrary:

Example usage of library
------------------------

::

         @Library('repo_jenkins_lib')
         import com.amarula.gerrit.GerritChange
         import com.amarula.repo.Repo

         node {
           stage('Repo init and sync') {
             def changes = []
             def value = GerritChange.FAILURE
             withCredentials([usernamePassword(
                 credentialsId: 'jenkins-builder-amarula_gerrit-rest-api',
                 passwordVariable: 'GERRIT_RESTAPI_PASS',
                 usernameVariable: 'GERRIT_RESTAPI_USER')]) {
               try {
                 def project = new Repo(this, env,
                     'ssh://gitea@gitea.amarulasolutions.com:38745/myAndroidProject/manifest.git')
                 sshagent(['someCredentialId1', 'someCredentialId2']) {
                   // repo init
                   project.init()

                   // checkout topic changes for manifest
                   changes.addAll(project.checkoutTopicForManifest(env.GERRIT_TOPIC))
                   
                   // repo sync
                   project.sync()
                   
                   // checkout topic changes for projects
                   changes.addAll(project.checkoutTopic(env.GERRIT_TOPIC))

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
