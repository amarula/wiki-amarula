Pipeline script snippets
*************************

.. container:: contentLayout2

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            | 

            .. container:: table-wrap

               +---------------------------------------------------------------------------+
               | .. container:: content-wrapper                                            |
               |                                                                           |
               |    .. container:: toc-macro client-side-toc-macro conf-macro output-block |
               +===========================================================================+
               +---------------------------------------------------------------------------+

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Useful examples:
               :name: Pipelinescriptsnippets-Usefulexamples:

            -  https://jenkins.io/doc/pipeline/examples/
            -  https://www.cloudbees.com/blog/parallelism-and-distributed-builds-jenkins

            .. rubric:: Working with quotes and variables
               :name: Pipelinescriptsnippets-Workingwithquotesandvariables

            The double quotes " x " allow to expand groovy variables (vat, groovyVar). To use double quotes and use shell variable the $ has to be escaped.

            The single quotes ' x ' won't expand groovy variables and so shell scripts can be written without escaping the $.

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     node() {
                       def var = 'variable'
                       def groovyVar = "groovy ${var}"

                       sh """
                         echo "groovyVar=${groovyVar}"
                         shellVar="shell variable"
                         echo "shellVar=\${shellVar}"
                       """
                       
                       sh '''
                         shellVar="shell variable"
                         echo "shellVar=${shellVar}"
                       '''
                     }

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     [Pipeline] sh
                     + echo groovyVar=groovy variable
                     groovyVar=groovy variable
                     + shellVar=shell variable
                     + echo shellVar=shell variable
                     shellVar=shell variable
                     [Pipeline] sh
                     + shellVar=shell variable
                     + echo shellVar=shell variable
                     shellVar=shell variable

            | 

            .. rubric:: Sharing artifacts between jobs
               :name: Pipelinescriptsnippets-Sharingartifactsbetweenjobs

            Usage of plugin in pipeline script: https://wiki.jenkins-ci.org/display/JENKINS/Copy+Artifact+Plugin

            Following snippet is the simplest way how to use artifact of a different job in yours. It is useful when you don't need specific version of the artifact you want to use. It does not matter on which node was the artifact built or on which will your job run.

            This plugin will copy the artifact from the latest stable (the last green) build of a specified job/project. When project doesn't exists or there no stable builds, exception is thrown. Therefore it is suggested to surround the code in try - catch if you want to handle the situation.

            Parameters:

            -  projectName: <String>, NOT optional

               -  Specify job/project you want the artifact from. Use the real name (not display name) including parent directories.
               -  You can see the name in the overview of your job/project as e.g. "Full project name: application_build/cts_setup_app".

            -  filter: <String>, optional

               -  Specific name or regular expression to match artifacts.

            -  target: <String>, optional

               -  Artifacts are copied to your current working directory if 'target' not specified.
               -  All non-existing folders in path are created - 'target/dir/another/dir/'.
               -  Even when you try to specify new name for the artifact, it will create a directory - 'target/path/name.apk' will lead to copying to target/path/name.apk/<artifact_name>.

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     node('...') {
                         stage('...') {
                             try {
                                 step ([$class: 'CopyArtifact',
                                         projectName: 'application_build/cts_setup_app',
                                         filter: '*.apk',
                                         target: 'target/path/']);
                             } catch (err) {
                                 echo "No successfull build :("
                             }
                         }
                     }

            .. rubric:: Parametrized building
               :name: Pipelinescriptsnippets-Parametrizedbuilding
               :class: auto-cursor-target

            Builds can be parametrized by choosing "This project is parameterized" option. Afterwards you can choose from various parameter types where the most simple are:

            -  String Parameter - value can be any String
            -  Choice Parameter - value is picked from pre-defined list of Strings

            Every parameter requires unique name which is used later in pipeline to receive its value:

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeHeader panelHeader pdl

                  **Acquiring build parameter value in the pipeline**

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     // we checkout specific revision according to the build parameter "revision_tag" defined by user
                     sh "git reset --hard ${revision_tag}"

            .. rubric:: Extendend choice parameters
               :name: Pipelinescriptsnippets-Extendendchoiceparameters

            Provides more complex way for jenkins parametrized builds to fulfill specific requirements.

            Following example provide one mandatory choice (BUILD_DEVICE parameter) and optional parameters which can be included one by one when running build. Declaration of parameters is done via `json-editor <https://github.com/jdorn/json-editor>`__ used in `extended choice parameters <https://wiki.jenkins-ci.org/display/JENKINS/Extended+Choice+Parameter+plugin>`__ `plugin <https://wiki.jenkins-ci.org/display/JENKINS/Extended+Choice+Parameter+plugin>`__:

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeHeader panelHeader pdl hide-border-bottom

                  **Array of parameters defined via json-editor**  Expand source

               .. container:: codeContent panelContent pdl hide-toolbar

                  .. code:: syntaxhighlighter-pre

                     import org.boon.Boon;

                     def jsonEditorOptions = Boon.fromJson(/{
                             disable_edit_json: true,
                             disable_properties: true,
                             no_additional_properties: true,
                             disable_collapse: true,
                             disable_array_add: false,
                             disable_array_delete: false,
                             disable_array_reorder: true,
                             theme: "bootstrap2",
                             iconlib:"none",
                     schema: {
                         "title": "YelloPad build options",
                         "type": "object",
                         "properties": {
                              "BUILD_DEVICE": {
                                 "title": "Boot device",
                                 "type": "string",
                                 "uniqueItems": true,
                                 "enum": [
                                     "emmc",
                                     "sdcard"
                                 ]
                             },
                             "BUILD_PARAMETERS": {
                                 "type": "array",
                                 "format": "table",
                                 "title": "Build Parameters",
                                 "uniqueItems": true,
                                 "items": {
                                     "type": "object",
                                     "title": "Parameter",
                                     "properties": {
                                         "Value": {
                                             "type": "string",
                                             "propertyOrder" : 2
                                         },
                                         "type": {
                                             "type": "string",
                                             "enum": [
                                                 "BUILD_TAG",
                                                 "BUILD_TOPIC"
                                             ],
                                             "propertyOrder" : 1
                                         }
                                     }
                                 }
                             }
                         }
                     }/);

                     return jsonEditorOptions;

            Particular values can be passed to pipeline via String representation of JSON. In order to conveniently access its values you can use groovy parser JsonSlurper as in following example:

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeHeader panelHeader pdl

                  **Extended choice parameters passed to pipeline**

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     // BuildParams is the name of extended choice parameter,
                     // we access its string value in same way as within simple jenkins parameters
                     def json = new JsonSlurper().parseText("${BuildParams}")
                     // we print the mandatory parameter value which is simply in the root of jason
                     println(json.BUILD_DEVICE)
                     // we look for BUILD_TAG parameter inside of dynamic parameters array and print its value
                     json.BUILD_PARAMETERS.each{ if(it.type.equals("BUILD_TAG")) {println(it.Value)}}

   .. container:: columnLayout two-equal

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Successful builds as parameter
               :name: Pipelinescriptsnippets-Successfulbuildsasparameter

            Requires `Extensible Choice Parameter plugin. <https://wiki.jenkins.io/display/JENKINS/Extensible+Choice+Parameter+plugin>`__

            This snippet allows you to create a dropdown selection menu that consists of list of successful builds of another job. You can then use the string description to download artifacts of that job. E.g. selecting chromium version to be included in Android OS build.

            Select the 'Extensible Choice' parameter type and then 'System Groovy Script Choice Parameter' as Choice Provider.

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     def builds = ['AOSP_PREBUILT']

                     def projectDir = jenkins.model.Jenkins.instance.getItem('2n')
                     def jobs = projectDir.getAllJobs()
                     def chromiumJob
                     jobs.each { 
                       if (it.name.equals('chromium'))
                         chromiumJob = it
                     }
                     chromiumJob.getBuilds().each {
                       if (it.getResult().toString().equals("SUCCESS"))
                         builds.add(it.description)
                     }
                     return builds
            
            .. image:: /images/pipeline_script_snippet.png

            It can look like this when starting a new job:

            .. image:: /images/pipeline_script_snippet_1.png

      .. container:: cell normal

         .. container:: innerCell

   .. container:: columnLayout single

      .. container:: cell normal

         .. container:: innerCell

            .. rubric:: Use Amarula docker registry in Jenkins pipeline
               :name: Pipelinescriptsnippets-UseAmaruladockerregistryinJenkinspipeline

            https://jenkins.io/doc/book/pipeline/docker/#using-a-remote-docker-server

            .. container:: code panel pdl conf-macro output-block

               .. container:: codeContent panelContent pdl

                  .. code:: syntaxhighlighter-pre

                     node("android-os-build") {
                          stage('Build OS') {
                             docker.withRegistry('https://registry.amarulasolutions.com:443','amarula-docker') {
                                 docker.image ('android-marshmallow-builder').inside {
                                     timestamps {
                                     }
                                 }
                             }
                         }
                     }
