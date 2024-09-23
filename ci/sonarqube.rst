Sonarqube
**********

| There are several ways to trigger sonar analysis from jenkins, for complete documentation see:
| https://docs.sonarqube.org/latest/analysis/scan/sonarscanner-for-jenkins/

| 

In any case sonar needs:

-  backend API access parameters
-  specific project parameters (project name and key)

If project with name and key does not exist on backend yet, it will be created automatically after first analysis (if jenkins has rights to do so)

.. _Sonarqube-Gradle:

Gradle
------

Sonar plugin is used for gradle and the parameters set in gradle build file. Analysis is triggered via task *./gradlew sonarqube*

.. _Sonarqube-Jenkins:

Jenkins
-------

Sonar-scanner-cli can be installed within jenkins or within docker when used. Then it is called within project source code root and sonar automatically detects the sources.

The backend access credentials can be set within global sonar qube env and project specific params can be injected within pipeline:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeHeader panelHeader pdl

      **Sonar params injection**

   ::

         def sonarHome = tool 'sonnar_4.6.2.2472' // tool installed in jenkins. In case of docker, it would have to be passed in some way to docker, or can be simply installed in docker image already
         withSonarQubeEnv(credentialsId: 'amarula-sonar') {
               sh '''
                  touch sonar-project.properties
                  echo "sonar.projectKey=voclarion-voclarion4_ui" >> sonar-project.properties
                  echo "sonar.projectName=voclarion-voclarion4_ui" >> sonar-project.properties
                  ${sonarHome}/bin/sonar-scanner
                  '''
         }
