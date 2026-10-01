The Workshop Upstream Manifesto: Prague Edition
================================================

.. note:: **TL;DR**
   - The second edition of **The Workshop Upstream Manifesto** takes place at our Prague office on **October 1-2, 2026** — a hands-on open source workshop on **mainline-first embedded development**.
   - Mentored by Amarula senior engineers and special guest **Michael Opdenacker** (rootcommit). The challenge is defined together during the workshop, and the deliverable is a real **upstream contribution**.

.. figure:: /images/workshop-prague-collaboration.jpg
   :alt: Root Commit and Amarula Solutions — a powerful collaboration

.. epigraph::

   "If it's not in mainline, it's technical debt."

**Location** Prague, Czech Republic — in our office

**Date** October 1-2, 2026

Why a second edition?
---------------------
The first edition, held in Carpi in May 2026, proved the format works: put
engineers in a room with an unsupported board, a mainline tree, and a mailing
list — and let them find out how much of the work is really upstreamable.
See `The Workshop Upstream Manifesto <workshop.html>`_ for the full story and
the challenges we ran there.

**Michael Opdenacker's team won the last edition** on two counts: they sent the
most contributions upstream, and they ended the two days with running, working
hardware. Merged or not was never the measure — that call belongs to the
maintainers and takes longer than the workshop lasts.

That is the bar the Prague teams have to beat, and the title is up for grabs
again.

The Prague edition is not a replay. It is the same workshop, with a different
room, different hardware, and a different challenge to define.

Which challenge will we pick this time?
---------------------------------------
That is exactly the point: we do not know yet, and that is the honest answer
this early. The challenge is defined *during* the workshop, by the people in
the room, once we see the boards on the table and check what mainline already
supports.

What is fixed is the method:

* Pick a target we can actually reach in two days — a board, a driver, a
  subsystem, a piece of firmware tooling.
* Check the real state of mainline first, instead of assuming.
* Write the code, break it, fix it.
* Leave with a patch series on a public mailing list.

Which principles do we bring to Prague?
---------------------------------------
The manifesto travels with us, unchanged:

No Vendor Crap
    We don't care about a "working" 4.4 kernel from a chip vendor. If it's not in
    mainline, it's technical debt. *(We have a bit of experience here).*

The Junior Drives
    Senior, put your hands in your pockets. If you're typing, you're failing.
    The Junior writes the code; you explain the *why*.

Break It to Fix It
    You don't learn from a successful build. You learn from the kernel panic
    and the ``bitbake`` error log.

The Mailing List is the Goal
    A hackathon project that stays on a laptop is a waste of electricity.
    The goal is ``git format-patch``.

Keep it Simple
    Don't over-engineer. Use the framework the community already built.

Who mentors the workshop?
-------------------------
Amarula senior engineers, with `Michael Opdenacker
<https://rootcommit.com/about/michael-opdenacker/>`_ joining again as special
guest and Senior mentor.

Where does the workshop take place?
-----------------------------------
The Prague edition is hosted in our own office, the same way the Carpi edition
was:

| Amarula Solutions s.r.o.
| Pekařská 628/14
| 155 00 Praha 5-Jinonice
| Czech Republic

**Phone** +420 212 245 723

The teams
---------

**Michael Opdenacker** team:
- Jennifer Chukwu
- Peter Janicka

**Michael Trimarchi** team:
- Roman Smrz
- Giacomo Trimarchi

The challenges
--------------

Team Michael Opdenacker proposal:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contribute to Yocto by reviewing, testing and pushing patches submitted
to the openembedded-core mailing list by the Auto Upgrade Helper.

Also investigate update failures, fix them (adapting the OE core recipes)
and pushing them upstream.

Target: 20 patches sent upstream!


Team Michael Trimarchi proposal:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upstream in linux kernel pcm1795 and pcm1796 starting from a 2018 contribuition from Michael Trimarchi. Upstream
rockchip rga fix to mainline. Upstream pmic changes in uboot on nxp chipset. Upstream Velp imx6dl board from BGM
elettronica.

.. note::
   This page is a live announcement: as the Prague challenges get defined and
   the patches go out, we will report the results here — the same way we
   followed up on the `first edition <workshop.html>`_.

.. tip::
   A hackathon project is only as good as its last upstream contribution.
   Interested in future workshops or embedded Linux training?
   Amarula Solutions offers custom on-site and remote training in Yocto,
   U-Boot, Linux kernel, and Buildroot.
   `Contact us about training <https://www.amarulasolutions.com/contact/>`_
