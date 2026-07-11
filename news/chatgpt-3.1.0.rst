Update ChatGpt Gerrit plugin to version 3.1.0
=============================================

.. note:: **TL;DR**
   - Version 3.1.0 of the **ChatGPT Gerrit Code Review plugin** adds **Gerrit 3.12.2 support** and a new **ON_DEMAND code context policy** — fetching only the minimal code artifacts requested by the model instead of uploading the entire repository.
   - Supported languages for on-demand context: **Python, C, Java, Kotlin**.

.. figure:: /images/chatgpt-news.png
   :align: center
|
|
Amarula Solutions S.R.O updates the https://amarula.github.io/chatgpt-code-review-website/ to version 3.1.0

**Major updates:**

* Support Gerrit 3.12.2.
* Add ON_DEMAND code context policy as an alternative to UPLOAD_ALL.
  Rather than uploading the complete repository each time, the plugin
  fetches just the minimal set of code artifacts requested by the Model.
  These artifacts can be function signatures, type declarations, or
  similar entities that provide sufficient context for reasoning about the
  change. This selective approach speeds up processing while maintaining
  accuracy in the review.
  Supported langs: python, c, java, kotlin.

**Behavior change:**

* enabledFileExtensions accepts extensions with or without leading dots.

**Minor changes and fixes:**

* Avoid NPE when scanning Git projects by handling missing file tree
    cases.

Stay tuned!
https://www.amarulasolutions.com/quotation/

.. tip::
   Want AI-powered code review integrated into your Gerrit workflow?
   Amarula Solutions develops and maintains the ChatGPT Gerrit plugin and
   offers customization and deployment support.
   `Contact us for a quote <https://www.amarulasolutions.com/quotation/>`_
