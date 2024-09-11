Signing android application releases
*************************************

`Android signing plugin <https://jenkins.io/doc/pipeline/steps/android-signing/>`__ can be used to sign android application releases in pipeline. Certificate has to be added in Jenkins credentials for this purpose.

The precondition is to have the proper keystore (which key should be used to sign app) within `jenkins credentials. </display/CI/Import+credential+certificate>`__

.. _Signingandroidapplicationreleases-Usingcertificateinpipeline:

Using certificate in pipeline
=============================

Following snippet is example from alcosystems ibac project:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeHeader panelHeader pdl

      **SigningStep**

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         step([$class: 'SignApksBuilder', apksToSign: "**/*-unsigned*.apk", keyAlias: 'alcosystems', keyStoreId: 'alcosystems-ibac_androidProdKeystore', zipalignPath: "${ANDROID_HOME}/build-tools/26.0.2/zipalign"])

**class** - plugin class for signing, do not change

**apksToSign** - path to unsigned apk

**keyAlias** - alias of the key within keystore used for the signing

**keyStoreId** - id of the credential in Jenkins

**zipalignPath** - path to zipalign tool (having ANDROID_HOME set to android SDK is not enough)

Signed artifact is archived automatically by default. It can be changed by plugin properties.

See `Android signing plugin <https://jenkins.io/doc/pipeline/steps/android-signing/>`__ for further options.

.. _Signingandroidapplicationreleases-Signingandroidapplicationbundle(.aabformat):

Signing android application bundle (.aab format)
------------------------------------------------

Google is deprecating usage of standalone apk for uploading the application to google play. Instead the `android application bundle <https://developer.android.com/guide/app-bundle>`__ will be mandatory.

Till jenkins signApksBuilder plugin does not support signing of such format, there is still possibility to use jarsigner directly, just the keystore has to be injected into pipeline with all its credentials:

.. container:: code panel pdl conf-macro output-block

   .. container:: codeHeader panelHeader pdl

      **Signing android application bundle**

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         withCredentials([certificate(aliasVariable: 'alias', credentialsId: 'dokoki-bsg_androidMobileReleaseKeystore', keystoreVariable: 'keystore', passwordVariable: 'password')]) {
             sh "zip -d ${buildPath} META-INF/* *"
             sh "jarsigner -verbose -storetype pkcs12 -sigalg SHA256withRSA -digestalg SHA-256 -keystore $keystore -storepass $password ${filePath} key0"
         }

| 
| **aliasVariable** - alias for the key which should be used from credentials keystore. In the example the key alias name is not defined within jenkins credentials but hardcoded in the pipeline straight (key0). 

**credentialsId** - the id of the keystore within jenkins credentials. In the example the dokoki project keystore is used

**keystoreVariable** - name of the keystore

**passwordVariable** - keystore password

**filePath** - not related to *withCredentials*, it is the path to the file which should be signed

Deletion of the META-INF folder is executed for the cases when e.g. gradle already signed the build and we need to override.

.. container:: confluence-information-macro confluence-information-macro-warning conf-macro output-block

   Possible errors

   .. container:: confluence-information-macro-body

      Following exceptions were observed in past due to certain bugs in version of java used for keystore generation:

      | 1. jarsigner error: java.lang.RuntimeException: keystore load: Integrity check failed: java.security.UnrecoverableKeyException: Failed PKCS12 integrity checking
      | 2. jarsigner error: java.lang.RuntimeException: keystore load: Integrity check failed: java.security.NoSuchAlgorithmException: Algorithm HmacPBESHA256 not available

      The solution was to re-generate p12 keystore (from jks or completely new one) within different version of java, e.g. java-1.11.0-openjdk-amd64 was used in successful scenario.
