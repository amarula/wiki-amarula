====================================================================
A Roadmap for Newbies: Tackling Unknown Tasks in Embedded Linux
====================================================================

.. note:: **TL;DR**
   A case-study presentation by **Annachiara Gallo** (Amarula Friday,
   April 2026) on the iterative methodology for tackling unfamiliar
   embedded Linux tasks, covering DNS resolution, mDNS, SSL certificate
   generation, hostapd/dnsmasq testing, and the real bottleneck of
   hardware verification.

`Download the slides (PDF) <../../../_static/roadmap-for-newbies-annachiara-gallo-2026.pdf>`__
(Licensed under Creative Commons BY-SA 3.0)

.. raw:: html

    <br>


What Is This About?
--------------------

Every junior engineer has been there: you're assigned a task in a codebase
you barely know, on a topic you've never studied, involving protocols and
tools you've only heard of. Where do you even start?

Annachiara Gallo's **Amarula Friday** presentation tackles this question
head-on through a real client task — **Acme Task 139** — and walks
through the complete lifecycle from initial confusion to working
implementation, documenting the process and the bottlenecks along the way.

The Task
~~~~~~~~

The starting point: an embedded device running a WiFi-connected HTTPS
server at ``https://bebeep.local``, with mDNS for service discovery and
self-signed SSL certificates. The client wants to add **subdomain
support** — they need ``https://api.bebeep.acme.local``,
``https://www.bebeep.acme.local``, and arbitrary subdomain queries
to all resolve correctly.

What sounds like a small feature request quickly exposes a cascade of
hidden requirements.

.. raw:: html

    <br>

The Iterative Method
======================

The presentation structures the work as a repeating cycle of five phases,
shown through two complete iterations:

Iteration 1 — First Pass
--------------------------

**1. Expand requirements.** What was left unsaid? The board needs a
sequential hostname per device, a fallback mechanism, an AT command to
reset the hostname, and changes to certificate generation.

**2. Narrow the field of interest.** Without a defined scope, you drown
in information. Identify your assumptions. What do you actually need to
know? In this case: Windows DNS resolution quirks, multi-label query
behavior, and what causes the browser to reject the current certificate.

**3. Gather information and validate hands-on.** Key findings:

   - Windows handles ``.local`` queries in a **non-standard way** for
     historical reasons.
   - Multi-label queries may not be resolved by mDNS even when ending
     with ``.local``.
   - The ``.local`` TLD is not recommended for anything other than
     mDNS queries.
   - Since 2015, SSL certificates **must be signed by a CA** for the
     browser to accept them.
   - Browsers reject certificates unless the hostname is listed inside
     the **Subject Alternative Name (SAN)** extension.

**4. Decide the course of action.** This is where inexperience hits
hardest. Evaluate the options yourself first, then present them to a
senior with your analysis. Do you remove mDNS or keep it? What should
the fallback hostname be?

**5. Development has its own iterations.** Development isn't just coding —
it's investigation, debugging, rethinking logic, unit testing, on-device
testing in both AP and STA modes, code review, and small incremental
commits. The most time-consuming part? Not the code itself, but
**verification on physical hardware**.

Iteration 2 — Going Deeper
----------------------------

With the first pass complete, new implicit requirements emerge:

- **Certificates**: set up a CA to sign them instead of self-signing.
- **Windows installation**: must be user-friendly (``.bat`` installer).
- **Host discovery**: with mDNS removed, how does the board announce
  itself on the network?

The investigation phase now focuses on **custom DNS responder
implementation** — studying protocol structure, compression pointers,
and learning from reference implementations like the ESP-IDF
``dns_server.c`` example.

.. note::

   **Watch out for compression pointers.** DNS message compression uses a
   two-octet pointer where the two most significant bits are set to 1
   and the remaining 14 bits are the offset. If not handled correctly,
   these pointers can cause **infinite loops** in your resolver.

**Network testing** spans two modes:

- **STA Mode**: set up an AP with ``hostapd`` and DNS forwarder with
  ``dnsmasq``, assign IPs, verify reachability.
- **AP Mode**: the device serves as the access point — the custom DNS
  server must handle all queries locally.

.. raw:: html

    <br>

The Real Bottleneck
--------------------

The presentation concludes with a striking observation: **the primary
bottleneck was verification on physical hardware, not logic development**.
This is a universal truth in embedded Linux engineering that junior
developers need to internalize early: working with real devices, real
network configurations, and real clients takes far more time than
reading documentation or writing code.

.. raw:: html

    <br>

Why Document Everything?
--------------------------

Annachiara closes with three compelling reasons:

#. **Recording motivations.** Explaining why specific choices were made
   prevents others — and your future self — from wasting time. The client
   needs to understand the reasoning behind network configuration
   requirements and installation steps.

#. **Recycling spent effort.** Common IoT patterns (browser warning
   fixes, DNS resolution, certificate generation) repeat across projects.
   Each time you solve one, document it so it's solved for the team.

#. **Future-you will thank you.** Will you remember all the logic behind
   your choices six months from now? Or will you waste time second-guessing?
   Spoiler: the second one.

.. raw:: html

    <br>

Key Takeaways for Junior Engineers
------------------------------------

- **Start narrow.** Scope your investigation before diving into documentation.
- **Validate assumptions hands-on.** Windows DNS behavior, mDNS quirks,
  browser certificate policies — nothing behaves exactly as the spec says.
- **Present options, not problems.** Evaluate yourself first, then bring
  structured choices to senior engineers.
- **Hardware is always the bottleneck.** Budget 2-3x your code-time
  estimate for on-device testing.
- **Small, incremental commits.** Each working step is a checkpoint you
  can return to.
- **Document as you go.** Motivations, dead ends, and testing procedures
  are as valuable as the final code.

.. raw:: html

    <br>

.. tip::
   Amarula Solutions runs regular internal knowledge-sharing sessions
   (Amarula Friday) and provides mentorship for junior embedded Linux
   engineers. Interested in joining our team or learning more about our
   training programs?
   `Contact us <https://www.amarulasolutions.com/contact/>`_
