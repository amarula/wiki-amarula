Fixing Flattened CodeNarc XML Report Paths in Jenkins Shared Libraries
======================================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


If you are developing a Jenkins Shared Library and using Gradle to run CodeNarc, you might have noticed a frustrating bug: your generated XML reports completely lose their package hierarchy. Instead of files being cleanly mapped to ``com/amarula/build/Build.groovy``, they are dumped into an empty package path (``<Package path=''>``) with just the filename.

This causes massive headaches when integrating with code quality tools like SonarQube, which rely on strict relative file paths to map violations to your source code.

Here is exactly why this happens and the silver-bullet workaround to fix it.

The Root Cause: The Jenkins JPI Plugin
--------------------------------------

The culprit is a deep-seated clash between Gradle's native CodeNarc task and the ``org.jenkins-ci.jpi`` plugin.

To support Continuation Passing Style (CPS) compilation for Jenkins pipelines, the JPI plugin fundamentally hijacks your ``sourceSets.main`` under the hood. It secretly slices your ``src/`` directory into a fragmented list of every single sub-package folder.

When Gradle's standard ``codenarc`` plugin inherits this modified source set, it receives a corrupted, flattened list. Because Gradle's internal optimizer sees a list of leaf directories rather than a cohesive tree, it treats every sub-folder as a base directory. As a result, the relative package paths are completely erased from the final XML report.

Standard overrides like ``source = fileTree('src')`` do not work because Gradle's task action continues to flatten the inputs right before the scan.

The Solution: Bypassing Gradle for Ant
--------------------------------------

To permanently fix this, we must completely bypass Gradle's native CodeNarc task action and invoke the underlying **Ant CodeNarc engine** directly. This allows us to feed the scanner an impenetrable base directory, preventing the JPI plugin from slicing it up.

Step 1: Isolate the Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When we bypass Gradle's native task, we lose access to its internal logging bridge. We need to create a dedicated configuration to supply CodeNarc and SLF4J directly to the Ant runner so it doesn't crash silently.

Create a new file called ``gradle/codenarc-ant.gradle`` and add the following:

.. code-block:: groovy

    configurations {
        codenarcRunner
    }

    dependencies {
        codenarcRunner 'org.codenarc:CodeNarc:3.7.0'
        codenarcRunner 'org.codehaus.groovy:groovy-all:3.0.23'
        codenarcRunner 'org.slf4j:slf4j-api:1.7.36'
        codenarcRunner 'org.slf4j:slf4j-simple:1.7.36'
    }

Step 2: Dynamically Override the Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the same file, we can clear Gradle's default actions for both the ``main`` and ``test`` tasks, replacing them with a direct Ant invocation. Using a map, we can keep the code perfectly DRY (Don't Repeat Yourself).

.. code-block:: groovy

    def targetTasks = [
        'codenarcMain': [ sourceDir: 'src',       reportFile: 'main.xml' ],
        'codenarcTest': [ sourceDir: 'test/unit', reportFile: 'test.xml' ]
    ]

    targetTasks.each { taskName, config ->
        tasks.named(taskName) {
            // 1. Wipe out the broken Gradle default execution completely
            actions.clear()

            doLast {
                def reportDir = file("$buildDir/reports/codenarc")
                reportDir.mkdirs()
                def reportOutput = file("${reportDir}/${config.reportFile}")
                def antTaskDefName = "customCodeNarc_${taskName}"

                println "==> Starting custom CodeNarc Ant Task for ${taskName}..."

                // 2. Define the Ant task using our isolated runner classpath
                ant.taskdef(
                    name: antTaskDefName,
                    classname: 'org.codenarc.ant.CodeNarcTask',
                    classpath: configurations.codenarcRunner.asPath
                )

                // 3. Invoke the Ant task dynamically
                ant."${antTaskDefName}"(
                    ruleSetFiles: "file:${file('codenarc/rules.groovy').absolutePath}",
                    maxPriority1Violations: 99999,
                    maxPriority2Violations: 99999,
                    maxPriority3Violations: 99999
                ) {
                    report(type: 'xml') { option(name: 'outputFile', value: reportOutput.absolutePath) }

                    // This strictly locks the base directory, preventing ANY flattening
                    fileset(dir: config.sourceDir) { include(name: '**/*.groovy') }
                }

                println "==> ${taskName} Finished! Report: ${reportOutput}"
            }
        }
    }

Step 3: Apply the Script
~~~~~~~~~~~~~~~~~~~~~~~~

Finally, go to your root ``build.gradle`` file. Ensure the standard CodeNarc plugin is generating tasks for both source sets, and apply the new Ant override script at the bottom.

.. code-block:: groovy

    codenarc {
        configFile = file('codenarc/rules.groovy')
        // Ensure both tasks exist in the build graph
        sourceSets = [sourceSets.main, sourceSets.test]
        ignoreFailures = true
        reportFormat = 'xml'
    }

    // Apply the custom Ant execution overrides
    apply from: 'gradle/codenarc-ant.gradle'

Conclusion
----------

By intercepting the task execution and forcing Ant to anchor directly to ``src`` and ``test/unit``, you successfully strip away the Jenkins JPI plugin's broken pathing logic.

Running ``./gradlew check`` will now yield perfectly structured XML reports with complete ``com/yourcompany/...`` package hierarchies, making code quality analysis seamless once again.
