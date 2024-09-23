Import credential certificate
******************************

.. _Importcredentialcertificate-ImportingcertificateviaUI:

Importing certificate via UI
============================

Jenkins → Credentials → System → <domain>→Add Credentials

Kind → Certificate

Upload certificate → select the keystore to upload

After filling particular fields and confirmation the certificate should start to be available under its ID for jenkins jobs.

Following example is for alcosystems ibac project:

.. image:: /images/import_credentials_jenkins.png

.. container:: confluence-information-macro confluence-information-macro-note conf-macro output-block

   Error message

   .. container:: confluence-information-macro-body

      After confirming the uploaded keystore file there might be still error message pressent (about the keystore not imported) but it will disappear after clicking on one of the fields (e.g. password).

.. _Importcredentialcertificate-ImportingcertificateviaSSH:

Importing certificate via SSH
=============================

In case the UI approach is not available for some reason, it is still possible to upload whole keystore via SSH by providing the Base64 encoded DER data (binary) of the keystore within XML structure.

The SSH has to be allowed within Global security configuration for certain port and user public key within his jenkins user profile as described here:

`https://www.jenkins.io/doc/book/managing/cli <https://www.jenkins.io/doc/book/managing/cli/#authentication>`__

The new credentials to be uploaded has to be in format of xml like this:

**Credential xml**

::

         <?xml version='1.0' encoding='UTF-8'?>
         <com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl plugin="credentials@2.3.14">
           <scope>GLOBAL</scope>
           <id>dokoki-bsg_androidMobileReleaseKeystore</id>
           <description>Keystore with google upload key for signing DOKOKI baby sleep guard mobile android application release (can be uploaded to google play then)</description>
           <keyStoreSource class="com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl$UploadedKeyStoreSource">
             <uploadedKeystoreBytes>
               {Base64 encoded binary keystore (.p12) data}
             </uploadedKeystoreBytes>
           </keyStoreSource>
           <password>
               {clear_password}
           </password>
         </com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl>

The sensitive values of keystore bytes and password are placed within brackets {}

In case of uploadedKeystoreBytes it has to be binary data of the .p12 keystore encoded to BASE64 format.

The XML can be then uploaded via ssh by following command:

**Jenkins SSH**

::

   ssh -l <user> -p <port> <address> create-credentials-by-xml <STORE> <DOMAIN> < <xml_file>

Example:

**Jenkins SSH**

::

   ssh -l miloslav.stefko -p 53801 localhost create-credentials-by-xml system::system::jenkins _ < newCredential.xml

In the example the default system STORE and unspecified DOMAIN is used ( \_ ).

If accessing from remote to `sirio.amarulasolutions.com <http://sirio.amarulasolutions.com>`__, the firewall rules have to be enabled accordingly.

| 
