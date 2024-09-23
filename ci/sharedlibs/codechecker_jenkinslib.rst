CodeChecker Jenkins library
****************************

CodeChecker jenkins lib is shared library for Jenkins that wraps the CodeChecker static code analysis tool and helps with basic operations with Gerrit change/topic verification.

source: https://gitea.amarulasolutions.com/i-tools/codechecker_jenkins_lib

source: https://gerrit-review.amarulasolutions.com/admin/repos/i-tools/codechecker_jenkins_lib

related documents: https://codechecker.readthedocs.io/en/latest/

-  name: codechecker_jenkins_lib
-  load implicitly: true
-  allow default version to be overridden: true

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   .. container:: confluence-information-macro-body

      All the changes are currently under review. You need to use "IT-109" branch of the codechecker_jenkins_lib and the same name of branch for the repo_jenkins_lib. These branches contain code that is under review: https://gerrit-review.amarulasolutions.com/q/topic:%22codecheckerlib%22

.. _CodeCheckerJenkinslibrary-Limitations:

Limitations
===========

.. _CodeCheckerJenkinslibrary-Keepthebuild/outputdirectoryoftheproject:

Keep the build/output directory of the project
----------------------------------------------

Due to the nature how the analysis tools work it is necessary to keep the build directory for the analysis part of the process. The JSON buildlog produced is formatted as `clang compilation database <https://clang.llvm.org/docs/JSONCompilationDatabase.html#format>`__. The working directory (build directory) of the commands is a base for possible relative paths.

.. _CodeCheckerJenkinslibrary-Installation:

Installation
============

Add the repository to your Jenkins instance as Shared library:
--------------------------------------------------------------

#. go to "Manage Jenkins" > "Configure System"
#. scroll down to "Global Pipeline Libraries" section
#. use "Add"

   #. Name: codechecker_jenkins_lib
   #. Default version: master
   #. Retrieval method → Modern SCM

      #. Source Code Management → Git
      #. Project Repository: ssh://gitea@gitea.amarulasolutions.com:38745/i-tools/codechecker_jenkins_lib.git

#. "Save"

.. _CodeCheckerJenkinslibrary-AddcredentialsfortheCodeCheckerserver(optional):

Add credentials for the CodeChecker server (optional)
-----------------------------------------------------

#. go to Credentials -> System
#. use Add Credentials

   #. Kind: Username with password
   #. Username: username
   #. Password: password
   #. ID: e.g. jenkins-builder-amarula-codechecker
   #. Description: ...

#. Save

.. _CodeCheckerJenkinslibrary-SetconfigurationvariablesforCodeCheckerserver(optional):

Set configuration variables for CodeChecker server (optional)
-------------------------------------------------------------

#. go to Manage Jenkins > Configure System
#. scroll down to Global properties section
#. use the Environment variables option
#. define these variables (values are examples): 

   #. CODECHECKER_URL : "https://codechecker.amarulasolutions.com"
   #. CODECHECKER_PORT : "443"

#. Save

.. _CodeCheckerJenkinslibrary-AnalysisprocessusingCodeChecker:

Analysis process using CodeChecker
==================================

In order to use the library correctly it is necessary to understand how the CodeChecker tool operates. You can find more information at the `official documentation page <https://codechecker.readthedocs.io/en/latest/>`__.

CodeChecker runs the given build command and monitors the build commands that were used. This operation is "log". It produces JSON compilation database file. If the build recompiles only some files during the build, only those files will be logged and analyzed in the next step.

The output of the "log" operation can be processed using "analyze". It runs static analysis tools on the files from the JSON compilation database and passes on the compilation flags used.

CodeChecker can process the analysis created from the previous step to create a report for Gerrit or human-readable HTML pages. This operation is called "parse".

The "log" and "analyze" operations can be done at once using "check". All these operations are wrapped in this library with functions of corresponding names.

.. _CodeCheckerJenkinslibrary-Supportedfunctionalities:

Supported functionalities
=========================

-  Supported languages: C/C++
-  Log build using CodeChecker log ...
-  Analyze log using CodeChecker analyze ...
-  Analyze build using CodeChecker check ...
-  Create HTML/Gerrit report using CodeChecker parse ...
-  Create differential reports using CodeChecker cmd diff ...
-  Send Gerrit report to Gerrit where it appears as comments for the analyzed change
-  Upload report to CodeChecker server
-  Perform incremental build and use CodeChecker log ... to log each increment
-  Perform analysis from the logs using CodeChecker analyze ... for each increment
-  Perform incremental build and use CodeChecker check ... to build and analyze each increment

.. _CodeCheckerJenkinslibrary-IntegrationintoCIJenkinslibrary:

Integration into CI Jenkins library
===================================

The Build and Verification classes from the `CI Jenkins library <./sharedlibs/ci_jenkinslib/index.html>`__ have become the standard way to build/verify projects. Therefore to make it even easier to use this library in our pipelines there are some convenient methods. The details can be found in the CI Jenkins library documentation: `com.amarula.build.Verification <./sharedlibs/ci_jenkinslib/verification.html>`__, `com.amarula.build.Build <./sharedlibs/ci_jenkinslib/jenkins_build_lib.html>`__

.. _CodeCheckerJenkinslibrary-Librarydescription:

Library description
===================

.. _CodeCheckerJenkinslibrary-Steps:

Steps
-----

.. _CodeCheckerJenkinslibrary-codechecker.log:

codechecker.log
~~~~~~~~~~~~~~~

Runs the given build command and records the executed compilation steps. These steps are written to the output file in a JSON format.

.. _CodeCheckerJenkinslibrary-codechecker.logGerritChanges:

