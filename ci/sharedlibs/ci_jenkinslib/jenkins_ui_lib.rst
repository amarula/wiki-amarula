com.amarula.ui.UI
******************

.. _com.amarula.ui.UI-Overview:

Overview
--------

This class is used to build parameters for a Jenkins job. It provides a builder pattern for adding various types of parameters to a job, such as boolean, string, choice, and password parameters.

.. _com.amarula.ui.UI-UiClass:

Ui Class
--------

The Ui class is the main class that contains the builder pattern to add parameters to a Jenkins job. It is a serializable class that can be used to build parameters for a job. The class has the following attributes:

-  ``parameters``: A list of parameters that have been added.

-  ``context``: The context of the Jenkins job.

-  ``is_new``: A boolean value that indicates whether the class is new.

.. _com.amarula.ui.UI-Constructor:

Constructor
~~~~~~~~~~~

The Ui class has a private constructor that takes three parameters

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         private Ui(parameters, context, is_new = false)

-  ``parameters``: A list of parameters that have been added.
-  ``context``: The context of the Jenkins job.
-  ``is_new``: A boolean value that indicates whether the class is new. It defaults to false.

.. _com.amarula.ui.UI-Usage:

Usage
~~~~~

To use this ``Ui`` class, you need to create an instance of its ``Builder`` class and use it to add the parameters you need for your Jenkins job. Then you can call the ``build()`` method to create an instance of the ``Ui`` class, which contains the parameters as a property.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         def context = new SecureGroovyScript("").with {
             delegate = null
             getClass().classLoader = Jenkins.instance.pluginManager.uberClassLoader
             evaluate()
         }()

         def ui = new Ui.Builder(context)
             .addBooleanParameter('boolParam', false, 'A boolean parameter.')
             .addStringParameter('strParam', 'default', 'A string parameter.')
             .addChoiceParameter('choiceParam', ['option1', 'option2'], 'A choice parameter.')
             .build()

In this example, we create a new ``Ui.Builder`` instance with a new ``SecureGroovyScript`` instance. Then we use the builder to add a boolean parameter with a default value of ``false``, a string parameter with a default value of ``'default'``, and a choice parameter with options ``'option1'`` and ``'option2'``. Finally, we call the ``build()`` method to create an instance of the ``Ui`` class and get the parameters using the ``get()`` method.

.. _com.amarula.ui.UI-Methods:

Methods
~~~~~~~

The Ui class has the following methods:

.. _com.amarula.ui.UI-get():

``get()``
^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         def get()

This method returns the list of parameters that have been added.

.. _com.amarula.ui.UI-isNew():

``isNew()``
^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         boolean isNew()

This method returns a boolean value that indicates whether the class is new.

.. _com.amarula.ui.UI-BuilderClass:

Builder Class
-------------

The Ui class also has a static inner class called Builder. This class is used to add various types of parameters to the Ui class. The Builder class has the following attributes:

-  ``parameters``: A list of parameters that have been added.
-  ``context``: The context of the Jenkins job.
-  ``is_new``: A boolean value that indicates whether the class is new.

.. _com.amarula.ui.UI-getValuefromProp(name,defaultValue):

``getValuefromProp(name, defaultValue)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         protected def getValuefromProp(name, defaultValue)

This method is used to get the value of a property from the context of the Jenkins job. If the property does not exist, it creates the property and sets its value to the default value.

-  ``name``: The name of the property.
-  ``defaultValue``: The default value of the property.

.. _com.amarula.ui.UI-Builder(context):

``Builder(context)``
^^^^^^^^^^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Builder(context)

The constructor for the Builder class takes the context of the Jenkins job as a parameter.

-  ``context``: The context of the Jenkins job.

.. _com.amarula.ui.UI-addBooleanParameter(name,defaultValue,description):

``addBooleanParameter(name, defaultValue, description)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Builder addBooleanParameter(name, defaultValue, description)

This method is used to add a boolean parameter to the Ui class.

-  ``name``: The name of the parameter.
-  ``defaultValue``: The default value of the parameter.
-  ``description``: The description of the parameter.

.. _com.amarula.ui.UI-addStringParameter(name,defaultValue,description,trim=false):

``addStringParameter(name, defaultValue, description, trim = false)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Builder addStringParameter(name, defaultValue, description, trim = false)

This method is used to add a string parameter to the Ui class.

-  ``name``: The name of the parameter.
-  ``defaultValue``: The default value of the parameter.
-  ``description``: The description of the parameter.
-  ``trim``: A boolean value that indicates whether to trim the value of the parameter. It defaults to false.

.. _com.amarula.ui.UI-addChoiceParameter(name,choices,description):

``addChoiceParameter(name, choices, description)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Builder addChoiceParameter(name, choices, description) 

This method is used to add a choice parameter to the Ui class.

-  ``name``: The name of the parameter.
-  ``choices``: The list of choices for the parameter.
-  ``description``: The description of the parameter.

.. _com.amarula.ui.UI-addPasswordParameter(name,defaultValue,description):

``addPasswordParameter(name, defaultValue, description)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Builder addPasswordParameter(name, defaultValue, description)

::

This method is used to add a password parameter

.. _com.amarula.ui.UI-build():

``build()``
^^^^^^^^^^^

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         Ui build()

This method builds the ``Ui`` object and returns it. It creates a ``props`` list, which contains the ``parameters`` list as a property definition, and sets it as a property of the ``context`` object. It then creates a new ``Ui`` instance with the ``context``, ``properties``, and \`is_new

| 
