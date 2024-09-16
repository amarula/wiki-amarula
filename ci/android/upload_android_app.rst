Uploading to Google Play
*************************

`Google Play Android Publisher Plugin <https://wiki.jenkins.io/display/JENKINS/Google+Play+Android+Publisher+Plugin>`__ can be used to automatically upload new releases of android applications to Google Play store.

Plugin web site describes in detail how to let Jenkins accessing the API of google play. Basically there are 3 main requirements:

#. Service account in Google API Console with the private/public keys generated
#. Google Play account connected to the service account from step 1 and having the proper rights to publish the applications
#. Jenkins having Service account credentials (private key) 

.. _UploadingtoGooglePlay-Usinginpipeline:

Using in pipeline
=================

Following snippet is example from travel smart application:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         androidApkUpload apkFilesPattern: '**/*signed.apk',
                 googleCredentialsId: 'Google Play Android Developer',
                 recentChangeList: [[language: 'en-GB', text: 'Please test the changes from Jenkins build.']],
                 trackName: 'internal'

**androidApkUpload** - plugin name to be used as command

**apkFilesPattern** - path to signed apk

**googleCredentialsId** - id of the credential for the google service account

**recentChangeList** - changes description for the version to be published

**trackName** - type of the release track, can be one of internal/alfa/beta/production

.. container:: confluence-information-macro confluence-information-macro-information conf-macro output-block

   Hint

   .. container:: confluence-information-macro-body

      In closed testing there can be more tracks defined within google play. This can be useful to e.g. distinguish the production and staging environment, then just the name of the track is provided within pipeline.

.. container:: confluence-information-macro confluence-information-macro-warning conf-macro output-block

   Signing android application bundle

   .. container:: confluence-information-macro-body

      Google is deprecating usage of standalone APK for uploading the application to google play. Instead the `android application bundle <https://developer.android.com/guide/app-bundle>`__ will be mandatory. See `Signing android application releases <./android_app_signing.html>`__ for the way how to sign .aab in jenkins pipeline.
