WhiteSourceReport library
*********************************

WhiteSource report library is used to determine the library/packages vulnerabilities by calling the WhiteSource API.

The result generates a pdf file showing the vulnerabilities and also sends the tabled list to the Mattermost verifier-build channel.

.. _com.amarula.ws.WhiteSourceReport-Builder:

Builder
=======

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         def ws = new WhiteSourceReport.Builder()
                      .context(context)
                      .userKey(userKey)
                      .apiKey(apiKey)
                      .build()

-  **Context **- Jenkins context ('this' in pipeline context)
-  **Userkey** - WhiteSource Userkey from Jenkins Credentials
-  **ApiKey** - WhiteSource ApiKey from Jenks Credentials

.. _com.amarula.ws.WhiteSourceReport-Methods:

Methods
=======

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         void generatePdfReport(String config, String projectToken, String project)

This generates the report in pdf format which will be persisted in the build artifacts. 

-  **Config **- This is the config of the environment the project is built in e.g Android, Yarn, or Groovy project. 
-  **ProjectToken** - The WhiteSource token for the particular project
-  **Project** - The Project name, used to name the pdf generated.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         void generateRiskReportAndNotify(String productToken, String peopleToNotify, String project)

This gets the list of all the vulnerabilities of the particular product, and then table and send to the MatterMost verifier-build channel.

-  **ProductToken** - WhiteSource productToken for the specific product.
-  **PeopleToNotify** - A string detailing MatterMost usernames for people to be notified
-  **Project** - The Project name

.. _com.amarula.ws.WhiteSourceReport-ExampleUsage:

Example Usage
=============

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         #!groovy

         import com.amarula.build.Build
         import com.amarula.ws.WhiteSourceReport

         node('android-build') {
             def credentials = 'credentials'
             def build = new Build(this, env, credentials)
             def context = this
             def repoUrl = "${GERRIT_SSH_JENKINSBUILDER_URL}/project"
             def projectToken = 'projectToken'
             def productToken = 'productToken'
             def project = 'SampleProject'
             def ws

             withCredentials([string(credentialsId: 'amarula-whitesource_user_key', variable: 'userKey'), string(credentialsId: 'amarula-whitesource_api_key', variable: 'apiKey')]) {
                 ws = new WhiteSourceReport.Builder()
                      .context(context)
                      .userKey(userKey)
                      .apiKey(apiKey)
                      .build()
             }

             build.setSyncMethod(Build.CHECKOUT)
             stage('report') {
                 build.build(repoUrl, {
                     ws.generatePdfReport(androidwssconfig, projectToken, project) //config passed via pipeline parameters
                     ws.generateRiskReportAndNotify(productToken, "@john, @doe", project)
                 }, ['branch': 'development', 'history': true])

             }
             archiveArtifacts '**/*whitesource.*.log'
             archiveArtifacts '**/*.pdf'
         }

| 

| 

| 
