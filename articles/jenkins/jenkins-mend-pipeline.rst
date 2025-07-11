Building Secure Yocto Images: An In-Depth Look at a Jenkins Pipeline with Mend SCA Integration 🔒
=================================================================================================

.. figure:: /images/mend-security.png
   :align: center

|
|

Developing custom embedded Linux systems requires a robust and automated build
process that prioritizes both efficiency and security. This article details a
sophisticated Jenkins pipeline designed to build Yocto-based images, showcasing its
integration with Mend Software Composition Analysis (SCA) for comprehensive
vulnerability scanning. This pipeline streamlines the development workflow,
automates crucial tasks, and significantly enhances the security posture of the
resulting embedded images.

Example Jenkins Pipeline
------------------------

.. code-block:: groovy

    #!groovy

    import com.amarula.build.Build
    import com.amarula.changelog.Changelog
    import com.amarula.git.Git
    import com.amarula.ui.Ui

    def runContainerCmd(String cmd, String config) {
        sh """
           #!/bin/bash -xe
           KAS_CONTAINER_IMAGE="registry.amarulasolutions.com:443/custom-builder:1.0" kas-container shell $config -c "$cmd"
        """
    }

    def runYoctoTargetBuild(String target, String config, boolean mend = false) {
        withCredentials([string(credentialsId: 'MEND_API_KEY', variable: 'mend_api_key'),
                         string(credentialsId: 'MEND_USERKEY', variable: 'mend_user_key'),
                         string(credentialsId: 'MEND_PRODUCT_TOKEN', variable: 'mend_product_token')]) {
            String options

            if (mend) {
                options = "--runtime-args \"-e WS_PRODUCTTOKEN=$mend_product_token -e WS_APIKEY=$mend_api_key -e WS_USERKEY=$mend_user_key -e JENKINS_BUILD_ID=jenkins_${env.BUILD_ID}\""
            } else {
                options = "--runtime-args \"-e JENKINS_BUILD_ID=jenkins_${env.BUILD_ID}\""
            }

            sh """
               #!/bin/bash -xe
               mkdir -p ${HOME}/data
               export SSTATE_DIR="${HOME}/data/bitbake.sstate"
               export DL_DIR="${HOME}/data/bitbake.downloads"
               mkdir -p ssh-build-hosts
               KAS_CONTAINER_IMAGE="registry.amarulasolutions.com:443/custom-builder:1.0" kas-container \\
               $options --ssh-dir ssh-build-hosts --ssh-agent shell $config -c \\
               "bitbake $target"
            """
       }
    }

    throttle(['heavy_job']) { node('build-node') {
        def credentials = ['credential-id-1', 'credential-id-2']
        def manifestUrl = "${GITEA_SSH_URL}/project/meta-project.git"

        /* Set job description */
        currentBuild.displayName = 'project_' + (env.GERRIT_TOPIC ? "${env.GERRIT_TOPIC}_" : '') + env.BUILD_NUMBER

        def ui = new Ui.Builder(this)
                       .addStringParameter("BRANCH", 'master', "The branch to start from in order to build. Tag are valid too")
                       .addStringParameter("GERRIT_TOPIC", '', "Gerrit Topic to cherry-pick, separated by ,")
                       .addBooleanParameter("CLEAN_STATE_CACHE", false, "Force of the clean of state cache.")
                       .addBooleanParameter("KEEP_BUILD", false, "If you want to keep build select it")
                       .addBooleanParameter("ENABLE_MEND", false, "If you want to run Mend Analisys")
                       .build()

        def buildCode = [
            'Clean state cache' : {
                runYoctoTargetBuild("-fc cleansstate image-type-a", "kas/config-a.yaml")
            },
            'Yocto image Type A' : {
                String mendPath = "build/tmp-glibc/log/mend"
                /* Clean up old report if any */
                dir (mendPath) {
                    deleteDir()
                }
                runYoctoTargetBuild("image-type-a image-type-b", "kas/config-b.yaml:kas/security.yaml", ENABLE_MEND.toBoolean())
                recordIssues sourceCodeRetention: 'LAST_BUILD',
                         tools: [yoctoScanner(pattern: "build/tmp-glibc/log/cve/cve-summary.json")]
                if (ENABLE_MEND.toBoolean()) {
                    archiveArtifacts "build/tmp-glibc/log/mend/mend-report-*.json"
                }
            },
            'Release notes' : {
                ...
            },
            'Archive artifacts' : {
                ...
            }
        ]

    if (CLEAN_STATE_CACHE.toBoolean() == false) {
        buildCode.remove('Clean state cache')
    }

    def ver = new Build(this, env, credentials)
    def options = ['branch': BRANCH, history: true, 'gerritProject': 'project/meta-project']
    ver.setSyncMethod(Build.CHERRYPICK)
    ver.build(manifestUrl, buildCode, options)

    if (KEEP_BUILD.toBoolean()) {
        currentBuild.setKeepLog(true)
    }

    }}


