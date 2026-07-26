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
  product, the ReviewAI Gerrit Code Review plugin. He has led a
  comprehensive architectural migration from OpenAI's deprecated
  Assistants API to the official Chat Completions API, implemented
  **parallel AI review processing** across multiple patch files, and
  built a modular AI Assistant framework with per-provider model
  configuration. His work on prompt engineering — harmonizing Gerrit
  and plugin-level prompts with default neutral review behavior — has
  made the plugin's output more consistent and actionable for
  developers.

**Key Technical Achievements**
  - Migration from OpenAI Assistants API to Chat Completions API
  - Parallel AI review architecture for multi-file patch sets
  - Centralized function calling and tool definitions
  - Dynamic AI configuration per provider and model
  - Review Agent framework integration for structured output
  - ``/help`` slash command and ``/show`` command result formatting
  - Multi-conversation AI history per patch set
  - Connection error handling and response timeout management

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
   * - Migration from Assistants API to official OpenAI Chat Completions API
     - ReviewAI Gerrit Plugin
   * - Parallel AI review processing across multiple patch files
     - ReviewAI Gerrit Plugin
   * - Review Agent framework integration with structured output
     - ReviewAI Gerrit Plugin
   * - Gerrit/plugin prompt harmonization with default neutral reviews
     - ReviewAI Gerrit Plugin
   * - AI Assistant modularization and central function calling
     - ReviewAI Gerrit Plugin
   * - /help command and /show command result formatting
     - ReviewAI Gerrit Plugin
   * - Multi-conversation AI history per patch set
     - ReviewAI Gerrit Plugin
   * - Per-provider model selection and dynamic configuration
     - ReviewAI Gerrit Plugin
   * - Connection error handling and response timeout extension
     - ReviewAI Gerrit Plugin
   * - Version 4.0.0 bump with compatibility fixes for Gerrit 3.9+
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
   This profile is part of the :doc:`Amarula Solutions Open Source Team directory <index>`.
   Amarula is a larger team; this directory covers only members with public upstream contributions.

.. tip::
   Interested in AI-assisted code review or want to integrate ReviewAI
   into your Gerrit workflow? Amarula Solutions provides plugin
   deployment, customization, and commercial support for the ReviewAI
   Gerrit plugin.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
