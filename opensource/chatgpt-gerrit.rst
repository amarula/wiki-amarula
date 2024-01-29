====================
ChatGPT meets Gerrit
====================

Motivation
----------

`Gerrit <https://www.gerritcodereview.com/>`__ is a web-based code review and project management tool for Git repositories. It facilitates collaborative coding by allowing developers to submit their changes to a central server, where others can review, discuss, and ultimately approve the changes before they are merged into the project. This process enables **multiple eyes to scrutinize every piece of code**.

At `Amarula <https://www.amarulasolutions.com/>`__, we extensively utilize Gerrit for our development processes, leveraging its robust code review and collaboration features. In light of its features, we concluded that the pairing of Gerrit and ChatGPT was a match already in the making. In our relentless quest for enhanced code quality and improved project management efficiency, we believe that incorporating ChatGPT into Gerrit can refine the review process and introduce an **extra dimension of AI-powered intelligence**.

As a **Virtual Gerrit User**, ChatGPT should be empowered to

* Offer **Insights** and **Suggestions**
* Provide **Automated Code Analysis**
* Respond to **Queries from Developers**

Control is the Key
------------------

*Talking about tools, the thin line that separates a dream from a nightmare is Control.*

Bearing this key principle in mind, it is essential that Gerrit administrators have the capability to selectively enable the ChatGPT review function for particular projects, users, groups, and topics.

**The reins of control are tightly held by the developers**, as shown in the following workflow:

* A Gerrit Patch Set that has the ChatGPT review function enabled is submitted to the Gerrit Server.
* ChatGPT delivers an initial insight on the Patch Set, and this insight is displayed within the Gerrit UI.
* Developers have the option to either disregard or act on the insight.
* Developers can also decide to **continue the dialogue with ChatGPT within the Gerrit UI** to gain additional insights.

Alternatively, the process can also begin when **developers use the Gerrit UI to start any conversation with ChatGPT** on their own, whether it’s a general discussion or based on a specific section of a Patch Set code.

The so-designed Gerrit plugin is available as Open Source project at https://github.com/amarula/chatgpt-code-review-gerrit-plugin/.

Quickstart
----------

Before diving into the specifics of the ChatGPT plugin, it's essential to have a Gerrit server up and running.

System Requirements
~~~~~~~~~~~~~~~~~~~

* Java SE Runtime Environment version 11 and up.
* Maven 3.0 or higher.

Installing Gerrit Server
~~~~~~~~~~~~~~~~~~~~~~~~

Below is an extract from the `Quickstart for Installing Gerrit on Linux <https://gerrit-review.googlesource.com/Documentation/linux-quickstart.html>`__. To install a Gerrit production environment, the `Standalone Daemon Installation Guide <https://gerrit-review.googlesource.com/Documentation/install.html>`__ should be followed instead.

1. **Download Gerrit** from the official `Gerrit Releases page <https://gerrit-releases.storage.googleapis.com/index.html>`__.
The command below downloads Gerrit 3.9.1:

.. code-block:: none

        wget https://gerrit-releases.storage.googleapis.com/gerrit-3.9.1.war

2. **Initialize Gerrit**

.. code-block:: none

        export GERRIT_SITE=~/gerrit_testsite
        java -jar gerrit*.war init --batch --dev -d $GERRIT_SITE

3. **Start Gerrit**

.. code-block:: none

        $GERRIT_SITE/bin/gerrit.sh start

Installing Gerrit ChatGPT plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following is an extract from the `Getting Started <https://github.com/amarula/chatgpt-code-review-gerrit-plugin/#getting-started>`__ section, intended for demonstration purposes. For production installation, please refer to the full guide at https://github.com/amarula/chatgpt-code-review-gerrit-plugin/.

1. **Download the plugin code**

.. code-block:: none

        git clone https://github.com/amarula/chatgpt-code-review-gerrit-plugin.git

2. **Build the plugin**

.. code-block:: none

        cd chatgpt-code-review-gerrit-plugin
        mvn -U clean package

3. **Install the plugin**

   Upload/copy the compiled jar file from the ``./target`` directory to ``$GERRIT_SITE/plugins``.

4. **Configure the plugin**

   First, create a ChatGPT user in Gerrit.
   Then, set up the basic parameters in ``$GERRIT_SITE/etc/gerrit.config`` file, under the section

   ``[plugin "chatgpt-code-review-gerrit-plugin"]``:

- ``gptToken``: OpenAI GPT token.
- ``gerritAuthBaseUrl``: The URL of Gerrit instance, similar to ``https://gerrit.local.team``.

  **NOTE**: Do not append "/a" authentication sub-path to the URL.