Pipeline Overview: Orchestrating the Yocto Build Process ⚙️
-----------------------------------------------------------

The Jenkins pipeline operates within a throttle block, limiting concurrent "heavy_job"
executions on a designated node (build-node), ensuring resource efficiency. It utilizes
several custom Groovy functions and a well-structured set of build stages to manage
the complexities of embedded system development.

Core Functions: The Building Blocks 🏗️
**************************************

runContainerCmd(String cmd, String config): This function serves as the primary
mechanism for executing commands within a kas-container. It relies on a specific container
image (registry.amarulasolutions.com:443/custom-builder:1.0), providing a consistent
and isolated environment for all build operations.

runYoctoTargetBuild(String target, String config, boolean mend = false): This is the
central function for generating Yocto images. It establishes essential environment variables
such as SSTATE_DIR (shared state cache) and DL_DIR (downloads directory) to optimize build times.
Crucially, it manages Mend SCA integration: if the mend parameter is true, it securely injects
Mend API keys and product tokens as runtime arguments into the kas-container,
enabling vulnerability scanning during the build. SSH keys for Git repositories
are also pre-configured, facilitating seamless source code access.

User Configuration and Control 🎮
*********************************

The pipeline offers several configurable parameters through its user interface,
providing developers with fine-grained control over the build process:

**BRANCH**: Specifies the Git branch or tag from which to build (defaults to master).

**GERRIT_TOPIC**: Allows for cherry-picking specific Gerrit changes into the build.

**CLEAN_STATE_CACHE**: A boolean flag that, when true, forces a complete clean of
the Yocto shared state cache, ensuring a pristine build environment.

**KEEP_BUILD**: A boolean parameter that determines whether build artifacts should
be retained after the Jenkins job completes.

**ENABLE_MEND**: This critical boolean parameter directly controls whether
Mend SCA vulnerability analysis is performed.

Deeper Dive into Build Stages: From Clean to Cloud 🚀
*****************************************************

The heart of the pipeline resides within the buildCode map, which defines a series
of distinct and often interdependent build stages. All of them allow not only to
build Yocto OS and archive it but even scan for vulnerabilities and license
compliance.

The Role of meta-mend: Powering Vulnerability Analysis 🛡️
*********************************************************

The meta-mend Yocto layer is instrumental in integrating Mend SCA into the build process.
It provides a BitBake class (bbclass) that allows Yocto to interact seamlessly
with the Mend platform for comprehensive open-source vulnerability scanning.

How meta-mend Works in the Pipeline:

**Containerized Environment**: meta-mend requires a Java runtime environment. The
pipeline addresses this by utilizing a kas-container image (registry.amarulasolutions.com:443/custom-builder:1.0)
that specifically includes Java, thereby fulfilling this prerequisite for the Mend analysis.

**Configuration Injection**: During the runYoctoTargetBuild function call, when ENABLE_MEND is set to true,
essential Mend configuration variables (WS_USERKEY, WS_APIKEY, WS_PRODUCTTOKEN, WS_WSS_URL, WS_PRODUCTNAME)
are passed directly into the container's environment as runtime arguments. These variables
are then picked up by the mend BitBake class, enabling it to authenticate with the Mend service
and associate the scan with the correct product.

**Automated Scanning**: Once configured, the mend bbclass integrates directly into the
Yocto build process. During the 'Yocto image Type A' stage, it performs the software
composition analysis, scanning the open-source components within the Yocto image
for known vulnerabilities against Mend's extensive database.

**Reporting and Archiving**: The outcomes of the Mend analysis are summarized in mend-report-*.json
and mend cloud portal.

Conclusion: A Secure and Streamlined Development Workflow ✅
------------------------------------------------------------

This Jenkins pipeline exemplifies a robust and contemporary approach to developing embedded Linux systems.
By automating critical processes such as building, testing, and artifact management,
and by strategically integrating Mend SCA for proactive vulnerability detection,
it significantly enhances the security and overall reliability of the produced embedded images.
This comprehensive workflow not only optimizes development time but also provides
crucial insights into the software supply chain, ensuring that the released images
are not only fully functional but also inherently secure.
