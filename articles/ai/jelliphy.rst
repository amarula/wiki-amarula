Jelliphy - AI Framework for Interactive Web Application Development
#####################################################################
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


Overview
********

Jelliphy is a **No-Code Browser-Based Framework** that integrates the **ChatGPT** API into your **Git-hosted** web application.

Jelliphy connects directly with your live user interface, enabling interaction with ChatGPT as you work within your web application:

- Annotate change requests on the page using freehand notes; Jelliphy captures these and submits them to ChatGPT to produce the relevant code patches.

- Select UI elements and describe intended modifications in natural language. Jelliphy uses ChatGPT to generate precise code patches, applies them to your repository, and updates the browser view immediately.

- Make graphic edits to UI components within the application; Jelliphy converts these actions into natural-language prompts for ChatGPT.

- Use freehand sketching to specify change requests, which Jelliphy forwards to ChatGPT for code patch generation (feature in progress).

This tool is designed to streamline the development process, making it easier to implement changes and collaborate with team members.

Architecture
************

Jelliphy operates as middleware between your browser and the ChatGPT API:

1. **Request Generation**: Translates user interactions into structured prompts sent to ChatGPT.
2. **Patch Application**: Receives patches from ChatGPT, applies it to the Git repository, and updates the page view.

.. figure:: /images/jelliphy-intro_1.png
   :alt: Jelliphy UI workflow

Key Benefits
************

- **Visual Interaction**: Directly click or draw on UI elements to initiate change requests.
- **Automated Patching**: Natural-language descriptions are converted into Git-diff patches.
- **Version Control**: All edits are committed through Git, ensuring traceability and easy rollback.
- **Collaborative Workflow**: Organize change requests either together or in parallel, enhancing team collaboration while optimizing performance.

.. figure:: /images/jelliphy-intro_2.png
   :alt: Collaborative Workflow

   Collaborative Workflow

Modes of Operation
******************

Jelliphy offers multiple modes to facilitate interaction with ChatGPT:

Navigation Mode
---------------

This default mode permits safe exploration of the application without generating any requests.

.. figure:: /images/jelliphy-intro_3.png
   :alt: Navigation mode

   Navigation mode

Pin Notes Mode
--------------

Add free-floating or element-pinned notes to specify desired changes in context-rich conversation threads, enabling

* ChatGPT to request clarifications, and

* You to iteratively refine the request.

.. figure:: /images/jelliphy-intro_4.png
   :alt: Free-floating pin notes

   Free-floating pin notes

.. figure:: /images/jelliphy-intro_4.1.png
   :alt: Element-pinned notes

   Element-pinned notes

Edit Mode
---------

Provides graphic transformation tools to manipulate UI components directly:

Edit Mode includes several sub-modes to facilitate different types of UI modifications:

- **Handle Mode**: Enables graphical transformations such as repositioning elements (moving them within the DOM or offsetting their position), resizing, editing text, aligning, and removing elements.
- **Properties Mode**: Allows modification of any CSS property, including font, text, color, shadow, positioning, box model (padding, margin, border), and more.
- **Area Mode**: Lets you select multiple elements within a defined area. You can also add or remove elements from the selection using standard Shift and Ctrl keys.
- **Eyedropper**: Lets you pick any color from the UI for use in subsequent change requests.
- **Paint**: Applies the currently selected foreground and background colors to the selected elements.
- **Table**: Provides tools for managing tables, such as adding or removing rows and cells.
- **Add**: Enables insertion of new elements into the page.


.. figure:: /images/jelliphy-intro_5.png
   :alt: Reposition elements

   Reposition elements

.. figure:: /images/jelliphy-intro_5.1.png
   :alt: Resize elements

   Resize elements

.. figure:: /images/jelliphy-intro_5.3.png
   :alt: Change element properties

   Change element properties

.. figure:: /images/jelliphy-intro_5.2.png
   :alt: Quick-Edit Content

   Quick-Edit Content

Workflow Strategies
*******************

Combined vs. Parallel Requests
------------------------------

- **Combined Requests**: Group multiple edits into a single prompt, generating one cohesive patch for related changes.
- **Parallel Requests**: Submit each edit separately to ChatGPT, applying independent patches as soon as they’re ready.

  This is ideal for large-scale projects where multiple developers are working on different features simultaneously.

.. figure:: /images/jelliphy-intro_7.png
   :alt: Parallel requests pipeline

   Parallel requests pipeline

Patch Application and Review
----------------------------

Once you have finalized your notes or transformations, click **Apply** to submit your requests. ChatGPT will generate the relevant patches, which are then applied to your project and immediately reflected in the browser.

.. figure:: /images/jelliphy-intro_8.png
   :alt: Patch Generation and Application process

   Patch Generation and Application process

Sketch Mode (WIP)
******************

Sketch Mode enables you to draw directly on the page. Jelliphy converts your sketches into image prompts for ChatGPT, which interprets them to generate relevant code changes.
This feature is currently under development and is intended to offer a more intuitive method for specifying design modifications.

.. figure:: /images/jelliphy-intro_9.png
   :alt: Sketch Mode Drawing

   Sketch Mode Drawing

Notes and Considerations
***********************

- Ensure your Git working directory is clean before applying patches to avoid merge conflicts.
- Select Combined Patches for atomic feature overhauls and Parallel Patches for simultaneous independent tweaks.
- Test the generated patches in a staging environment before deploying to production.
- Regularly review and refine your prompts to improve the quality of generated patches.
- Consider using a dedicated branch for Jelliphy-generated patches to maintain a clean commit history.
- Monitor the performance of Jelliphy and ChatGPT to ensure optimal response times and accuracy.
- Stay updated with the latest Jelliphy releases for new features and improvements.
- Provide feedback on the Jelliphy GitHub repository to help improve the tool.
- Experiment with different prompt styles to find the most effective way to communicate your desired changes to ChatGPT.
- Leverage Jelliphy's collaborative features to enhance team communication and project management.
- Use Jelliphy in conjunction with other development tools to streamline your workflow and improve productivity.
- Share your experiences and success stories with Jelliphy in the developer community to inspire others.
