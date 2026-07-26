================================
ReviewAI Gerrit Plugin
================================

.. note:: **TL;DR**
   - **ReviewAI is a Gerrit plugin by Amarula Solutions** that brings AI-powered code review to the Gerrit change page through a sidebar chat interface, supporting automatic Patch Set reviews, follow-up conversations, and multiple AI provider backends.
   - Licensed under **Apache 2.0**, supporting OpenAI, DeepSeek, Gemini, Ollama, and MoonShot via LangChain, with specialized review agents for correctness, testability, code quality, documentation, and security.

.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

What is ReviewAI?
-------------------

`ReviewAI <https://github.com/amarula/reviewai-gerrit-plugin>`__ is an
Apache 2.0-licensed Gerrit plugin that integrates an AI-powered code
review assistant directly into the Gerrit UI. It provides a sidebar
chat interface on the change page where developers can ask questions
about Patch Sets, trigger automatic reviews, and maintain per-review
conversation history.

Originally forked from `xielong/chatgpt-code-review-gerrit-plugin
<https://github.com/xielong/chatgpt-code-review-gerrit-plugin>`__,
Amarula Solutions has evolved it into a multi-provider, multi-agent
review platform with 587+ commits of development.

**Multi-Provider Backend**

  ReviewAI supports multiple AI providers through LangChain:
  **OpenAI**, **DeepSeek**, **Google Gemini**, **MoonShot**, and
  **Ollama** (local, self-hosted). Users select provider and model
  combinations from a sidebar dropdown. Tokens are configured
  per-provider and can be stored in Gerrit's ``secure.config``.

**Specialized Review Agents**

  Three agent modes provide increasing sophistication:

  - **Single Agent** — one AI reviewer evaluates the entire Patch Set
  - **Scoped Agents** — separate agents for code changes and commit
    messages
  - **Specialized Agents** — dedicated agents for correctness,
    testability, code quality, documentation, and security (from
    the Sashiko project)

**On-Demand Code Context**

  When configured, the AI can request repository context via tool
  calls: file listing, reference search, and file reading —
  providing deeper understanding beyond just the patch diff.

How It Works
---------------

#. A Patch Set is submitted to Gerrit.
#. ReviewAI formats the changed code with configurable context lines
   and sends it to the selected AI provider.
#. The AI returns a structured JSON response parsed into Gerrit
   comments (patch-set-level and inline).
#. A ``Code-Review`` vote is optionally cast.
#. Developers can continue the conversation via Gerrit comments by
   mentioning the AI user (``@{gerritUserName}``) or through the
   sidebar chat.

ReviewAI also supports **topic-aware review** — grouping related
Patch Sets by topic for a unified AI review across a series.

Features at a Glance
----------------------

.. list-table::
   :header-rows: 0
   :widths: 35 65

   * - **Sidebar Chat**
     - Full conversation interface embedded in the Gerrit change page
   * - **Automatic Review**
     - AI reviews every Patch Set on submission, posting comments
       and optionally casting votes
   * - **Slash Commands**
     - ``/review``, ``/help``, ``/suggest`` (generates Gerrit
       suggested edits), ``/forget_thread``, ``/configure``,
       ``/show``, ``/directives``
   * - **Multi-Provider**
     - OpenAI, DeepSeek, Gemini, MoonShot, Ollama via LangChain
   * - **Model Selection**
     - Select provider/model from the sidebar dropdown
   * - **Specialized Agents**
     - Correctness, testability, code quality, documentation,
       security agents from the Sashiko project
   * - **Directives System**
     - Mandatory plain-English review instructions, configurable
       globally, per-project, or dynamically
   * - **Comment Filtering**
     - Relevance-based filtering of AI comments with configurable
       threshold (default 0.6)
   * - **Code Context**
     - ``ON_DEMAND`` mode lets the AI request repository context
       via tool calls (file listing, reference search, file reading)
   * - **ZDR Mode**
     - Zero Data Retention for OpenAI — uses local plugin memory
       instead of server-side conversation storage
   * - **Secure Config**
     - API tokens stored in ``secure.config`` with optional
       encryption

.. figure:: /images/reviewai-sidebar.png

    ReviewAI sidebar chat interface embedded in the Gerrit change page

.. figure:: /images/reviewai-sidebar-review.png

    AI-generated Patch Set review results with inline comments

.. figure:: /images/reviewai-sidebar-model_dropdown.png

    Provider and model selection from the sidebar dropdown

