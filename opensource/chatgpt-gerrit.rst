====================
ChatGPT meets Gerrit
====================

Motivation
----------

`Gerrit <https://www.gerritcodereview.com/>`__ is a web-based code review and project management tool for Git repositories. It facilitates collaborative coding by allowing developers to submit their changes to a central server, where others can review, discuss, and ultimately approve the changes before they are merged into the project. This process enables **multiple eyes to scrutinize every piece of code**.

At `Amarula <https://www.amarulasolutions.com/>`__, we extensively utilize Gerrit for our development processes, leveraging its robust code review and collaboration features. In light of its features, we concluded that the pairing of Gerrit and ChatGPT was a match already in the making. In our relentless quest for enhanced code quality and improved project management efficiency, we believe that incorporating ChatGPT into Gerrit can refine the review process and introduce an extra dimension of AI-powered intelligence.

As a **virtual Gerrit user**, ChatGPT should be empowered to

* offer insights and suggestions,
* provide automated code analysis, and
* respond to queries from developers.

Control is the Key
------------------

    Talking about tools, the thin line that separates a dream from a nightmare is Control.

Bearing this key principle in mind, it is essential that Gerrit administrators have the capability to selectively enable the ChatGPT review function for particular projects, users, groups, and topics.

**The reins of control are tightly held by the developers**, as shown in the following workflow:

* A Gerrit PatchSet that has the ChatGPT review function enabled is submitted to the Gerrit Server.
* ChatGPT delivers an initial insight on the PatchSet, and this insight is displayed within the Gerrit UI.
* Developers have the option to either disregard or act on the insight.
* Developers can also decide to **continue the dialogue from this insight through the Gerrit UI** to gain additional insights.

Alternatively, the process can also begin when **developers use the Gerrit UI to start any conversation with ChatGPT** on their own, whether it’s a general discussion or based on a specific section of a PatchSet code.

Going to Production
-------------------

The so-designed Gerrit plugin is available as Open Source project at https://github.com/amarula/chatgpt-code-review-gerrit-plugin/.

This initiative is not just a mere experiment. It’s a full-fledged implementation being rigorously tested in the crucible of real-world, production environments. This real-time testing scenario provides us with a golden opportunity to refine the integration, informed by practical feedback and demands for functionality enhancements.

Let’s see it in action.

PatchSet Review
---------------

ChatGPT, acting as a vigilant overseer, reviews PatchSets of selected Gerrit projects as they arrive. This feature ensures that each submission undergoes a preliminary, AI-driven analysis, setting a high standard of quality and coherence right from the start.

.. image:: /images/chatgpt_patchset_review.png
    :width: 1200

Behind the scenes, the path towards enhancing the quality of ChatGPT’s responses was achieved through meticulous prompt engineering. This significant progression involved more than just fine-tuning algorithms; it was centered on grasping the subtleties of developer interactions and customizing the responses to match these nuances. The enhanced ChatGPT plugin can now focus more precisely on identifying and correcting code issues.

Moreover, it can examine the congruence of **commit messages** with the PatchSets’ changes, ensuring that the narrative of the commit aligns with the actual modifications made.

.. image:: /images/chatgpt_patchset_review_2_highlighted.png
    :width: 1200

Interactive Assistance
----------------------

ChatGPT goes beyond being just a tool, acting more like a virtual colleague. It’s ready to respond to user inquiries, offering suggestions, and clarifying any doubts. This function is akin to having an additional team member, one that’s always available to provide insights and clarifications, much like a knowledgeable human peer.

The ability to start conversations with ChatGPT directly from an inline comment adds a layer of dynamism to the interaction. Users can request reviews on specific parts of the code, extending even beyond the current PatchSet, or ask for improvement suggestions. This feature essentially brings an on-demand, AI-powered code review assistant into the workflow, available at the click of a button.

In the following example, the author inquires further about implementing a change recommended by ChatGPT within the code of Gerrit ChatGPT plugin project itself, showcasing the feature’s interactive and responsive capabilities.

.. image:: /images/chatgpt_interactive_assistance_cropped.png
    :width: 1200

In the example showcased next, ChatGPT is queried about a different implementation approach on a code segment that **isn’t directly related to the changes** in the PatchSet.

.. image:: /images/chatgpt_query_min.png
    :width: 600

Adjusting Verbosity Level
-------------------------

The verbosity level can be further increased by specifically requesting multiple alternatives and code examples.

.. image:: /images/chatgpt_query_max.png
    :width: 600

Security and Privacy
--------------------

Last but certainly not least, we give utmost importance to security and privacy.

Recognizing scenarios where code confidentiality is paramount, we’ve introduced a new configuration option (``gptFullFileReview``) which, when set to false, restricts the code reviewed by ChatGPT to only the changes made, without including the entire file. This feature provides peace of mind, ensuring that sensitive information remains within the confines of the organization, thus safeguarding intellectual property and adhering to privacy standards.

Conclusion
----------

Our exploration of the integration of ChatGPT into Gerrit has highlighted several key points:

* **Innovative Integration**: We’ve discussed the groundbreaking integration of ChatGPT into a Gerrit plugin, showcasing how it acts not just as a tool but as a virtual collaborator in the development process.
* **Control and Customization**: We emphasized the importance of control, allowing Gerrit administrators to selectively activate ChatGPT for specific projects, users, groups, and topics. This ensures that ChatGPT’s insights are relevant and aligned with the developers’ needs.
* **Interactive and Responsive Nature**: The feature that allows developers to continue conversations based on initial insights or start new ones independently showcases the interactive and responsive nature of the plugin.

By integrating ChatGPT into Gerrit, we aim to enhance code quality, streamline project management, and introduce AI-driven intelligence into the software development lifecycle. This integration is a step towards a more efficient, collaborative, and intelligent coding environment, highlighting our commitment to innovation and excellence in software development.
