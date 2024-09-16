Android app Jenkins Pipeline job configuration
##############################################

A complete example in how to configure the pipeline is given in `Android Jenkins Continue integration <https://jenkins.amarulasolutions.com/job/application_build/job/barcode-scanner/configure>`__. What is needed is configure the project in order to have verified label as shown in the picture

.. image:: /images/android_application_pipeline_creation.png

Pipeline Script
~~~~~~~~~~~~~~~

Node master is setup with gradle installation and android sdk in order to build android application. We are using credential of jenkins-builder-android in order to checkout code from gerrit for aevi-albert projects and amarula\* groups

::

         node('android-build') {
             def gerritTrigger = true
             
             stage('checkout') {
                 sshagent(['9af8a985-9516-467e-b9cb-0174692fe8c0']) {
                     dir("barcode-scanner-app") {
                         deleteDir()
                     }
                     sh 'git clone ssh://jenkins-builder-amarula@gerrit-review.amarulasolutions.com:29418/aevi-albert/barcode-scanner-app -b master'
                 }
                 // Fetch the changeset to a local branch using the build parameters provided to the
                 // build by the Gerrit plugin...
                 try {
                     sshagent(credentials: ['9af8a985-9516-467e-b9cb-0174692fe8c0'], ignoreMissing: true) {
                         def changeBranch = "change-${GERRIT_CHANGE_NUMBER}-${GERRIT_PATCHSET_NUMBER}"
                         withEnv(["changeBranch=${changeBranch}"]) {
                             dir("barcode-scanner-app") {
                                 sh 'git fetch origin ${GERRIT_REFSPEC}:${changeBranch}'
                                 sh 'git checkout ${changeBranch}'
                             }
                         }
                     }
                 } catch (err) {
                     println("Normal build")
                     gerritTrigger = false
                 }
             }
             
             stage('build') {
                 try {
                     echo "stage build"
                     dir("barcode-scanner-app") {
                         echo "invoke gradle"
                         sh './gradlew clean'
                         sh './gradlew build'
                     }
                     
                     if (gerritTrigger) {
                         setGerritReview()
                     } else {
                         archiveArtifacts artifacts: 'barcode-scanner-app/build/outputs/apk/*.apk', fingerprint: true
                     }
                 } catch (err) {
                     if (gerritTrigger) {
                         setGerritReview()
                     }
                     throw err
                 }
             }
         }

Manage of exception is suboptimal right now. This script let doing manual build and build by trigger. One important note:

::

   If you have some shell script that need to read some environment from the groovy this should be exported using withEnv(["changeBranch=${changeBranch}"])


Using `Shared library <../sharedlibs/shared_lib.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

         import com.amarula.Verification

         node('android-build') {
             def ver = new Verification(steps, env)
             
             ver.verifyBuild('9af8a985-9516-467e-b9cb-0174692fe8c0',
                     'ssh://jenkins-builder-amarula@gerrit-review.amarulasolutions.com:29418/aevi-albert/barcode-scanner-app',
                     {
                         sh './gradlew clean build'
                     }
             )

             stage('Deploy') {
                 if (!ver.isTriggeredByGerrit()) {
                     archiveArtifacts artifacts: 'barcode-scanner-app/build/outputs/apk/*.apk', fingerprint: true
                 }
             }
         }