.. figure:: /images/reviewai-sidebar-message_reply.png

    Follow-up conversation through the ReviewAI sidebar

.. figure:: /images/reviewai-gerrit_change_log-review.png

    AI comments and Code-Review vote visible in the Gerrit change log

Getting Started
-----------------

Requirements
~~~~~~~~~~~~~

- **JDK 21** and **Bazel** (Bazelisk recommended)
- **Gerrit** compatible with the plugin's Bazel external deps
- API tokens for at least one AI provider

Build from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    git clone https://github.com/amarula/reviewai-gerrit-plugin.git
    cd reviewai-gerrit-plugin

    # Link into a Gerrit checkout
    cd gerrit/plugins
    ln -s /path/to/reviewai-gerrit-plugin .

    # Build
    cd ../..
    bazelisk build plugins/reviewai-gerrit-plugin:reviewai-gerrit-plugin

    # Development build (includes admin/debug features)
    bazelisk build plugins/reviewai-gerrit-plugin:reviewai-gerrit-plugin-dev

Installation
~~~~~~~~~~~~~

Upload the built JAR to ``$gerrit_site/plugins/`` and restart Gerrit.

Configuration
~~~~~~~~~~~~~~~

Set up in ``$gerrit_site/etc/gerrit.config`` under
``[plugin "reviewai-gerrit-plugin"]``:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Parameter
     - Description
   * - ``gerritUserName``
     - Gerrit username of the AI bot user (required)
   * - ``aiTokens``
     - Provider tokens, e.g. ``OpenAI/{key}``, ``Gemini/{key}``
   * - ``aiProviders``
     - Provider routes to expose (default: ``OpenAI``)
   * - ``aiModels``
     - Specific model routes by provider
   * - ``aiReviewPatchSet``
     - Enable automatic review (default: ``true``)
   * - ``enabledVoting``
     - Allow AI to cast Code-Review votes (default: ``false``)
   * - ``agentSpecializationLevel``
     - ``SINGLE_AGENT``, ``SCOPED_AGENTS``, or ``SPECIALIZED_AGENTS``
   * - ``maxReviewLines``
     - Max lines included in review (default: ``1000``)
   * - ``codeContextPolicy``
     - ``NONE`` or ``ON_DEMAND`` (default: ``NONE``)
   * - ``enabledFileExtensions``
     - File types to include in reviews
   * - ``directive``
     - Mandatory review instructions (repeatable)

For the complete configuration reference, see the `README
<https://github.com/amarula/reviewai-gerrit-plugin#readme>`__.

Key Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Purpose
   * - ``aiDomain``
     - Custom API endpoint (overrides provider defaults)
   * - ``aiReviewTemperature``
     - Temperature for Patch Set reviews (default: 0.2)
   * - ``aiReviewCommitMessages``
     - Also review commit messages (default: true)
   * - ``patchContextLines``
     - Context lines around changes (default: 3)
   * - ``aiMaxMemoryTokens``
     - Max tokens in conversation memory (default: 16K)
   * - ``ollamaDomain``
     - Ollama server endpoint (default: ``http://localhost:11434``)
   * - ``commentRelevanceThreshold``
     - Minimum relevance score for AI comments (default: 0.6)

Testing
~~~~~~~~~

.. code-block:: none

    bazelisk test plugins/reviewai-gerrit-plugin:reviewai_tests
    bazelisk test plugins/reviewai-gerrit-plugin:reviewai_tests \
      plugins/reviewai-gerrit-plugin:reviewai_dev_tests

Why Amarula Maintains This
----------------------------

Amarula Solutions runs Gerrit-based code review across all development
workflows — from embedded Linux BSPs and kernel drivers to Jenkins
pipelines and Flutter applications. ReviewAI reduces review latency,
catches issues early, and provides a consistent first-pass analysis
before human reviewers engage.

The plugin has been extensively tested in production environments and
evolved through real-world feedback into a mature, multi-provider AI
review platform.

License and Attribution
-------------------------

- **License:** Apache License, Version 2.0
- **Repository:** `amarula/reviewai-gerrit-plugin <https://github.com/amarula/reviewai-gerrit-plugin>`__
- **Upstream:** Forked from `xielong/chatgpt-code-review-gerrit-plugin <https://github.com/xielong/chatgpt-code-review-gerrit-plugin>`__

.. tip::
   Want AI-powered code review in your Gerrit workflow? Amarula Solutions
   provides ReviewAI deployment, custom directive configuration, and
   multi-provider AI integration for on-premise Gerrit instances.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
