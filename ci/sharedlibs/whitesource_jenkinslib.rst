MendReport library
*********************************

Mend report library is used to determine the library/packages vulnerabilities by calling the Mend API.

The result generates a pdf file showing the vulnerabilities and also sends the tabled list to the Mattermost verifier-build channel.

.. _com.amarula.ws.MendReport-Builder:

Builder
=======

::

         def ws = new MendReport.Builder()
                      .context(context)
                      .userKey(userKey)
                      .apiKey(apiKey)
                      .build()

-  **Context**- Jenkins context ('this' in pipeline context)
-  **Userkey** - Mend Userkey from Jenkins Credentials
-  **ApiKey** - Mend ApiKey from Jenks Credentials

.. _com.amarula.ws.MendReport-Methods:

Methods
=======
::

         void performProjectAnalysis(String config, String projectToken, String project) {

First step which is triggering the analysis of the project on server side and waits for the result.
If there is no exception based on result we can continue with generating reports.

-  **Config**- This is the config of the environment the project is built in e.g Android, Yarn, or Groovy project.
-  **ProjectToken** - The Mend token for the particular project
-  **Project** - The Project name, used to name the pdf generated.

::

         void generatePdfReport(String projectToken, String project)

This generates the report in pdf format which will be persisted in the build artifacts. 

-  **ProjectToken** - The Mend token for the particular project
-  **Project** - The Project name, used to name the pdf generated.

::

         void generateRiskReportAndNotify(String productToken, String peopleToNotify, String project)

This gets the list of all the vulnerabilities of the particular product, and then table and send to the MatterMost verifier-build channel.

-  **ProductToken** - Mend productToken for the specific product.
-  **PeopleToNotify** - A string detailing MatterMost usernames for people to be notified
-  **Project** - The Project name

.. _com.amarula.ws.MendReport-ExampleUsage:

Example Usage
=============

::

         #!groovy

         import com.amarula.build.Build
         import com.amarula.mend.MendSourceReport
         import com.amarula.ui.Ui

         node('android-build') {
             def build = new Build(this, env, '9af8a985-9516-467e-b9cb-0174692fe8c0')
             def context = this
             def repoUrl = "${GERRIT_SSH_JENKINSBUILDER_URL}/amarula-app/travel-smart"
             def projectToken = '*****************************'
             def productToken = '*****************************'
             def project = 'travelSmart'
             def dockerImage = 'mobile-app:1.12'
             def ws

             def wssconfig = '''
                 projectName=travelSmart
                 projectVersion=
                 ...
             '''.stripIndent()

             def ui = new Ui.Builder(this)
                            .addStringParameter('peopleToNotify', '@peterj, @ronnie.otieno', 'Write particular people to be notified via mattermost - has to use same reference approach, e.g.: @milo, @peterj')
                            .addMultilineStringParameter('androidwssconfig', wssconfig, 'A whitesource android configuration.')
                            .build()

             withCredentials([string(credentialsId: 'amarula-whitesource_user_key', variable: 'userKey'), string(credentialsId: 'amarula-whitesource_api_key', variable: 'apiKey')]) {
                 ws = new MendSourceReport.Builder()
                                          .context(context)
                                          .userKey(userKey)
                                          .apiKey(apiKey)
                                          .build()
             }

             build.setSyncMethod(Build.CHECKOUT)
             build.build(repoUrl, {
                 stage('mend analysis') {
                     withEnv(["JAVA_HOME=/home/jenkins/.sdkman/candidates/java/17.0.6-amzn"]) {
                         ws.performProjectAnalysis(androidwssconfig, projectToken, project)
                     }
                 }
                 stage('pdf risk report') {
                     withEnv(["JAVA_HOME=/home/jenkins/.sdkman/candidates/java/17.0.6-amzn"]) {
                         ws.generatePdfReport(projectToken, project)
                     }
                 }
                 stage('security notification') {
                     ws.generateRiskReportAndNotify(projectToken, peopleToNotify, project)
                 }
             }, ['branch': 'master', 'history': true, dockerImage: dockerImage])

             archiveArtifacts '**/*whitesource.*.log'
             archiveArtifacts '**/*.pdf'
         }

| 

| 

| 
