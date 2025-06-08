.. _dsl_pipeline_verification:

=======================================================
DSL Pipeline for Espressif Project Verification Builds
=======================================================

This article outlines the process of setting up a Jenkins DSL (Domain Specific Language) pipeline for automated verification builds of Espressif projects, integrated with Gerrit for code review. This setup ensures that every proposed change undergoes a thorough build and test process before being merged, enhancing code quality and stability.

Introduction
------------

Automated verification is crucial in continuous integration and delivery workflows. For Espressif projects, which often involve embedded firmware, a robust CI/CD pipeline is essential. By leveraging Jenkins and Gerrit, we can create a system where every patchset submitted to Gerrit triggers a verification build on Jenkins, providing immediate feedback to developers.

Prerequisites
-------------

Before you begin, ensure you have the following:

* A running Jenkins instance with the Job DSL plugin installed.
* A Gerrit server configured for your Espressif projects.
* Necessary Jenkins credentials for Git (e.g., SSH keys for Gitea).
* Docker installed on your Jenkins agent for containerized builds.

Jenkins DSL Pipeline Configuration
----------------------------------

The core of this setup is a Jenkins Job DSL script that defines the pipeline. This script automates the creation and configuration of the Jenkins job.

**1. Jenkins Job Definition**

The DSL script defines a `pipelineJob` that is triggered by Gerrit events.

.. code-block:: groovy

    pipelineJob("amarula/duckacme/acme-verification") {
        description("ACME verification gerrit trigger")
        keepDependencies(false)
        definition {
            cpsScm {
                scm {
                    git {
                        remote {
                            url("ssh://gitea@gitea.amarulasolutions.com:38745/duckacme/jenkins_ci.git")
                            credentials("c4f9fa8c-45d7-459e-a645-203f1245d914")
                        }
                        branch("*/main")
                    }
                }
                scriptPath("acme_Jenkinsfile")
            }
        }
        disabled(false)
        logRotator {
            numToKeep(10)
            daysToKeep(20)
        }
        // ... (rest of the job definition)
    }

* **`pipelineJob("amarula/duckacme/acme-verification")`**: Defines a new Jenkins pipeline job.
* **`description`**: A human-readable description for the job.
* **`cpsScm`**: Specifies that the pipeline script is loaded from Source Control Management.
* **`git`**: Configures the Git repository where the `Jenkinsfile` resides.
    * **`url`**: The URL of your Jenkins CI Git repository.
    * **`credentials`**: The Jenkins credentials ID for accessing the Git repository.
    * **`branch`**: The branch to checkout (e.g., `*/main` to match any remote main branch).
* **`scriptPath("acme_Jenkinsfile")`**: The path to the Jenkinsfile within the Git repository.
* **`logRotator`**: Configures log retention for the job.

**2. Gerrit Trigger Configuration**

The pipeline is configured to be triggered by specific events in Gerrit.

.. code-block:: groovy

    properties {
        pipelineTriggers {
            triggers {
                gerrit {
                    serverName('Amarula Solutions Gerrit')
                    triggerOnEvents {
                        patchsetCreated {
                            excludeDrafts(true)
                            excludeWipState(true)
                        }
                    }
                    gerritProjects {
                        gerritProject {
                            compareType('ANT')
                            pattern('duckacme/build')
                            branches {
                                branch {
                                    compareType('ANT')
                                    pattern('**')
                                }
                            }
                            disableStrictForbiddenFileVerification(false)
                        }
                        gerritProject {
                            compareType('ANT')
                            pattern('duckacme/firmware')
                            branches {
                                branch {
                                    compareType('ANT')
                                    pattern('**')
                                }
                            }
                            disableStrictForbiddenFileVerification(false)
                        }
                        gerritProject {
                            compareType('ANT')
                            pattern('duckacme/manifest')
                            branches {
                                branch {
                                    compareType('ANT')
                                    pattern('**')
                                }
                            }
                            disableStrictForbiddenFileVerification(false)
                        }
                    }
                }
            }
        }
    }

* **`gerrit`**: Configures the Gerrit trigger.
* **`serverName`**: The name of your Gerrit server as configured in Jenkins.
* **`triggerOnEvents { patchsetCreated { ... } }`**: The pipeline will be triggered when a new patchset is created.
    * **`excludeDrafts(true)`**: Prevents triggering on draft patchsets.
    * **`excludeWipState(true)`**: Prevents triggering on Work-In-Progress patchsets.
* **`gerritProjects`**: Defines which Gerrit projects will trigger the build.
    * **`gerritProject`**: Each block specifies a project to monitor.
        * **`compareType('ANT')`**: Uses ANT-style patterns for matching.
        * **`pattern('duckacme/build')`**: Matches the `duckacme/build` project. Similar patterns are used for `duckacme/firmware`  and `duckacme/manifest`.
        * **`branches { branch { pattern('**') } }`**: Monitors all branches within the specified projects.

Jenkinsfile Implementation
--------------------------

The `acme_Jenkinsfile` contains the actual pipeline stages for building and testing the Espressif project. It runs on a designated agent (e.g., `firmware-nodes`) and utilizes Docker for a consistent build environment.