codechecker.logGerritChanges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run build and log it for each of the given Gerrit changes.

.. _CodeCheckerJenkinslibrary-codechecker.analyze:

codechecker.analyze
~~~~~~~~~~~~~~~~~~~

Use the previously created JSON Compilation Database to perform an analysis on the project, outputting analysis results in a machine-readable format.

.. _CodeCheckerJenkinslibrary-codechecker.analyzeGerritChanges:

codechecker.analyzeGerritChanges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the previously created collection of JSON Compilation Databases to perform an analysis on the project. The analysis results of each change will be merged and reported back to Gerrit.

.. _CodeCheckerJenkinslibrary-codechecker.check:

codechecker.check
~~~~~~~~~~~~~~~~~

Run analysis for a project by building it. Only the files involved in the build are checked. Clean up the build directory to analyze all files. Re-check after applying a patch to check only changed files by the patch.

.. _CodeCheckerJenkinslibrary-codechecker.checkGerritChanges:

codechecker.checkGerritChanges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run analysis of Gerrit changes by building and analyzing each change. The results are reported back to Gerrit.

.. _CodeCheckerJenkinslibrary-codechecker.diffReport:

codechecker.diffReport
~~~~~~~~~~~~~~~~~~~~~~

Create report of new issues comparing two given CodeCheckerAnalysis.

.. _CodeCheckerJenkinslibrary-Mainclasses:

Main classes
------------

.. _CodeCheckerJenkinslibrary-com.amarula.codechecker.analysis.CodeCheckerAnalysis:

com.amarula.codechecker.analysis.CodeCheckerAnalysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**createReport** - Create report from this analysis.

**uploadAnalysis** - Upload this analysis to CodeChecker server specified in env as CODECHECKER_URL and CODECHECKER_PORT.

.. _CodeCheckerJenkinslibrary-com.amarula.codechecker.server.CodeCheckerServer:

com.amarula.codechecker.server.CodeCheckerServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**productExists** - Checks if product with given name exists on the server.

**createProduct** - Creates new product with given endpoint name.

.. _CodeCheckerJenkinslibrary-Typicaluse:

Typical use
===========

The example below shows typical use-case of code analysis using this library. The code assumes the project is synced and it is running inside a properly configured Docker container.

::

         library 'codechecker_jenkins_lib'
         import com.amarula.codechecker.analysis.*

         CodeCheckerAnalysis analysis = codechecker.check(Language.C_CPP, [Analyzer.clangtidy], 'make')
         def path = analysis.createReport(CodeCheckerReportFormat.HTML)

         sh "tar -cvf codechecker_html.tar ${path}"
         archiveArtifacts 'codechecker_html.tar'

| 

Following example shows a code that runs analysis and uploads the results to CodeChecker server.

::

         library 'codechecker_jenkins_lib'
         import com.amarula.codechecker.*

         def gitRevision = sh returnStdout: true, script: 'git rev-parse HEAD'

         CodeCheckerAnalysis analysis = codechecker.check(Language.C_CPP, [Analyzer.clangtidy], 'make')
         analysis.uploadAnalysis('myProject', "master_rev_${gitRevision.trim()}")

| 

The next example uses diffReport to get only new issues caused by a new Gerrit Change. The code assumes proper credentials are used to access the Git repository and Gerrit REST API. It also assumes it is running inside a properly configured Docker container.

::

         library 'codechecker_jenkins_lib'
         import com.amarula.codechecker.analysis.*
         import com.amarula.codechecker.report.*

         library 'repo_jenkins_lib'
         import com.amarula.git.Git
         import com.amarula.gerrit.GerritChange

         Git repo = new Git(this, env, url, [history: true])

         repo.sync('master')
         CodeCheckerAnalysis baseAnalysis = codechecker.check(Language.C_CPP, [], 'make')

         GerritChange change = repo.checkoutChange('refs/changes/34/1234/5')
         CodeCheckerAnalysis changeAnalysis = codechecker.check(Language.C_CPP, [], 'make')

         String report = codechecker.diffReport(baseAnalysis, changeAnalysis, CodeCheckerReportFormat.GERRIT, repo, change)
         change.setReviewFromFile(report)

| 

The previous example could be simplified using checkGerritChanges as shown below. The codechecker.checkGerritChanges step works with a List of GerritChanges. It finds out the target branch of the changes, checks out the branch and runs a base analysis. Then  applies one by one each change and runs a new analysis that is compared to the previous one. The results are reported to each Gerrit change.

::

         library 'codechecker_jenkins_lib'
         import com.amarula.codechecker.*
         import com.amarula.codechecker.analysis.*

         library 'repo_jenkins_lib'
         import com.amarula.git.Git
         import com.amarula.gerrit.GerritChange

         Git repo = new Git(this, env, url, [history: true])
         GerritChange change = repo.checkoutChange('refs/changes/34/1234/5')

         codechecker.checkGerritChanges(Language.C_CPP, [], 'make', repo, [change])

| 

The next example shows how to analyze Gerrit changes when building several variants. The results are reported to Gerrit.

::

         library 'repo_jenkins_lib'
         import com.amarula.git.Git
         import com.amarula.gerrit.GerritChange

         Git repo = new Git(this, env, url, [history: true])

         def result = codechecker.logGerritChanges('make X=0', repo, repo.checkoutTopic(env.GERRIT_TOPIC))
         sh 'make clean'
         codechecker.logGerritChanges('make X=1', repo, result)
         sh 'make clean'
         codechecker.logGerritChanges('make X=2', repo, result)

         codechecker.analyzeGerritChanges(Language.C_CPP, [], result, repo)
