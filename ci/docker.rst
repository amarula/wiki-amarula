Build Dependency Cache for Docker Jobs
***************************************

Docker jobs on Jenkins always starts clean, so time and bandwidth are usually wasted in downloading the same build dependencies again and again. This page shows how you can configure the jobs to use a proxy cache for the build dependencies in various build systems.

A proxy cache is like a proxy server for downloading build dependencies, but it caches the files and reuse them the next time the same files are downlaoded. Many artifact hosting projects support such features.

Another approach would be to cache the job outputs and restore them on the next job, similar to `GitHub Actions <https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows>`__. Unfortunately, Jenkins has no such feature.

.. _BuildDependencyCacheforDockerJobs-Howtouseinapipeline:

How to use in a pipeline
========================

Beware that we only need to care about Docker jobs. Jenkins jobs not running in Docker are run in the same system and thus share the build system like Gradle Daemon.

This shows a simple pipeline that will use the proxy cache:

::

         import com.amarula.build.Verification
         node('android-build') {
             final def ver = new Verification(this, env, 'XXX')
             final def repoUrl = "${GERRIT_SSH_JENKINSBUILDER_URL}/ipco_navy/wcs_ipcosip_benchmark"
             final def buildCode = {
                 sh "gradle check"
             }
             ver.build(repoUrl, buildCode, 'docker.io/gradle:jdk11')
         }

The most important thing here is that the name of the Docker image is specified in method ``Verification#build()`` .

By utilizing this particular Jenkins library method, the job will be run in a Docker container configured to use the proxy cache provided by a Sonatype Nexus instance dedicated to the Jenkins node. Supported build systems include:

-  Gradle (See also: `the initialization script <https://gerrit-review.amarulasolutions.com/c/i-tools/ci_jenkins_lib/+/25765>`__)
-  Grails
-  npm
-  Yarn (Won't work because ``package-lock.json`` references npm registry. See https://github.com/yarnpkg/rfcs/pull/64)

See `this directory <https://gerrit-review.amarulasolutions.com/plugins/gitiles/i-tools/ci_jenkins_lib/+/refs/heads/master/resources/com/amarula/build/docker/proxy-cache/nexus-repositories/>`__ for all the public repositories configured in the Sonatype Nexus instance.

.. _BuildDependencyCacheforDockerJobs-WorkaroundforYarn(WIP):

Workaround for Yarn (WIP)
=========================

Yarn does not honor the overridden registry if a ``package-lock.json`` exists. A workaround is to replace the registry URL in that file with the proxy cache URL. For example, add this before running Yarn:

::

         sh "touch ~/.yarnrc.yml"
         final def registry = sh(
             script: "yq .npmRegistryServer ~/.yarnrc.yml",
             returnStdout: true,
         ).trim()
         if (registry != "null") {
             echo "Replacing the hardcoded registry in `package-lock.json` with $registry"
             sh "sed --in-place --expression='s|\"resolved\": \"https://registry.npmjs.org|\"resolved\": \"${registry}|g' package-lock.json"
         }

.. _BuildDependencyCacheforDockerJobs-ImplementationdetailsoftheJenkinslibrary:

Implementation details of the Jenkins library
=============================================

`This patch <https://gerrit-review.amarulasolutions.com/c/i-tools/ci_jenkins_lib/+/26052>`__ implements the process of running the proxy cache service. Here are some diagrams demonstrating the process:

.. image:: /images/jenkins_lib_impl1.png

.. image:: /images/jenkins_lib_impl2.png
