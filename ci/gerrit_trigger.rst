Gerrit trigger
***************

plugin page: https://plugins.jenkins.io/gerrit-trigger

source: https://github.com/jenkinsci/gerrit-trigger-plugin

.. container:: toc-macro client-side-toc-macro conf-macro output-block

.. _Gerrittrigger-SetupinPipelineconfiguration:

Setup in Pipeline configuration
===============================

See example of typical configuration below:

.. image:: /images/gerrit_trigger_configuration.png

Notice that you can add more trigger events beside "Patchset Created", see complete list below. You can also use this pipeline for more projects by using "Add Project" button.

We don't want Jenkins to set Code-Review label, only Verified, so we need to configure this via the "Advanced..." options in the configuration: Fill the fields under "Code Review" with zeros.

.. image:: /images/gerrit_trigger_config_1.png

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   .. container:: confluence-information-macro-body

      In order to provide the verification label in gerrit, there has to be the gerrit user dedicated to jenkins with access rights set to set label for the project.

.. _Gerrittrigger-TriggerEvents:

Trigger Events
--------------

-  **Draft Published:** Sent when a change moves from draft state to new.
-  **Patchset Created:** Sent when a new patchset arrives on a change.
-  **Change Merged:** Sent when a change is merged on the Gerrit server.
-  **Comment Added:** Sent when a comment is added to a change. Which category and value to trigger on can be configured. The available categories can be configured in the server settings for the plugin.
-  **Ref Updated:** Sent when a ref is updated on the Gerrit server, i.e. someone pushes code review.

.. _Gerrittrigger-Pipelinesteps:

Pipeline steps
==============

**setGerritReview**: Allows altering the Gerrit review posted at the end of build during the build.

.. _Gerrittrigger-Pipelinetriggerparameters:

Pipeline trigger parameters
===========================

Not all of them has to be set. Accessible as environment variables.

