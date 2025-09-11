Update ChatGpt Gerrit plugin to version 3.1.0
============================================================

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
