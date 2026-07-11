Global variables
****************

.. note:: **TL;DR**
   - Reference of **Jenkins global environment variables** configured at Amarula Solutions — covering **URL variables** (Archiva, Docker Registry, Gerrit, Gitea, Mattermost, SFTP), **Ruby path variables**, and **AWS tuning variables** for S3 artifact management and session duration.
   - These variables enable consistent pipeline configuration across all Amarula Jenkins projects.

Jenkins exports variables for jobs when they are executed. Some of them are configured from Jenkins and plugins (see https://jenkins.amarulasolutions.com/job/amarula/job/test/pipeline-syntax/globals) and some of them are defined by Jenkins administrators (Manage Jenkins → Configure System → Global properties.

Variables defined by administrators can be referenced in the configuration itself and are exported to shell environment and are also accessible in the pipeline script.

.. _Globalvariables-URLvariables:

URL variables
=============

.. container:: table-wrap

   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | Variable name                 | Value                                                      | Description                                               |
   +===============================+============================================================+===========================================================+
   | ARCHIVA_URL                   | archiva.amarulasolutions.com                               |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | ARCHIVA_RELEASE_REPO_URL      | https://${ARCHIVA_URL}/artifacts/repository/releases/      |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | ARCHIVA_SNAPSHOT_REPO_URL     | https://${ARCHIVA_URL}/artifacts/repository/snapshots/     |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | DOCKER_REGISTRY_URL           | registry.amarulasolutions.com                              |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | DOCKER_REGISTRY_HTTPS_URL     | https://${DOCKER_REGISTRY_URL}:443                         |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | DOCKER_REGISTRY_USER          | amarula-docker                                             |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | GERRIT_URL                    | gerrit-review.amarulasolutions.com                         |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | GERRIT_SSH_JENKINSBUILDER_URL | ssh://jenkins-builder-amarula@${GERRIT_URL}:29418          | URL to use gerrit via SSH as user jenkins-builder-amarula |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | GITEA_URL                     | gitea.amarulasolutions.com                                 |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | GITEA_SSH_URL                 | ssh://gitea@${GITEA_URL}:38745                             | URL to use gitea via SSH                                  |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | MATTERMOST_URL                | mattermost.amarulasolutions.com                            |                                                           |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | MATTERMOST_ENDPOINT_URL       | https://${MATTERMOST_URL}/hooks/awdjf7bzopyodgo9h86yd71axw | URL to use as endpoint in mattermostSend                  |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | MATTERMOST_WH_ENDPOINT_URL    | https://${MATTERMOST_URL}/hooks/393yc99qa7n1bft1u5ktu1rxkr | URL to use as endpoint in mattermostSend for W&H team     |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+
   | SFTP_URL                      | secure-storage.amarulasolutions.com                        | Amarula SFTP                                              |
   +-------------------------------+------------------------------------------------------------+-----------------------------------------------------------+

.. _Globalvariables-Rubyvariables:

Ruby variables
==============

.. container:: table-wrap

   +------------------+---------------------+----------------------------------------------------------------------------+
   | Variable name    | Value               | Description                                                                |
   +==================+=====================+============================================================================+
   | DEFAULT_GEM_PATH | /home/jenkins/.gem/ | Path to use when using bundler "bundle install --path ${DEFAULT_GEM_PATH}" |
   +------------------+---------------------+----------------------------------------------------------------------------+

|

.. _Globalvariables-AWStuningvariable:

AWS tuning variable
===================

More configuration is need to delete artifacts in aws and to increase session timeout in /etc/default/jenkins file or /etc/systemd/system/jenkins.service.d/override.conf

::

         # delete artifacts on the S3 Bucket
         JAVA_ARGS="${JAVA_ARGS} -Dio.jenkins.plugins.artifact_manager_jclouds.s3.S3BlobStoreConfig.deleteArtifacts=true"

         # delete stashes on the S3 Bucket
         JAVA_ARGS="${JAVA_ARGS} -Dio.jenkins.plugins.artifact_manager_jclouds.s3.S3BlobStoreConfig.deleteStashes=true"

         # increase aws session timeout
         JAVA_ARGS="${JAVA_ARGS} -Dio.jenkins.plugins.aws.global_configuration.CredentialsAwsGlobalConfiguration.sessionDuration=7200"

.. tip::
   Need consistent pipeline configuration across your CI/CD infrastructure?
   Amarula Solutions sets up global environment variables, credential
   management, and AWS/S3 integration for Jenkins at scale.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
