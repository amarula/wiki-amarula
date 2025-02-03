Warning-ng Jenkins plugin now can report Valgrind memory leak
==============================================================

.. figure:: /images/valgrind-warning.png
   :align: center
|
|

Amarula Solutions

Optimizing IoT Development at Amarula Solutions: A Focus on Memory Safety
*************************************************************************

At Amarula Solutions, we are constantly striving to optimize our IoT development processes.
A recent focus has been on enhancing memory safety and stability within our embedded systems.
This article details a significant improvement we've made in this area.

The Challenge:
**************

Memory leaks and other memory-related issues can have severe consequences in embedded systems, leading to unpredictable behavior, system crashes, and ultimately, device failures. To mitigate these risks, we implemented a robust system for detecting and preventing memory-related problems.   

The Solution:
*************

* Valgrind Integration: We integrated the valgrindParser tool into our build process. This powerful tool analyzes memory usage during runtime, identifying potential memory leaks, invalid memory accesses, and other memory-related errors.   

* Enhanced Issue Tracking: To streamline issue tracking, we modified our build system to retain issue records only for the most recent build. This ensures a clean and focused issue history, preventing clutter from older builds and improving the efficiency of issue resolution.

* Robust Quality Gates: We established strict quality gates. Any memory leaks or other issues detected by Valgrind will immediately cause the build to fail, preventing potentially problematic code from being deployed and ensuring only memory-safe code reaches our devices.

* Local Testing and Deployment: Before integrating changes into our production environment, we rigorously test them on a local Jenkins instance (version 2.489). This allows for thorough validation and minimizes the risk of unintended side effects.

* Open Source Contribution: We have merged these improvements into the warning-ng project, contributing to the open-source community and potentially benefiting other developers facing similar challenges.

Benefits:
*********

* Improved Code Quality: Proactive identification and resolution of memory issues significantly enhance the robustness and long-term stability of our IoT devices.

* Enhanced Development Efficiency: By preventing memory-related issues early in the development cycle, we reduce the time and effort required for debugging and rework, leading to faster development cycles and increased productivity.

* Increased Customer Satisfaction: By delivering more reliable and stable devices, we enhance customer satisfaction and build stronger relationships with our customers.

Conclusion:
***********

This initiative represents a significant step forward in our commitment to delivering high-quality,
reliable IoT solutions. By continuously improving our development processes and leveraging 
open-source tools and best practices, we are well-positioned to meet the evolving demands of the IoT landscape.

Example of Jenkins pipeline
***************************

.. figure:: /images/pipeline-overview.png
   :align: center
|
|

.. code-block:: groovy

   #!groovy

   import com.amarula.build.Verification

   node('android-os-build') {

       def dockerImage = 'qio-builder:latest'
       def manifestUrl = "${GITEA_SSH_URL}/duckduck/manifest.git"
       def credentials = ['c4f9fa8c-45d7-459e-a645-203f1245d914', '9af8a985-9516-467e-b9cb-0174692fe8c0']

       env.REPO_URL = 'https://lnkd.in/dRV_qssT'
       env.REPO_BRANCH = 'main'

       final def buildCode = [
           'Build all' : {
               sh """#!/bin/bash
                     source build/envsetup.sh
                     rm -rf out/
                     make all"""
           },
           'Performing tests' : {
               stages = [:]
               stages['Check formatting'] = {
                   sh """#!/bin/bash
                         find firmware -name "*.c" -or -name "*.h" | xargs clang-format -n &> out/clang-format.txt"""

                   recordIssues sourceCodeRetention: 'MODIFIED',
                                sourceCodeEncoding: 'UTF-8',
                                tool: groovyScript(parserId: 'clang-format',
                                pattern: 'out/clang-format.txt', reportEncoding:'UTF-8'),

                   qualityGates: [[threshold: 1, type: 'TOTAL', criticality: 'FAILURE']]

                   if (currentBuild.result == 'FAILURE') {
                       error("Formatting errors found")
                   }
               }
               stages['Run memcheck'] = {
                   sh """#!/bin/bash
                         source build/envsetup.sh
                         make memcheck"""

                   recordIssues sourceCodeRetention: 'MODIFIED',
                                tool: valgrind(pattern: "out/test/memcheck.xml"),

                   qualityGates: [[threshold: 1, type: 'TOTAL', criticality: 'FAILURE']]

                   if (currentBuild.result == 'FAILURE') {
                       error("Formatting errors found")
                   }
               }
               stages['Run Unit tests'] = {
                   sh """#!/bin/bash
                         source build/envsetup.sh
                         make test"""

                   junit 'out/test/results.xml'

                   recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'out/test/coverage.xml']])
                   recordIssues sourceCodeRetention: 'MODIFIED', tools: [sphinxBuild()]

                   if (currentBuild.result == 'UNSTABLE') {
                       error("Unable to complete test")
                   }
               }

               parallel(stages)
           }
       ]
       ver = new Verification(this, env, credentials)
       def options = ['dockerImage': dockerImage]
       ver.repoBuild(manifestUrl, buildCode, options)
   }


.. figure:: /images/pipeline-console.png
   :align: center
