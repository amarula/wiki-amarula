Jenkins
********

Jenkins is a major part of `Amarula Solutions <http://www.amarulasolutions.com/>`__' continuous integration framework. While detailed information about Jenkins can be found in the `Jenkins Guide </download/attachments/4489295/jenkins-the-definitive-guide.pdf?version=1&modificationDate=1473326864935&api=v2>`__, this document specifically outlines Jenkins's significance within the broader context of the Amarula CI product.

At Amarula, we write `pipeline scripts <https://www.jenkins.io/doc/book/pipeline/>`__ in the Groovy programming language. These scripts, dedicated to specific projects, serve as the instructions guiding the workflow for individual Jenkins jobs, defining how tasks are executed and coordinated throughout a CI process. To achieve efficiency and standardization across projects, we have organized these scripts in what we call the `Jenkins shared libraries </display/CI/Shared+libraries>`__. These libraries encapsulate the common elements crucial for every project, promoting re-usability, maintainability, and consistency in our CI pipelines. The Jenkins shared libraries form the backbone of our continuous integration strategy.

| 

.. container:: toc-macro client-side-toc-macro conf-macro output-block

.. _Jenkins-JenkinsPipelines:

Jenkins Pipelines
=================

Jenkins pipelines serve as **orchestrators**, functioning as central points for interaction and integration within continuous integration and continuous delivery (CI/CD) frameworks. These pipelines act as coordinators, seamlessly bringing together diverse tools, running or triggering them, and efficiently passing outputs to provide a conclusive result.

The utility of pipeline code extends beyond its primary role in software change verification. Consider it as a dynamic orchestrator with unlimited potential, capable of serving as a user interface for administrative tasks when integrated into relevant software.

Key Functions of Jenkins Pipelines:

-  **Automated Verification:** Ensuring systematic validation of code modifications.

-  **Software Releases and Deployment:** Facilitating the streamlined release and deployment of software products.

-  **Vulnerability Detection:** Identifying and addressing potential vulnerabilities within the software.

-  **Administrative Tasks:** Performing various administrative functions, such as generating user workload reports from tracking tools like JIRA.

The adaptability of Jenkins pipelines offers infinite configurations, allowing users to tailor workflows precisely according to project requirements beyond software development.

.. _Jenkins-PipelinesforContinuousIntegration:

Pipelines for Continuous Integration
------------------------------------

The primary objective of Jenkins pipelines in our CI system is to automate the entire software development life cycle. These pipelines seamlessly guide the software from the initial checkout of the source code from version control to the final deployment, ensuring that the end product is prepared and available for the customer.

By using Jenkins pipelines, we establish a systematic and efficient workflow. This allows us to incorporate various steps serving different purposes, including quality verification, integration of software variants, frameworks, tools, and scripts specific to the targeted software product.

.. image:: /images/pipeline_for_ci.png

.. _Jenkins-StructureofJenkins:

Structure of Jenkins
====================

Our structure in Jenkins is based on customers and related projects, this is achieved via the recursive folders similar as on the file system.

.. image:: /images/jenkins_structure.png

.. _Jenkins-Foldersnamingconvention:

Folders naming convention
-------------------------

Our folder hierarchy consists of one or two levels. The top level directory name should be a customer name written as camelCase. Optional second level is project name also written as camelCase. If the second level is present, the build jobs are in them. The job name is also written in camelCase and describes the purpose of the job - e.g. gerritProjectA, buildProdProjectA.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         <Customer1>
          |_ <Job>
          |_ <AnotherJob>
         <Customer2>
          |_ <ProjectA>
              |_ <JobForA>
          |_ <ProjectB>
              |_ <JobForB>

.. _Jenkins-Creatinganewpipelinejob:

Creating a new pipeline job
===========================

