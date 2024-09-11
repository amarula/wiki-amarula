Jenkins pipeline autocompletion in Intellij Idea IDE
*****************************************************

`IT-117 <https://jira.amarulasolutions.com/browse/IT-117>`__\ - Getting issue details... STATUS Writing a Jenkins pipeline is not very easy without code autocompletion.

Autocompletion is very useful when writing complex pipelines, we don’t need to google each time for even smaller syntaxes.

| 

Intellij by default doesn’t come with Jenkins autocompletion. In order to make intellij ready for jenkins syntax autocompletion, we need to follow certain steps.  

Even after making Intellij ready for jenkins pipeline development, the ide don’t recognise all pipeline syntaxes. 

| 

This guide will help in setting up autocompletion and the methods which are available.

.. _JenkinspipelineautocompletioninIntellijIdeaIDE-Prerequisite:

Prerequisite
------------

#. Intellij Idea IDE
#. Jenkins gdsl file

.. _JenkinspipelineautocompletioninIntellijIdeaIDE-Whatisjenkinsgdsl?:

What is jenkins gdsl?
~~~~~~~~~~~~~~~~~~~~~

Jenkins provides a GDSL file that describes the language constructs available for a given Jenkins instance.

It also contains syntax of the various plugins installed in the instance.

| 

**How to get a Jenkins gdsl file?**

You can get the gdsl file by accessing the url of jenkins instance. 

Example:http://(yourjenkinsurl)/job/(yourpipelinejob)/pipeline-syntax/gdsl

.. image:: /images/jenkins_gdsl.png

You can copy the content from this url in a file and save it as  'jenkinsSyntax.gdsl'

.. _JenkinspipelineautocompletioninIntellijIdeaIDE-Setupintellijforautocompletion:

Setup intellij for autocompletion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make intellij ready for autocompletion. Follow the steps:

| 

#. First create a project or open a project
#. Now copy and paste the \`jenkinsSyntax.gdsl\` file that you created in your main directory. E.g if you have created a package in your pipeline project.Paste the file in your main package, let's say you have \`com.amarula.pipeline`. Just paste the file in this package.

Intellij is ready for autocompletion. Now you can start writing your pipeline and intellij will start showing autocompletion for jenkins pipeline syntax.

| 

**How to add support for autocompletion for jenkins shared libraries?**

| 

To add support for showing autocomplete for amarula jenkins shared libraries, you will need to download the jar file of shared library and repo jenkins library.

After downloading the jar files, follow these steps

#. Create or open a pipeline project
#. Copy and paste the jar file in the libs folder of your pipeline.
#. Now add the jar file as a library to your pipeline. 

| 

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   .. container:: confluence-information-macro-body

      If you don’t know how to add the jar as a library. 

      #. Right click on the jar file, it will open a context menu with many options.
      #. Scroll down to the bottom of the context menu, you will see an option named \`Add as library`.
      #. Click on that and it will be added to your project.       

      .. image:: /images/intellij_import_jar.png
| 

Now your project is ready for jenkins shared library autocompletion.

Same way you add other 3rd party libraries to your pipeline.

Even after adding gdsl, intellij doesn't show autocomplete for all methods. These are two cases when autocomplete didn’t work.

#. Jenkins environment variable. Jenkins doesn't expose the environment variable, so autocomplete will not work in this case.
#. Some of the plugin methods are also not exposed. Example \`withCredentials\` accepts \`usernamePassword\` as param. Intellij doesn’t show autocomplete nor does it highlight the text.

| 

| 

| 

| 

| 

| 

| 

| 

| 

| 

| 

| 
