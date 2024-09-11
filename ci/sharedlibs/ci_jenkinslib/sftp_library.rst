com.amarula.deploy.Sftp
************************

.. container:: contentLayout2

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. container:: toc-macro client-side-toc-macro conf-macro output-block

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Constructors
               :name: com.amarula.deploy.Sftp-Constructors

            .. rubric:: Sftp(steps, environment, String url, port, String credentialsId)
               :name: com.amarula.deploy.Sftp-Sftp(steps,environment,Stringurl,port,StringcredentialsId)

            Create instance of Sftp to handle remote operations.

            -  **steps** Jenkins steps (steps variable in pipeline context)
            -  **environment** Jenkins environment variables (env variable in pipeline context)
            -  **url** SFTP server URL
            -  **port** SFTP server port
            -  **credentialsId** ID of USERNAME-PASSWORD credentials stored in Jenkins

            .. rubric:: Public methods
               :name: com.amarula.deploy.Sftp-Publicmethods
               :class: auto-cursor-target

            .. rubric:: def setRemotePath(String path)
               :name: com.amarula.deploy.Sftp-defsetRemotePath(Stringpath)

            Set remote path on SFTP server where to upload files.

            -  **path** Remote path

            .. rubric:: boolean createDirectory(String path)
               :name: com.amarula.deploy.Sftp-booleancreateDirectory(Stringpath)

            Create directory including it's parent directories if they do not exist.

            -  **path** Remote path

            Returns: true if all directories were created or already existed.

            .. rubric:: boolean fileExists(String path)
               :name: com.amarula.deploy.Sftp-booleanfileExists(Stringpath)

            Checks whether file or directory exists.

            -  **path** Remote path

            Returns: true if file/directory exists.

            .. rubric:: boolean uploadFile(String remotePath = path, List<String> localFiles)
               :name: com.amarula.deploy.Sftp-booleanuploadFile(StringremotePath=path,List<String>localFiles)

            Upload given files to given remote location. Existing files will get overwritten. Missing directories won't be created.

            **remotePath = path** Remote path

            **localFiles** Local paths

            Returns: true if all files were successfully uploaded.

            .. rubric:: Private methods
               :name: com.amarula.deploy.Sftp-Privatemethods

            .. rubric:: private boolean runSftp(List<String> commands)
               :name: com.amarula.deploy.Sftp-privatebooleanrunSftp(List<String>commands)

            Run given sftp commands as a batch. Commands that by default can fail are: get, put, reget, reput, rename, ln, rm, mkdir, chdir, ls, lchdir, chmod, chown, chgrp, lpwd, df, symlink, and lmkdir. When command fails the rest of the commands won't be executed and this method will return false. If you do not wish to fail on a command then put '-' before it, e.g. '-rm /path/file'.

            -  **commands** Commands to execute

            Returns: true if commands were successfully executed.
