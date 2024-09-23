Shared libraries
*****************

.. container:: contentLayout2

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            There are huge possibilities of jenkins usage. As the pipelines for various purposes grown in time, some of the pipelines code was repeating and that is where shared libraries become handy. Share library written in groovy is compiled and imported as dependency to any pipeline where needed.

            Following main features are currently supported

            -  Working with remote git repositories including the repo multiprojects (as it is in Android open source project)
            -  Working with gerrit code review system
            -  Building and verification of the projects
            -  Notifications to gerrit review system and to communication channels about the verification results
            -  Parametrization of the builds via UI (set your build/release parameters within UI template)
            -  Automated changelog description for the releases
            -  Static code analysis via SonarQube and CodeChecker
            -  Vulnerabilities analysis via Mend

            The particular features were split into several shared libraries logically by its purpose.

            -  `Automated tests <https://confluence.amarulasolutions.com/display/CI/Automated+tests>`__
            -  `Changelog Jenkins library <./changelog_lib/index.html>`__
            -  `CI Jenkins library <./ci_jenkinslib/index.html>`__
            -  `CodeChecker Jenkins library <./codechecker_jenkinslib.html>`__
            -  `Mend Jenkins library <./whitesource_jenkinslib.html>`__
            -  `Repo Jenkins library <./repo_jenkinslib/index.html>`__
            -  `Shared resource Jenkins library <https://confluence.amarulasolutions.com/display/CI/Shared+resource+Jenkins+library>`__
            -  `UI Jenkins library <https://confluence.amarulasolutions.com/display/CI/UI+Jenkins+library>`__

   .. container:: columnLayout two-equal

      .. container:: cell normal

         .. container:: innerCell

            Public Jenkins shared library documentation: https://jenkins.io/doc/book/pipeline/shared-libraries/

            Public Gerrit Trigger plugin documentation: https://plugins.jenkins.io/gerrit-trigger/

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Adding shared library
               :name: Sharedlibraries-Addingsharedlibrary
               :class: auto-cursor-target

            Add the repository to your Jenkins instance as Shared library:

            #. go to "Manage Jenkins" > "Configure System"
            #. scroll down to "Global Pipeline Libraries" section
            #. use "Add" and fill in the name of the library, default version and retrival method (Git is highly recommended):

               #. Name: ci_scripts
               #. Default version: master
               #. Retrieval method → Modern SCM

                  #. Source Code Management → Git
                  #. Project Repository: ssh://gitea@gitea.amarulasolutions.com:38745/i-tools/ci_jenkins_lib.git

            #. "Save"

            The library can be loaded into every pipeline by selecting "Load implicitly".

            It is useful for testing to be able to change the version of the library (tag / branch). Select "Allow default version to be overridden" to enable this.

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Importing shared library
               :name: Sharedlibraries-Importingsharedlibrary

            By setting option 'load implicitly' to true, the library is loaded into the node automatically. To import the set version use:

            ::

                     import com.amarula.*
                     /* OR */
                     import com.amarula.build.Build
                     import com.amarula.deploy.Sftp

            | 
            | Importing shared library without the 'load implicitly' option would look like:

            ::

                     @Library('ci_scripts')
                     import com.amarula.*

            Specific version of library can be loaded using '@<version>'. Version refers to tag, branch or commit id.

            ::

                     /* Using a version specifier, such as branch, tag, etc */
                     @Library('ci_scripts@devel')
                     import com.amarula.*
                     
