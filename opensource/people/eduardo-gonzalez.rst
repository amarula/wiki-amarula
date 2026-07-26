.. ============================================================================
   Eduardo Gonzalez — Profile page for Amarula Solutions' open source contributor
   directory. Data sourced from amarulasolutions.com/team/eduardo-gonzalez-lazo
   and the monthly contribution reports in opensource/reports/.
   ============================================================================

=====================
Eduardo Gonzalez
=====================

.. image:: /images/people/eduardo-gonzalez.png
   :align: right
   :width: 220

**Role:** Embedded Software Engineer

**Location:** Trieste, Italy

**Education:** PhD in Statistical Physics, SISSA (Scuola Internazionale
Superiore di Studi Avanzati)

|

Eduardo studied Physics for most of his life before transitioning to
embedded software engineering through self-learning and hands-on
projects. With a PhD in Statistical Physics from SISSA, he brings a
rigorous analytical mindset to embedded systems development.

At Amarula, he specializes in **cross-platform C++ application
development** using **CMake** build systems and **C++/QML** for
embedded interfaces. He is the primary maintainer of
**libcppconnman**, Amarula's open-source C++ wrapper for the ConnMan
network manager, where he leads CI/CD workflows, testing
infrastructure, and API design. He is actively growing his expertise
in **Yocto**, embedded Linux, and team collaboration practices.

|

----

Open Source Focus
=================

**libcppconnman (Primary Maintainer)**
  Eduardo is the lead developer and maintainer of libcppconnman, a C++
  wrapper library for the ConnMan network management daemon used in
  embedded Linux systems. He has driven significant architectural
  improvements: migrating to GLib main loop integration with
  ``g_main_context_invoke``, implementing thread-safe non-blocking
  proxy and agent APIs, and eliminating memory leaks in the GDBus
  interface layer. He established the CMake-based build system with
  proper version and SOVERSION handling, enforced static linking for
  Google Test, and added comprehensive unit and integration tests.

**CI/CD & Developer Experience**
  Created GitHub Actions workflows for code formatting checks,
  build-and-test automation (``conf-build-test.yml``), and post-build
  result reporting. He fixed Clang compilation warnings and improved
  logging throughout the codebase, making the library easier to debug
  and integrate.

**ConnMan Integration**
  Extended ConnMan's C++ API surface with tethering test support,
  ConnMan service property accessors, and readline-based interactive
  control (``connmanctl``). His work on non-blocking agent
  registration and D-Bus thread safety ensures libcppconnman is safe
  for use in multi-threaded embedded applications.

**Embedded Linux**
  Currently expanding into Yocto-based BSP development and embedded
  Linux system integration, complementing his C++ and build-system
  expertise.

|

----

Selected Contributions (2025–2026)
====================================

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Contribution
     - Project / Area
   * - GLib main loop integration via g_main_context_invoke
     - libcppconnman
   * - Non-blocking agent registration (gagent + gproxy)
     - libcppconnman
   * - Thread-safe GDBus proxy and service manager
     - libcppconnman
   * - CMake VERSION + SOVERSION for library releases
     - libcppconnman
   * - Google Test static linking and CI test infrastructure
     - libcppconnman
   * - Memory leak fix in GConnMan D-Bus proxy
     - libcppconnman
   * - ConnMan tethering test suite (gconnman_tech_test)
     - libcppconnman
   * - Clang compilation warning cleanup
     - libcppconnman
   * - GitHub Actions: conf-build-test.yml and code-format.yml
     - CI/CD
   * - ConnMan service property accessors and readline connmanctl
     - ConnMan / libcppconnman

|

Beyond the Code
===============

When not debugging D-Bus threading issues or writing CMake rules,
Eduardo enjoys swimming, running, and playing guitar. His physics
background gives him a distinct perspective on system-level
debugging — approaching complex embedded problems with the same
analytical rigor he applied to statistical physics at SISSA.

|

.. tip::
   Need a C++ library for ConnMan integration or embedded networking
   support? Amarula Solutions provides custom library development,
   CMake/CI pipeline design, and ConnMan/Yocto integration.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
