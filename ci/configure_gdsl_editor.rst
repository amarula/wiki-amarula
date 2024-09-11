Configure editor using GDSL
****************************

GDSL is a Groovy-based Domain Specific Language that allows users to define and configure Jenkins jobs in a programmatic way. GroovyDSL is a framework designed to define the behaviour of end-user DSLs as script files which are executed by the IDE on the fly, bringing new reference resolution and code completion (commonly called as auto-completion) logic into the scope of a project. GroovyDSL relies on the Program Structure Interface (PSI), a set of internal classes and interfaces of IntelliJ IDEA, which allow all programming languages to be described in a uniform way. Due to Groovy's meta-programming capabilities, the developer of DSL descriptions in GroovyDSL need not be aware of how PSI works. All interoperation with PSI is covered by calls to methods and properties of GroovyDSL scripts.

It is useful for creating and maintaining complex pipelines, managing configuration as code, and automating job creation. Jenkins GDSL works by using a plugin called Job DSL that generates .gdsl files for Jenkins jobs based on Groovy scripts.

.. _ConfigureeditorusingGDSL-AdvantagesofGDSLfiles:

Advantages of GDSL files
~~~~~~~~~~~~~~~~~~~~~~~~

#. It can push these files with the code and all the developers in the team will start getting auto-completes for the dynamic code.
#. Simple to write and understand as they use the groovy DSL format.
#. These files can be packaged in a jar and all projects using that jar will start getting auto-completes and syntax hinting for the dynamic code.

.. _ConfigureeditorusingGDSL-GettingGDLSfromthepipelineintoIntelliJIDEA:

Getting GDLS from the pipeline into IntelliJ IDEA
=================================================

A way to make IntelliJ IDEA aware of the pipeline DSL syntax, which supports the developer with auto-completion and documentation, is to generate GDLS from pipeline/s.

1] Visit web interface and go directly to pipeline, what you want to use the *Pipeline Syntax Snippet Generator.*

2] Click on *Pipeline Syntax*

.. image:: /images/gdsl_pipeline_syntax.png

3] Click on *IntelliJ IDEA GDSL*

.. image:: /images/gdsl_pipeline_syntax_2.png

4] Select all and copy content into *pipeline.gdls* (name can be different) file into the some folder (which is mark as Sources Root) in project.

5] After finishing editing and saving a GroovyDSL script one can notice a yellow band on top of an editor screen, informing, that modified GroovyDSL script should be reloaded. After clicking on it an actual script will be processed and activated to make the IDE aware about new behaviour.

.. _ConfigureeditorusingGDSL-Troubleshooting:

Trouble shooting
----------------

.. _ConfigureeditorusingGDSL-IDEisn'tawareofchangesinGDSL:

IDE isn't aware of changes in GDSL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After putting the contents of the Jenkins output into a f.e. *pipeline.gdsl* file in the **src/** folder if IDE is not aware of changes, it need to be done importing these changes. Importing can be done by marking my project as a new Groovy project withing IntelliJ (*File > New > Project from Existing Sources…*). After confirmation of options within creation of project from existing sources a message popped up: *DSL descriptor file has been change and isn’t currently executed*. Click on Activate back and let IDEA reload sources.

.. _ConfigureeditorusingGDSL-MarkingfolderasSourceroot:

Marking folder as Source root
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For an example go to **src** folder, right click on it and from the dialog select → Mark directory as → Sources Root.

.. _ConfigureeditorusingGDSL-CreatingGDSLscript:

Creating GDSL script
~~~~~~~~~~~~~~~~~~~~

For an example go to **src** folder, right click on it and from the dialog select new → Groovy Script. Now a dialog will appear and then select “GroovyDSL Script” in the “kind” parameter. Now you have the script file and you can start coding GDSL in here. `see more here <https://youtrack.jetbrains.com/articles/GROOVY-A-15796912#contexts-and-contributors>`__

.. image:: /images/create_gdsl.png

.. _ConfigureeditorusingGDSL-Auto-completionforsharedlibraries:

Auto-completion for shared libraries
====================================

Getting GDLS from the pipeline has caveats and that means it will not generate code for custom global variables and functions from shared libraries.  We have few possibilities to workaround:

#. Manually edit the *pipeline.gdsl* file which was generated over Jenkins interface and implement missing classes, variables and functions. The guide describing GDSL contexts and contributors is located in this `knowledge base <https://youtrack.jetbrains.com/articles/GROOVY-A-15796912#contexts-and-contributors>`__. It contains few examples of GDLS scripting.
#. Dependency can be created by extending projects of maven or gradle file into the both projects: Shared-library and Jenkinsfile projects. It need to set up specific group id, artifact id and version. It should perform 'mvn install' whenever it change the shared library (this goal used to add shared library jar artifact to the local maven repository). In another repository where it will write the jenkins file, it should also create a maven project and just add the shared library as a maven dependency. Then it should be possible use code autocompletion from the shared library in the jenkins file.
#. Autogenerating gdsl:

   #. Create own script that generate GDSL. There is no existing code that is able to generate script for 3rd party libraries. The script will iterate over all packages and classes in the shared library and generate contributors and extend the *pipeline.gdsl* file which was generated over Jenkins interface.
   #. Install plugin `jenkins-pipeline-shared-libraries-gradle-plugin <https://github.com/mkobit/jenkins-pipeline-shared-libraries-gradle-plugin>`__ onto Jenkins. There is also an `example repository <https://github.com/mkobit/jenkins-pipeline-shared-library-example>`__ for a demonstration of using this plugin.
   #. Look closer if GDSL generator exists.

| 

// TODO decide on the GDLS for shared library approach and prepare. Few discussions that I have found\ `1 <https://gist.github.com/arehmandev/736daba40a3e1ef1fbe939c6674d7da8>`__\ `2 <https://github.com/jaydubb12/jenkins-dsl-pipelines>`__\ `3 <https://stackoverflow.com/questions/53363828/jenkins-shared-library-with-intellij>`__\ and haven't include into options above.

.. _ConfigureeditorusingGDSL-Resources:

Resources
---------

-  `Pipeline Development Tools <https://jenkins.io/doc/book/pipeline/development/>`__
-  `Scripting IDE for DSL awareness <https://confluence.jetbrains.com/display/GRVY/Scripting+IDE+for+DSL+awareness>`__
-  Jenkinsfile support `plugin <https://marketplace.visualstudio.com/items?itemName=secanis.jenkinsfile-support>`__ for Visual Studio Code
-  `Jenkins pipeline autocompletion in intellij <https://st-g.de/2016/08/jenkins-pipeline-autocompletion-in-intellij>`__

| 
