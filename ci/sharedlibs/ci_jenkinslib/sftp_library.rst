com.amarula.deploy.Sftp
************************

.. note:: **TL;DR**
   - Reference for the ``Sftp`` class from Amarula Solutions' **CI Jenkins shared library** — provides methods for secure file transfer to SFTP servers, with support for file uploads, downloads, and directory operations.

.. container:: contentLayout2

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Constructors
               :name: com.amarula.deploy.Sftp-Constructors

            .. rubric:: Sftp(steps, environment, String url, port, String credentialsId)

            Creates new instance for SFTP operations.

            -  **steps** Jenkins steps (this variable in pipeline context)
            -  **environment** Jenkins environment variables (env variable in pipeline context)
            -  **url** SFTP server URL
            -  **port** SFTP server port
            -  **credentialsId** Jenkins Credentials ID for SFTP authentication

            .. rubric:: Methods

            upload(String localPath, String remotePath)
                Uploads a file from local path to the remote SFTP server.

            download(String remotePath, String localPath)
                Downloads a file from the SFTP server to the local path.

.. tip::
   Need secure artifact deployment in your CI/CD pipeline? Amarula Solutions
   provides SFTP integration for build artifact distribution and deployment
   automation in embedded software projects.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