**GERRIT_CHANGE_SUBJECT:** Parameter name for the commit subject (commit message's 1st line).

**GERRIT_CHANGE_COMMIT_MESSAGE:** Parameter name for the full commit message.

**GERRIT_BRANCH:** Parameter name for the branch.

**GERRIT_TOPIC:** Parameter name for the topic.

**GERRIT_OLD_TOPIC:** Parameter name for the old topic (in case of topic was changed).

**GERRIT_TOPIC_CHANGER:** The name and email of the changer of the topic.

**GERRIT_TOPIC_CHANGER_NAME:** The name of the changer of the topic.

**GERRIT_TOPIC_CHANGER_EMAIL: **\ The email of the changer of the topic.

**GERRIT_CHANGE_ID:** Parameter name for the change-id.

**GERRIT_CHANGE_NUMBER: **\ Parameter name for the change number.

**GERRIT_CHANGE_URL:** Parameter name for the URL to the change.

**GERRIT_PATCHSET_NUMBER:** Parameter name for the patch set number.

**GERRIT_PATCHSET_REVISION:** Parameter name for the patch set revision.

**GERRIT_PROJECT:** Parameter name for the Gerrit project name.

**GERRIT_REFSPEC:** Parameter name for the refspec.

**GERRIT_CHANGE_ABANDONER:** The name and email of the abandoner of the change.

**GERRIT_CHANGE_ABANDONER_NAME:** The name of the abandoner of the change.

**GERRIT_CHANGE_ABANDONER_EMAIL:** The email of the abandoner of the change.

**GERRIT_CHANGE_OWNER:** The name and email of the owner of the change.

**GERRIT_CHANGE_OWNER_NAME:** The name of the owner of the change.

**GERRIT_CHANGE_OWNER_EMAIL:** The email of the owner of the change.

**GERRIT_CHANGE_RESTORER:** The name and email of the restorer of the change.

**GERRIT_CHANGE_RESTORER_NAME:** The name of the restorer of the change.

**GERRIT_CHANGE_RESTORER_EMAIL:** The email of the restorer of the change.

**GERRIT_PATCHSET_UPLOADER:** The name and email of the uploader of the patch-set.

**GERRIT_PATCHSET_UPLOADER_NAME:** The name of the uploader of the patch-set.

**GERRIT_PATCHSET_UPLOADER_EMAIL:** The email of the uploader of the patch-set.

**GERRIT_EVENT_ACCOUNT:** The name and email of the person who triggered the event.

**GERRIT_EVENT_ACCOUNT_NAME:** The name of the person who triggered the event.

**GERRIT_EVENT_ACCOUNT_EMAIL:** The email of the person who triggered the event.

**GERRIT_REFNAME:** The refname in a ref-updated event.

**GERRIT_OLDREV:** The old revision in a ref-updated event.

**GERRIT_NEWREV:** The new revision in a ref-updated or change-merged event.

**GERRIT_SUBMITTER:** The submitter in a ref-updated event.

**GERRIT_SUBMITTER_NAME:** The name of the submitter in a ref-updated event.

**GERRIT_SUBMITTER_EMAIL:** The email of the submitter in a ref-updated event.

**GERRIT_NAME:** The name of the Gerrit instance.

**GERRIT_HOST:** The host of the Gerrit instance.

**GERRIT_PORT:** The port number of the Gerrit instance.

**GERRIT_SCHEME:** The protocol scheme of the Gerrit instance.

**GERRIT_VERSION:** The version of the Gerrit instance.

**GERRIT_EVENT_HASH:** A hashcode of the Gerrit event object, to make sure every set of parameters is unique (allowing jenkins to queue duplicate builds).

**GERRIT_EVENT_TYPE:** The type of the event.

**GERRIT_EVENT_COMMENT_TEXT:** Comment posted to Gerrit in a comment-added event.

.. _Gerrittrigger-Exampleofvalues:

Example of values
-----------------

.. container:: expand-container conf-macro output-block
   :name: expander-1547571607

   .. container:: expand-control
      :name: expander-control-1547571607

       Click here to expand...

   .. container:: expand-content expand-hidden
      :name: expander-content-1547571607

      .. container:: code panel pdl conf-macro output-block

         .. container:: codeContent panelContent pdl

            .. code:: syntaxhighlighter-pre

               GERRIT_CHANGE_ID=I2237c5a9a364df5d5e9f49950768df323110a19c
               GERRIT_CHANGE_NUMBER=4039
               GERRIT_CHANGE_OWNER=\"Ondrej Pik\" <ondrej@amarulasolutions.com>
               GERRIT_CHANGE_OWNER_EMAIL=ondrej@amarulasolutions.com
               GERRIT_CHANGE_OWNER_NAME=Ondrej Pik
               GERRIT_CHANGE_SUBJECT=Test triggers
               GERRIT_CHANGE_URL=https://gerrit-review.amarulasolutions.com/4039
               GERRIT_EVENT_HASH=-2023676231
               GERRIT_EVENT_TYPE=patchset-created
               GERRIT_HOST=gerrit-review.amarulasolutions.com
               GERRIT_NAME=Amarula Solutions Gerrit
               GERRIT_PATCHSET_NUMBER=1
               GERRIT_PATCHSET_REVISION=03d9debf16a0d3f0eb0d949cd45ca4ccb3604c10
               GERRIT_PATCHSET_UPLOADER=\"Ondrej Pik\" <ondrej@amarulasolutions.com>
               GERRIT_PATCHSET_UPLOADER_EMAIL=ondrej@amarulasolutions.com
               GERRIT_PATCHSET_UPLOADER_NAME=Ondrej Pik
               GERRIT_PORT=29418
               GERRIT_PROJECT=aevi-albert/qa-automated-tests
               GERRIT_REFSPEC=refs/changes/39/4039/1
               GERRIT_SCHEME=ssh
               GERRIT_VERSION=2.14.6

.. _Gerrittrigger-Usefulcodesnippets:

Useful code snippets
--------------------

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         //def repoUrl = 'ssh://jenkins-builder-amarula@gerrit-review.amarulasolutions.com:29418/aevi-albert/qa-automated-tests'
         def repoUrl = "ssh://jenkins-builder-amarula@${GERRIT_HOST}:${GERRIT_PORT}/${GERRIT_PROJECT}"