- ``gerritUserName``: Gerrit username of ChatGPT user.
- ``gerritPassword``: Gerrit password of ChatGPT user.
- ``globalEnable``: Default value is false. The plugin will only review specified repositories. If set to true, the plugin will by default review all pull requests.

5. **Restart Gerrit**

.. code-block:: none

        $GERRIT_SITE/bin/gerrit.sh restart

Going to Production
-------------------

We are convinced that this initiative is not just a mere experiment. It’s a full-fledged implementation being rigorously tested in the crucible of real-world, production environments. This real-time testing scenario provides us with a golden opportunity to refine the integration, informed by practical feedback and demands for functionality enhancements.

We realized that it was the right time to move to production. Let's take a look at the outcome.

Patch Set Review
----------------

ChatGPT, acting as a vigilant overseer, reviews Patch Sets of selected Gerrit projects as they arrive. This feature ensures that each submission undergoes a preliminary AI-driven analysis, setting a high standard of quality and coherence right from the start.

.. figure:: /images/chatgpt_patchset_review.png

    ChatGPT's insight on a patched code segment in Kotlin

Behind the scenes, the path towards enhancing the quality of ChatGPT’s responses was achieved through meticulous prompt engineering. This significant progression involved more than just fine-tuning algorithms; it focused on understanding the delicate dynamics of developer interactions and tailoring the responses to align with these nuances.

An additional feature allows for examining the congruence of the **commit messages** with the Patch Sets’ changes, ensuring that the narrative of the commit aligns with the actual modifications made.

.. figure:: /images/chatgpt_patchset_review_commit_message.png

    ChatGPT's insight on a Patch Set commit message

Interactive Assistance
----------------------

ChatGPT goes beyond being just a tool, acting more like a virtual colleague. It’s ready to respond to user inquiries, offering suggestions, and clarifying any doubts. This function is akin to having an additional team member, one that’s always available to provide insights and clarifications, much like a knowledgeable human peer.

The ability to start conversations with ChatGPT directly from an inline comment adds a layer of dynamism to the interaction. Users can request reviews on specific parts of the code, extending even beyond the current Patch Set, or ask for improvement suggestions. This feature essentially brings an on-demand code review assistant into the workflow, available at the click of a button.

In the following example, a further inquiry about how to implement a change recommended by ChatGPT is showcased.

.. figure:: /images/chatgpt_interactive_assistance_cropped.png

    ChatGPT's interaction on a patched code segment in Java

In the example showcased next, ChatGPT is queried about a different implementation approach on a code segment that **isn’t directly related to the changes** in the Patch Set.

.. figure:: /images/chatgpt_query_min.png
    :width: 650

    ChatGPT interaction in response to an inquiry about a code line from a Python project

Adjusting Verbosity Level
-------------------------

The verbosity level can be further increased by specifically requesting multiple alternatives and code examples.

.. figure:: /images/chatgpt_query_max.png
    :width: 650

    ChatGPT interaction in response to an inquiry about a code line from a Python project

It is also possible to submit broader inquiries about the entire Patch Set.

.. figure:: /images/chatgpt_query_entire_patchset_bounds.png
    :width: 650

    ChatGPT answer to a broad query related to a Kotlin project

Security and Privacy
--------------------

Last but certainly not least, we give utmost importance to security and privacy.

Recognizing scenarios where code confidentiality is paramount, we’ve introduced a new configuration option (``gptFullFileReview``) which, when set to false, restricts the code reviewed by ChatGPT to only the changes made, without including the entire file. This feature ensures that sensitive information remains within the confines of the organization, thus safeguarding intellectual property and adhering to privacy standards.

Conclusion
----------

Our exploration of the integration of ChatGPT into Gerrit has highlighted several key points:

* **Virtual Gerrit Collaborator**: We’ve discussed the groundbreaking integration of ChatGPT into a Gerrit plugin, showcasing how it acts not just as a tool but as a Virtual Collaborator in the development process.
* **Control and Customization**: We emphasized the importance of control, allowing Gerrit administrators to selectively activate ChatGPT for specific projects, users, groups, and topics, and enabling developers to maintain a firm grip on the reins of control. This ensures that ChatGPT’s insights are relevant and aligned with the developers’ needs.
* **Interactive and Responsive Nature**: The feature that allows developers to continue conversations based on initial insights or start new ones independently showcases the interactive and responsive nature of the plugin.
* **Security and Privacy**: We shared best practices for maintaining security and privacy when using ChatGPT within Gerrit.

By integrating ChatGPT into Gerrit, we aim to enhance code quality, streamline project management, and introduce AI-driven intelligence into the software development lifecycle. This integration is a step towards a more efficient, collaborative, and intelligent coding environment, highlighting our commitment to innovation and excellence in software development.