.. code-block:: groovy

    node('firmware-nodes') {
        jobDsl scriptText: dslScript, ignoreExisting: true
        def dockerImage = 'acme-builder:latest'
        def manifestUrl = "${GITEA_SSH_URL}/duckacme/manifest.git"
        def credentials = ['c4f9fa8c-45d7-459e-a645-203f1245d914', '9af8a985-9516-467e-b9cb-0174692fe8c0']

        env.REPO_URL = 'https://android.googlesource.com/tools/repo'
        env.REPO_BRANCH = 'main'
        env.GERRIT_TOPIC = '' // We don't want to be triggered by topic

        final def buildCode = [
            'Build firmware' : {
                sh """#!/bin/bash
                   source build/envsetup.sh
                   rm -rf out/
                   make build"""
            },
            'Build Documentation' : {
                sh """#!/bin/bash
                   source build/envsetup.sh
                   make docs"""
            },
            'Performing tests' : {
                def stages = [:]

                stages['Check formatting'] = {
                    sh """#!/bin/bash
                       find firmware -name "*.c" -or -name "*.h" |
                       xargs clang-format -n &> out/clang-format.txt"""
                    recordIssues sourceCodeRetention: 'MODIFIED',
                       sourceCodeEncoding: 'UTF-8',
                       tool: groovyScript(parserId: 'clang-format',
                       pattern: 'out/clang-format.txt', reportEncoding:'UTF-8'),
                       qualityGates: [[threshold: 1, type: 'TOTAL', criticality: 'FAILURE', unstable: false]]
                }
                stages['Check cmake formatting'] = {
                    sh """#!/bin/bash
                       find firmware -name "CMakeLists.txt"
                       -o -name "*.cmake" | xargs cmake-lint &> out/cmake-tidy.txt || true"""
                    recordIssues sourceCodeRetention: 'MODIFIED',
                       tool: pyLint(pattern: 'out/cmake-tidy.txt'),
                       qualityGates: [[threshold: 1, type: 'TOTAL', criticality: 'FAILURE', unstable: false]]
                }
                stages['Run memcheck'] = {
                    sh """#!/bin/bash
                       source build/envsetup.sh
                       make memcheck"""
                    recordIssues sourceCodeRetention: 'MODIFIED',
                       tool: valgrind(pattern: "out/test/memcheck.xml"),
                       qualityGates: [[threshold: 1, type: 'TOTAL', criticality: 'FAILURE', unstable: false]]
                }
                stages['Run Unit tests'] = {
                    sh """#!/bin/bash
                       source build/envsetup.sh
                       make test"""
                    junit 'out/test/results.xml'
                    recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'out/test/coverage.xml']])
                    recordIssues sourceCodeRetention: 'MODIFIED',
                        tools: [sphinxBuild()],
                        qualityGates: [[threshold: 0, type: 'TOTAL', criticality: 'FAILURE', unstable: false]]
                }
                parallel(stages)
            }
        ]
        def ver = new Verification(this, env, credentials)
        def options = ['dockerImage': dockerImage]
        ver.repoBuild(manifestUrl, buildCode, options)
    }

* **`node('firmware-nodes')`**: Specifies the Jenkins agent where the pipeline will run.
* **`dockerImage = 'acme-builder:latest'`**: Defines the Docker image to be used for the build environment. This ensures all dependencies are consistently available.
* **`manifestUrl`**: The URL for the manifest repository.
* **`credentials`**: A list of Jenkins credential IDs required for accessing repositories.
* **`env.REPO_URL`, `env.REPO_BRANCH`, `env.GERRIT_TOPIC`**: Environment variables set for the build process.
* **`buildCode`**: A map defining different build and test stages.

    * **'Build firmware'**:
        * Executes shell commands to set up the build environment (`source build/envsetup.sh`), clean the output directory, and build the firmware (`make build`).
    * **'Build Documentation'**:
        * Executes shell commands to set up the build environment and build the project documentation (`make docs`).
    * **'Performing tests'**: This stage runs several tests in parallel:
        * **'Check formatting'**:
            * Uses `clang-format` to check C/C++ file formatting.
            * `recordIssues` is used to report findings with a quality gate, failing the build if more than 1 issue is found.
        * **'Check cmake formatting'**:
            * Uses `cmake-lint` to check CMake file formatting.
            * Reports issues and applies a quality gate.
        * **'Run memcheck'**:
            * Executes `make memcheck` to run memory leak checks.
            * `recordIssues` is configured with `valgrind` parser and a quality gate.
        * **'Run Unit tests'**:
            * Executes `make test` to run unit tests.
            * `junit` publishes test results from `out/test/results.xml`.
            * `recordCoverage` collects code coverage reports using Cobertura format.
            * `recordIssues` with `sphinxBuild()` and a quality gate.
* **`ver.repoBuild(manifestUrl, buildCode, options)`**: This is a call to a custom `Verification` class (presumably from `com.amarula.build.Verification`) that orchestrates the repository synchronization and execution of the defined build stages.

Conclusion
----------

By implementing this Jenkins DSL pipeline, you can establish a robust and automated verification process for your Espressif projects. This integration with Gerrit ensures that code quality is maintained through continuous testing and immediate feedback, significantly improving the development workflow and reducing the likelihood of regressions.
