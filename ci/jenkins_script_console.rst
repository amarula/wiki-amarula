Jenkins script console
**********************

.. note:: **TL;DR**
   - How to access the **Jenkins script console** on a per-node basis — for running Groovy scripts and shell commands directly on Jenkins agents (e.g., cleaning up Docker images on a specific node).

The particular nodes can be accessed via the script console (in browser UI) and if allowed execute also the shell commands.

| It can be found when clicked on specific node:

.. image:: /images/jenkins_script_console.png

| And then on "Script console" in left menu:

.. image:: /images/jenkins_script_console_2.png

The edit text area will appear with some example how should prompts look like.

E.g. you can remove some docker images from the particular node, in following example we remove the mobile-app docker image from local docker registry:

.. image:: /images/jenkins_script_console_editor.png

.. tip::
   Need help with Jenkins node administration or script console automation?
   Amarula Solutions provides Jenkins infrastructure management and
   troubleshooting for embedded CI/CD environments.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