To create any new item in the Jenkins structure there is \`new item\` button in the menu

.. image:: /images/creating_pipeline_job.png

There are more types of the items to be created but mostly we use it to create the **folder** and **pipeline**:

**Folder** - can be created recursively to setup proper structure as described earlier

===============================    ===============================
.. image:: /images/folder_1.png    .. image:: /images/folder_2.png
===============================    ===============================

**Pipeline** - the JOB which is defined by various attributes, parameters and the pipeline script itself
 
.. image:: /images/pipeline.png

   
The name of the pipeline is entered and pipeline option selected. It can be fresh new pipeline or copied from already existing pipeline, just the path to existing pipeline needs to be entered. In such case all the existing attributes, parameters and script references will be copied too. This is useful when you create similar pipeline and just few things need to be adopted.

When pipeline is created it can be configured. It consists of particular sections which can be enabled or disabled. New plugins installed in Jenkins can provide additional section or option which will appear in the Jenkins pipeline configuration UI (e.g. `gerrit trigger </display/CI/Gerrit+trigger>`__).

.. _Jenkins-Pipelinescriptcode:

Pipeline script code
====================

| The heart section of pipeline job is the script section. It is a piece of code which is executed and performs the desired job which can be basically anything but usually involves some part of continuous integration.
| There are 2 main ways of passing the script code to job:

-  inject the script code directly to the input field in the UI configuration. We use that only for **quick testing** whether code really works in Jenkins.
-  **reference the script code in version control** (git in our case), and that is how we persist all scripts and track their changes also via `Gerrit Code Review </display/CI/Gerrit+trigger>`__ system.

.. image:: /images/pipeline_script.png

The repository address, path to the file and branch need to be specified together with credentials ID (which is referencing the SSH key securely stored in Jenkins, it will be then used by pipeline to have ssh access to git repository)

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   Shared libraries

   .. container:: confluence-information-macro-body

      The first thing to ask when writing new pipeline is if the functionality is already provided by a `shared library </display/CI/Shared+libraries>`__. It can reduce the amount of code repeated between pipelines and avoids the mistakes done within some areas of Continuous integration like checkout of the code, work with multi-repo, etc ...

| Very helpful tool within Jenkins is **Pipeline syntax** which showcase the various features as the code examples dynamically generated, even the referenced global Jenkins variable names or credentials can be provided to be then included in the syntax example. You can get into pipeline syntax from the link at the end of script section.

.. image:: /images/pipeline_script_2.png

The example on screenshot shows generated syntax of *withCredentials* step which loads the certain credentials from Jenkins secured storage and can be used later in the pipeline block via predefined variable names. There are plenty of options to show and it is good way to get idea about the syntax of pipelines. When installing new Jenkins plugin its syntax can be seen here too.

Another helper is **IntelliJ Idea GDSL**. The Jenkins core methods can be listed in GDSL groovy Jenkins file. The file can be imported into IDE and autocompletion and static error detection can be enabled.

https://gist.github.com/arehmandev/736daba40a3e1ef1fbe939c6674d7da8

`Pipeline examples </display/CI/Pipeline+script+snippets>`__

.. _Jenkins-Triggeringthejob:

Triggering the job
==================

Various types of jobs can have different types of triggering. There are few main types we usually use:

| **Gerrit trigger** is crucial for verification builds. It should happen always when some new code patch set appears in code review system. So the task is to confirm automatically whether changes are OK (anything what can be confirmed automatically - compilation, unit testing, static code analysis).
| It is implemented within additional Jenkins plugin which has to be installed (see plugins section) and appears as new UI section. It has to be setup to interact with existing instance of `Gerrit Code Review </display/CI/Gerrit+Code+Review>`__ system: `Gerrit trigger </display/CI/Gerrit+trigger>`__.

| **Jenkins UI trigger** is available within the same UI of job which was created. There should be \`Build\` or \`Build with parameters\` button available in the menu.
| With parametrized build, user can specify various attributes and conditions for that particular build. Those are then passed to the pipeline script in the list of parameters so that code can execute according to conditions provided  (e.g. checkout from specific branch, decide whether to do release or just snapshot build, create build for specific commit, etc...).

**Cron trigger** is useful to start job regularly, for instance nightly build of some Android OS. Or vulnerability check of the SW to detect whether there recently appeared some SW holes which need to be fixed ASAP.

.. _Jenkins-Pipelineoutputs:

Pipeline outputs
================

The pipeline job status can be tracked within UI and logs can be read, where all the steps of pipeline are printed.

If there are some results/outputs like html report or built SW component, it can be passed to anywhere else outside the Jenkins, but Jenkins also provides the workspace browser where can be stored visibly and user can download then by simple click.

.. image:: /images/pipeline_result.png
   
This screenshot shows the outputs of Android application release job. We have automated deployment to Google Play Store too, but the artifacts can be visible also within job UI and can be downloaded easily when needed. Same as HTML report about the potential issues reported by lint which is integrated within application sources.

.. _Jenkins-Goodpracticesandtips:

Good practices and tips
=======================

#. See the `Structure of Jenkins <#Jenkins-StructureofJenkins>`__ above to properly place and name your job. It is good convention to include the type of pipeline in the job name - if it is a Gerrit verification job start the job name with 'gerrit' or end the name with 'verifier', e.g. "ibacAndroidVerifier", "gerritIbacAndroid".
#. If your job will be computationally demanding (like an OS build), see `Throttling of builds </display/CI/Throttling+of+builds>`__ page.
#. Keep only necessary artifacts and set "Discard old builds" in the job configuration. For Gerrit verification, use 30 days and 30-50 last builds.
#. See `Shared libraries </display/CI/Shared+libraries>`__ page to use some preexisting methods.
#. It is recommended to keep verification and release jobs separated.

