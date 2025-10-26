Warning-ng Jenkins plugin codechecker integration
==============================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

.. figure:: /images/code-checker-warnings.png
   :align: center

|
|

Amarula Solutions

=====================================================================
Streamlining Static Analysis with CodeChecker and Jenkins Warnings NG
=====================================================================

In the world of software development, ensuring code quality and security is paramount.
Static analysis tools play a crucial role in identifying potential issues early in
the development lifecycle, saving time and resources. CodeChecker, a powerful
static analysis tool, combined with the Jenkins Warnings NG plugin, provides a
robust solution for automating and visualizing code analysis results within a
continuous integration environment. This article explores the benefits of
integrating these two tools and how they can improve your development workflow.

What is CodeChecker?
--------------------

CodeChecker is an open-source static analysis tool suite capable of detecting a
wide range of code defects, including:

* **Bug Detection:** Identifies potential bugs such as memory leaks, null
  pointer dereferences, and division by zero.
* **Style Violations:** Enforces coding standards and best practices, promoting
  code consistency and readability.
* **Security Vulnerabilities:** Detects potential security flaws like buffer
  overflows and format string vulnerabilities.
* **Concurrency Issues:** Identifies potential problems related to
  multithreading and concurrency.

CodeChecker supports various programming languages, including C, C++, and
Objective-C, making it a versatile tool for diverse projects. It offers a
command-line interface and can be easily integrated into build systems.

What is the Jenkins Warnings NG Plugin?
---------------------------------------

The Jenkins Warnings NG plugin is a powerful Jenkins plugin that collects and
displays compiler warnings, static analysis issues, and other build warnings.
It provides a centralized view of all warnings across different build tools and
analysis tools, making it easy to track and manage them. Key features include:

* **Unified Warning Display:** Aggregates warnings from various sources into a
  single, manageable view.
* **Trend Analysis:** Tracks the evolution of warnings over time, allowing
  developers to identify and address recurring issues.
* **Filtering and Sorting:** Provides flexible filtering and sorting options to
  prioritize and focus on specific types of warnings.
* **Integration with Build Status:** Allows warnings to influence the build
  status, failing builds with critical warnings.
* **Detailed Reporting:** Generates comprehensive reports on detected warnings,
  including context information and links to the source code.

The Power of Integration: CodeChecker and Jenkins Warnings NG
-------------------------------------------------------------

Integrating CodeChecker with the Jenkins Warnings NG plugin brings several
advantages:

* **Automated Analysis:** CodeChecker can be integrated into your Jenkins build
  pipeline, automatically running static analysis on every build.
* **Centralized Visualization:** The Warnings NG plugin displays CodeChecker's
  findings within the Jenkins dashboard, providing a clear overview of code
  quality.
* **Early Issue Detection:** By running static analysis on every commit,
  potential issues are identified early, preventing them from propagating into
  the codebase.
* **Improved Code Quality:** The combined solution encourages developers to
  address warnings and improve code quality, resulting in more robust and
  maintainable software.
* **Simplified Workflow:** The integration streamlines the process of code
  analysis and warning management, making it easier for development teams to
  maintain high code quality standards.

Example Jenkins Pipeline Snippet using Amarula Solutions Library:
-----------------------------------------------------------------

