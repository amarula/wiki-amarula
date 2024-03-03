Update ChatGpt Gerrit plugin to version 2.1.0
============================================================

.. figure:: /images/chatgpt-news.png
   :align: center
|
|
Amarula Solutions S.R.O updates the https://amarula.github.io/chatgpt-code-review-website/ to version 2.1.0

**Major updates:**

* Introduced voting capability, allowing ChatGPT to assign a score to the Change Sets.
* Implemented comment visibility filtering based on scores, with a default focus on displaying negative feedback, customizable to user preference.
* Transitioned to treating Patch Set review comments as separate entities, moving away from compiling them into a single list.
* Implemented a complete lifecycle for review comment resolution. Each comment starts from an unresolved state, with options for users to agree, discuss alternatives, or dispute ChatGPT's suggestions, influencing the Change Set score.
* Blocked the display of duplicate and conflicting comments.
* Enabled processing of commands via comments. Command `/review` triggers full Change Set reviews and `/review_last` targets the latest Patch Set.

**Behavior change:**
* Reviews of commit messages are now enabled by default.

**Minor changes and fixes:**

* Excluded WIP Change Sets from automated review.
* Fine-tuned the temperature settings differentiating between comment queries and Patch Set reviews.
* Reduced the size of the message history data payload.
* Fixed rendering issues of ChatGPT comments in the Gerrit UI.
* Fixed various issues with detecting code snippets in ChatGPT responses.
* Fixed review posting issue with out-of-bounds line numbers from ChatGPT.

Stay tuned!
https://www.amarulasolutions.com/quotation/
