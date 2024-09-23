com.amarula.deploy.Archiva
***************************

.. _com.amarula.deploy.Archiva-DocumentationforArchivaclass:

Documentation for Archiva class
===============================

The ``Archiva`` class provides methods for uploading files to the Archiva repository manager. This document explains how to use the class and its methods.

.. _com.amarula.deploy.Archiva-ImportingtheArchivaclass:

Importing the Archiva class
---------------------------

To use the ``Archiva`` class, you must import the ``com.amarula.deploy.Archiva`` package. Here is an example:

::

         import com.amarula.deploy.Archiva

.. _com.amarula.deploy.Archiva-CreatinganinstanceoftheArchivaclass:

Creating an instance of the Archiva class
-----------------------------------------

To create an instance of the ``Archiva`` class, you must provide the context of the script that uses this class, the server information, the name of the repository to upload to, and the subdirectories of the repository to upload to. Here is an example:

::

         def serverInfo = [ url: 'https://example.archiva.com/artifacts/repository', login: 'archiva_user', password: 'secret' ] 
         def archiva = new Archiva(ctx, serverInfo, "my-repo", "dirs/of/my/group/")


Parameters:
~~~~~~~~~~~

-  ``ctx``: The context of the script that uses this class.
-  ``serverInfo``: A map that contains the ``url``, ``login``, and ``password`` of the Archiva server.
-  ``repo``: The name of the repository to upload to.
-  ``dirs``: The subdirectories of the repository to upload to.

.. _com.amarula.deploy.Archiva-Settingtheremotepath:

Setting the remote path
-----------------------

To set the remote path of the repository and subdirectories to upload to, you can use the ``setRemotePath`` method of the ``Archiva`` class. Here is an example:

| 

::

         archiva.setRemotePath("another-repo", "another/dirs/of/my/group/")

| 

.. _com.amarula.deploy.Archiva-Parameters:.1:

Parameters:
~~~~~~~~~~~

-  ``repo``: The name of the repository to upload to.
-  ``dirs``: The subdirectories of the repository to upload to.

.. _com.amarula.deploy.Archiva-UploadingfilestoArchiva:

Uploading files to Archiva
--------------------------

To upload multiple files to the Archiva server, you can use the ``uploadFile`` method of the ``Archiva`` class. Here is an example:

::

         def uploadArtifacts = [
             [
                 paths : ["/path/to/my/file.zip", "/path/to/my/first/file.jar"], // A list of paths to local files to be uploaded for this artifact in Archiva.
                 name : "my-artifact-first-name", // The name of this artifact.
                 version : "1.0.0", // The version of this artifact.
                 packaging: "zip" // The packaging of this artifact.
             ],
             [
                 paths : ["/path/to/my/artifact.dll", "/path/to/my/artifact.jar"],
                 name : "my-artifact-second-name",
                 version : "1.0.1",
                 packaging: "zip"
             ]
         ]
         archiva.uploadFile(uploadArtifacts)

````

.. _com.amarula.deploy.Archiva-Parameters:.2:

Parameters:
~~~~~~~~~~~

-  ``artifacts``: A list of ``Map<String, Object>`` objects that represent the files to upload.


Return value:
~~~~~~~~~~~~~

-  ``true`` if all uploads were successful, ``false`` otherwise.

.. _com.amarula.deploy.Archiva-MethodsoftheArchivaclass:

Methods of the Archiva class
----------------------------

.. _com.amarula.deploy.Archiva-Archiva(ctx,serverInfo,Stringrepo,Stringdirs):

``Archiva(ctx, serverInfo, String repo, String dirs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Constructs a new ``Archiva`` instance with the given context and server information.

.. _com.amarula.deploy.Archiva-setRemotePath(Stringrepo,Stringdirs):

``setRemotePath(String repo, String dirs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sets the remote path of the repository and subdirectories to upload to.

.. _com.amarula.deploy.Archiva-uploadFile(List<Map<String,Object>>artifacts):

``uploadFile(List<Map<String, Object>> artifacts)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uploads multiple files to the Archiva server with the given artifact list.

.. _com.amarula.deploy.Archiva-generateManifestCommand(Stringname,Stringversion,Stringpackaging):

``generateManifestCommand(String name, String version, String packaging)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Private method to generate the POM manifest file for the artifact.

.. _com.amarula.deploy.Archiva-generateFileUploadCommand(StringsourcePath,Stringname,Stringversion):

``generateFileUploadCommand(String sourcePath, String name, String version)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Private method to generate the command that uploads a file to Archiva for a given artifact.

.. _com.amarula.deploy.Archiva-runArchiva(List<String>commands):

runArchiva(List<String> commands)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Private method that runs a list of shell commands to upload files to the Archiva repository.

.. _com.amarula.deploy.Archiva-Exampleusage:

Example usage
=============

::

         def serverInfo = [
             url: 'https://example.archiva.com/artifacts/repository',
             login: 'archiva_user',
             password: 'secret'
         ]
         def archiva = new Archiva(ctx, serverInfo, "my-repo", "dirs/of/my/group/")
         def uploadArtifacts = [
              [
                  paths    : ["/path/to/my/file.zip", "/path/to/my/first/file.jar"], // A list of paths to local files to be uploaded for this artifact in Archiva.
                  name     : "my-artifact-first-name", // The name of this artifact.
                  version  : "1.0.0", // The version of this artifact.
                  packaging: "zip" // The packaging of this artifact.
              ],
              [
                  paths    : ["/path/to/my/artifact.dll", "/path/to/my/artifact.jar"],
                  name     : "my-artifact-second-name",
                  version  : "1.0.1",
                  packaging: "zip"
              ]
         ]
         archiva.uploadFile(uploadArtifacts)
         archiva.setRemotePath("another-repo", "another/dirs/of/my/group/")
         archiva.uploadFile(uploadArtifacts)

| 