.. _Jenkins-Gerrittrigger:

Gerrit trigger
==============

In order to have the Gerrit trigger verification working there are few steps needed on both Jenkins and Gerrit instance - `setup gerrit trigger </display/CI/Gerrit+trigger>`__.

The result of this feature is that every code change pushed in Gerrit review system will verify automatically and label it with result:

.. _Jenkins-TriggerGerritverificationmanually:

Trigger Gerrit verification manually
------------------------------------

The Gerrit patches when properly mapped to Jenkins, can be found in the section *Query and Trigger Gerrit Patches* (from main Dashboard menu). There user can search for particular patch, see its status of verification and potentially retrigger the related job.

.. image:: /images/trigger_gerrit_manually.png

.. _Jenkins-Credentials:

Credentials
===========

Jenkins has safe way to store the sensitive data like private keys, passwords, secret files. It can be stored as credential object within credentials configuration:

.. image:: /images/jenkins_credentials.png

The reference ID string can be then used within pipeline to access those credentials without showing their content to user or exporting anywhere else.

.. _Jenkins-Jenkinscredentialsnamingconventions:

Jenkins credentials naming conventions
--------------------------------------

Jenkins credential should be ordered and well named. All the keys are define in `https://jenkins.amarulasolutions.com/credentials/. <https://jenkins.amarulasolutions.com/credentials/>`__

Keystructure:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         <customer>-<project>_<keyName>
         example amarula-openid_deployService

         <keyName> Should be a readable name that describes the usage. keyName should not include - or _ and it can be in camel case format

.. _Jenkins-JenkinsSharedlibrary:

Jenkins Shared library
======================

Jenkins supports loading of groovy code from custom source. It is useful to extract common parts of code and store them in a Git repository. The Global Pipeline Libraries is an official feature in Jenkins and allows to do such a thing very easily.

Code from the libraries is trusted by default and runs without sandbox.

There is more information available on `Shared libraries </display/CI/Shared+libraries>`__ page.

.. _Jenkins-Globalenvironmentvariables:

Global environment variables
============================

There are certain values which are used across the pipelines and thus can be stored globally under some ID string and then just referenced from the pipeline.

It can be setup within Jenkins configuration, in main dashboard menu → Manage Jenkins → System.

.. image:: /images/global_env_variable.png

.. _Jenkins-UsingDockerinpipelinejobs:

Using Docker in pipeline jobs
=============================

Docker became inseparable part of Jenkins pipelines in Amarula. It provides the desired SW needed by job in convenient way.

We are keeping some separation of docker images according to the pipeline type/purpose. E.g. we have mobile-app docker in Amarula docker registry which has preinstalled the Android SDK for Android applications building, cross platform related build chain (npm, yarn, react native...), Java SDKs, Emulators, etc.

The list of currently managed images can be found on `Amarula dockers </display/DEV/Docker+registry>`__ page.

.. _Jenkins-Plugins:

Plugins
=======

There are plenty of plugins which we already use in Jenkins

.. image:: /images/jenkins_plugin.png

and much more which we did not come to yet. It is possible to install new plugin when considered worth via Jenkins configuration→ Plugins

.. image:: /images/jenkins_plugin_2.png

.. _Jenkins-Pipelinetesting:

Pipeline testing
================

-  You can see the pipeline code and adjust it for a new build using "Replay"
-  You can create small and simple jobs to test triggers, steps, ... . Then you can disable these jobs.
-  You can install groovy on your laptop and test simple parts of the code locally or in some online groovy console.
-  You can create a test branch within the Git repository with new changes and test them in a copy of the main job before merging the changes to the main branch

.. _Jenkins-Theexecutiononnodes:

The execution on nodes
======================

Jenkins executes the jobs on Jenkins server nodes. The server, where Jenkins is running, can also serve as execution node. Jenkins can have several nodes with one or more slots for execution. One execution allocates one slot of a node. If none are available the execution is halted until a free slot is available.

Nodes can be labeled based on their special qualities (special HW connect, specific OS running on them). Jenkins pipeline can be restricted to be executed only on some nodes / labels using the "node" step.

.. image:: /images/jenkins_nodes_execution.png

.. _Jenkins-Requirements:

Requirements
------------

The minimal software needed on the node is:

-  SSH server
-  Java (openjdk 11 / openjdk 17 / openjdk 21 supported)
-  docker

It is also a good idea to create "jenkins" user with its own home directory.

Additionally we recommend to also install Git for debugging and checking the state of source code without the need to use docker image with Git.