.. code-block:: groovy

   #!groovy

   import com.amarula.build.Build
   import com.amarula.changelog.Changelog
   import com.amarula.codechecker.analysis.Analyzer
   import com.amarula.codechecker.analysis.Language
   import com.amarula.codechecker.report.CodeCheckerReportFormat
   import com.amarula.ui.Ui

   node {
       def dockerImage = 'bb2-builder:1.0.5'
       def dockerOptions = ' --privileged -v /proc:/proc -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /var/run/dbus:/var/run/dbus'
       def manifestUrl = "${GITEA_SSH_URL}/beepbeep/bb2-firmware.git"
       def credentials = ['c4f9fa8c-45d7-459e-a645-203f1245d914', '9af8a985-9516-467e-b9cb-0174692fe8c0']

       def ui = new Ui.Builder(this)
           .addStringParameter("BRANCH", "master", "Branch or tag to be built")
           .addStringParameter("GERRIT_TOPIC", '', "Gerrit Topic to cherry-pick.")
           .addStringParameter("Mailers", "", "Address to send emails")
           .addBooleanParameter("Email", false, "Send email with changelog and artifacts")
           .addBooleanParameter("Security", true, "Enable build with security enabled")
           .build()

       env.CI_JENKINS_LIB_VERIFICATION_OVERRIDE = 1
       ver = new Build(this, env, credentials)
       ver.setSyncMethod(Build.CHERRYPICK)

       def ref = params.BRANCH
       def status = ""
       def skipfile = "${env.WORKSPACE}/skipfile.txt"
       def textfile = "-*/build/*\n" + "-*src/LowLevelDrivers/*"

       writeFile file: skipfile, text: textfile

       currentBuild.description = "<br>Version<br>"

       final def buildCode = [
           'Build ARM using gcc' : {
               status = sh(returnStatus: true, script: 'git describe --tags')
               def fromRef
               if (status != 0) {
                   status = ""
                   fromRef = """git rev-list --max-parents=0 HEAD"""
               } else {
                   status = "_" + sh(returnStdout: true, script: 'git describe --tags').trim();
                   fromRef = """git describe --abbrev=0 --always --tags HEAD^ --match='v[0-9].[0-9].[0-9]'"""
               }
               def options = [from: fromRef, to: "HEAD"]
               def security

               if (Security.toBoolean()) {
                  security = "USE_SECURITY=1"
               }

               sh """
                  make clean
               """
               ver.logBuild("make USE_GCC=1 USE_STM32G071=ON POSTFIX_NAME=${status} ${security} all")

               if (Security.toBoolean()) {
                   sh """
                      export PATH="${PATH}":/opt/STM32/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin
                      STM32_Programmer_CLI -sl bins/bb2_controller*.bin 0x8000000 0x801E000 0x400
                      STM32_Programmer_CLI -sl bins/bb2_deployer*.bin 0x8000000 0x801E000 0x400
                   """
               }
               def changelogString = new Changelog().generate(this, options)
               currentBuild.description += changelogString
           },
           'Static code analysis' : {
               def tool = ver.analyzeBuild(Language.C_CPP, [Analyzer.clangtidy, Analyzer.clangsa], [ignore: skipfile])
               def outputFile = tool.createReport(CodeCheckerReportFormat.TXT, ".")
               recordIssues sourceCodeRetention: 'MODIFIED', tool: codeChecker(pattern: outputFile)
           }
       ]

       def options = ['branch': ref, history:true, 'dockerImage': dockerImage, 'dockerOptions': dockerOptions,
               'gerritProject': 'beepbeep/bb2-firmware']
       ver.build(manifestUrl, buildCode, options)

       notification.monitoredStage('Deploy') {
           def filename = 'release' + status + '.tgz'
           sh(returnStdout: true, script: 'tar -C bb2-firmware -czf ' + filename + ' bins/');
           archiveArtifacts filename

           if (Email.toBoolean()) {
               def sub = 'New BBD release' + status + ' PDK'
               emailext(attachmentsPattern: filename, mimeType: 'text/html', body: currentBuild.description,
                        subject: sub, to: Mailers)
           }
           notification.notifySuccess()
       }
   }


.. figure:: /images/pipeline-codechecker.png
   :align: center

Conclusion:
-----------

The combination of CodeChecker and the Jenkins Warnings NG plugin offers a
powerful and efficient solution for automating static analysis and managing
code quality within a continuous integration environment. By integrating these
tools, development teams can identify and address potential issues early,
improve code quality, and deliver more robust and secure software. This approach
promotes a culture of code quality and helps to streamline the development
workflow. Remember to consult the official documentation for both CodeChecker
and the Jenkins Warnings NG plugin for the most up-to-date information and
detailed configuration instructions.
