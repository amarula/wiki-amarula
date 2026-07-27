.. ============================================================================
   Patrizio Gelosi — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from amarulasolutions.com/team/patrizio-gelosi and
   the monthly contribution reports in opensource/reports/.
   ============================================================================

===============
Patrizio Gelosi
===============

.. image:: /images/people/patrizio-gelosi.jpg
   :align: right
   :width: 220

**Role:** Senior Software Developer

**Education:** Master's Degree in Software Engineering, University of Pisa (1999)

|

Patrizio is a software engineer by profession and by passion. With a
Master's degree from the University of Pisa and over two decades of
industry experience, he has worked across the full spectrum of software
development — from large corporate environments at **Telecom Italia**
and **Vueling Airlines** to founding and running his own ventures
(**Dispage**, **3nce**, **HandyContract**).

His project portfolio spans natural language processing engines, image
processing platforms (2D and 3D), document processing systems for both
digital and scanned documents, HTML graphic editors, and web application
plugins for CRM and CMS platforms. Since joining Amarula, he has become
the **lead developer of the ReviewAI Gerrit Code Review plugin**,
driving its evolution from an experimental AI integration into a mature,
production-grade code review tool.

|

----

Open Source Focus
=================

**ReviewAI Gerrit Plugin (Lead Developer)**
  Patrizio is the primary developer of Amarula's flagship open source
  product, the ReviewAI Gerrit Code Review plugin. He led the migration
  from OpenAI's deprecated Assistants API to the official Responses API,
  integrated ReviewAI with the Gerrit Review Agent sidebar, and
  centralized provider transport through LangChain for OpenAI, Gemini,
  DeepSeek, MoonShot, and Ollama. His work includes configurable
  single-agent, scoped-agent, and specialized-agent (Sashiko-inspired)
  review modes; topic-wide analysis; AI-generated review suggestions;
  and targeted repository exploration under the ON_DEMAND policy using a
  limited set of basic commands.

**Key Technical Achievements**
  - Migration from OpenAI Assistants API to the Responses API
  - Gerrit Review Agent sidebar integration with private per-user
    conversations
  - Configurable single, scoped, and specialized AI review workflows
  - Sashiko-inspired Level 2 agent orchestration and final review
    synthesis
  - Topic-wide reviews across related Gerrit changes
  - AI-generated suggestions for patch sets and commit messages
  - Query-driven ON_DEMAND code retrieval with ``tree``, ``get_content``,
    and ``grep``
  - Multi-provider LangChain transport and dynamic model configuration
  - Database-backed conversation storage and multi-conversation patch-set
    history
  - Per-provider and per-model AI cost tracking through telemetry
  - Gerrit permission gating, custom AI administrator groups, and
    admin-only tooling

**DevOps & CI**
  Contributes to build system maintenance, version bumping, and
  compatibility testing across Gerrit versions, ensuring the plugin
  works reliably in production environments.

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project
   * - Migration from Assistants API to official OpenAI Responses API
     - ReviewAI Gerrit Plugin
   * - Parallel AI review processing across multiple patch files
     - ReviewAI Gerrit Plugin
   * - Gerrit Review Agent sidebar integration with provider and model
       selection
     - ReviewAI Gerrit Plugin
   * - Adoption of the Sashiko workflow for Level 2 specialized agents
     - ReviewAI Gerrit Plugin
   * - AI-generated review suggestions for patch sets and commit messages
     - ReviewAI Gerrit Plugin
   * - Query-driven ON_DEMAND code context retrieval
     - ReviewAI Gerrit Plugin
   * - LangChain transport for OpenAI, Gemini, DeepSeek, MoonShot, and Ollama
     - ReviewAI Gerrit Plugin
   * - Per-provider and per-model AI cost tracking in telemetry
     - ReviewAI Gerrit Plugin
   * - Separate production and development builds with Bazel in-tree support
     - ReviewAI Gerrit Plugin
   * - Gerrit/plugin prompt harmonization and configurable review scoring
     - ReviewAI Gerrit Plugin

|

Beyond the Code
===============

Patrizio has been passionate about **mathematics and physics** since
childhood. During college he combined these interests with programming,
building a simulation where a population of programs in a
bidimensional programming language could spontaneously evolve. He
plays the **piano** in his spare time, with a particular fondness for
pieces by **Chopin** and **Beethoven**.

|

.. note::
   This profile is part of the :doc:`Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Interested in AI-assisted code review or want to integrate ReviewAI
   into your Gerrit workflow? Amarula Solutions provides plugin
   deployment, customization, and commercial support for the ReviewAI
   Gerrit plugin.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
