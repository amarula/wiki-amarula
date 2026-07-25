Metadata-Driven A/B Firmware Update for STM32MP Platforms
==========================================================

.. note:: **TL;DR**
   - `Pull Request #110 <https://github.com/STMicroelectronics/meta-st-stm32mp/pull/110>`_ on ``meta-st-stm32mp`` introduces a **native, metadata-driven A/B firmware update** implementation for STM32MP15 and STM32MP25 platforms.
   - Unlike ST's existing RAUC-tied approach, this solution uses **FWU metadata and UUIDs** to dynamically identify boot and root partitions — the physical disk layout no longer dictates boot success.
   - Works with **any update manager** (SWUpdate, RAUC, or others), integrates the new ``fwumdata`` U-Boot tool, and includes a ``bootcount.service`` for post-boot bank validation.

|


In embedded Linux systems deployed in the field, reliable firmware updates are not
optional — they are a fundamental requirement. A failed update that bricks a device
means a truck roll, a service outage, or worse. STMicroelectronics' STM32MP platform
has long supported the concept of A/B updates through its ``meta-st-ota`` layer and
associated documentation, but the existing implementation comes with notable
limitations: it is tightly coupled to **RAUC** and relies on a **static position-based
partition scheme**.

`Pull Request #110 <https://github.com/STMicroelectronics/meta-st-stm32mp/pull/110>`_,
authored by **Dario Binacchi** of Amarula Solutions, proposes a fundamentally
different approach: a **metadata-driven** A/B update framework where the boot
workflow is governed by FWU (Firmware Update) metadata, and partitions are identified
by UUIDs rather than by their physical position on the storage medium.

.. image:: /images/update-fwdata.drawio.png

Why Metadata-Driven Matters
----------------------------

The core insight behind this contribution is that firmware update logic should not
need to know *where* a partition lives — only *what* it contains. The FWU metadata
tables, defined by the UEFI FWU specification and supported in U-Boot and TF-A,
already encode this information. By leveraging these tables at runtime, the boot
process becomes:

* **Position-independent**: Partitions are found by ``TYPEUUID`` and ``PARTUUID``,
  so reordering or resizing them does not break the update logic.
* **Update-manager agnostic**: Whether the system uses SWUpdate, RAUC, Mender, or a
  custom updater, the metadata tells U-Boot which bank to boot — no hardcoded
  assumptions.
* **Robust against partial updates**: The bank state field (valid/accepted/invalid)
  is atomically updated in the metadata, while a separate boot counter tracks trial
  attempts and triggers a rollback if the new bank is never confirmed — so an
  interrupted or failing update leaves the system in a known, recoverable state.

Key Technical Contributions
---------------------------

The PR spans **63 files**, adding approximately 3,800 lines of code across the
following layers:

TF-A (Trusted Firmware-A) Patches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New build-flag support (``STM32MP_PSA_FWU_AB_SUPPORT``) enables A/B redundancy at
the secure firmware level. Additional patches introduce extended bootloader and
Linux data partition GUIDs, laying the groundwork for metadata-driven bank
selection at the earliest boot stage.

These TF-A changes have been submitted upstream, successfully reviewed, and
merged into the official Trusted Firmware-A repository [1]_.

U-Boot Patches
^^^^^^^^^^^^^^

A substantial portion of the series (20 patches) covers U-Boot enhancements:

* **Dynamic A/B bank bootup** for both ``stm32mp15`` and ``stm32mp25`` boards —
  U-Boot reads FWU metadata to determine the active bank and locates the
  corresponding partitions by UUID, feeding the correct kernel and rootfs to the
  boot command.
* **FWU platform hooks** for metadata access on STM32MP platforms.
* **UUID-based partition lookup** in the ``part`` command, allowing boot scripts
  to find partitions without relying on device node ordering.

These changes have been submitted upstream, successfully reviewed, and merged
into the official U-Boot repository [2]_ [3]_.

Machine Configuration and WIC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A/B firmware update is enabled via a single ``MACHINE_FEATURES`` flag:

.. code-block:: bash

   MACHINE_FEATURES += "fw-update-ab"

The series adds example WIC kickstart files for A/B SD card layouts on both
``stm32mp257f-ev1`` and ``stm32mp157f-dk2`` boards, with and without a vendor
filesystem partition. Existing WIC files are updated to use PARTUUID-based
identification (``--use-uuid``) for all partitions.

The ``bootcount`` Service
^^^^^^^^^^^^^^^^^^^^^^^^^^

A new ``bootcount`` recipe provides a systemd service that runs after a
successful boot to validate the current bank via the upstream ``fwumdata``
utility. The service updates the bank state in the FWU metadata, marking the
new bank as accepted. This closes the update loop: U-Boot selects and boots the
new bank in trial mode, while userspace confirms the update once the system has
started successfully. At the next reboot, TF-A processes the updated metadata
state and completes the transition from trial to normal boot operation.

The ``fwumdata`` utility represents an important step forward in the FWU
workflow, providing a simple and effective way to update individual FWU
metadata fields at runtime. This differs from the previous ``mkfwumdata``-based
approach, which required regenerating the complete FWU metadata binary for
every change.

This useful contribution was developed and submitted upstream by Kory Maincent
from Bootlin [4]_, and is now part of the official U-Boot project.

Current Status and Roadmap
--------------------------

As of the latest rebase (July 2026), the series is based on **v26.06.10** of
``meta-st-stm32mp``. Key updates in the rebase include:

* Removal of patches already integrated into the new release.
* Replacement of TF-A and U-Boot patches with **backports** of the upstream
  versions (``Upstream-Status: Backport``).
* The ``fw-update-ab`` machine feature is **commented out by default** to
  preserve backward compatibility.

ST has indicated that the series is under review with an internal ticket tracking
analysis and system-test impact. The target is integration into the **v7.0.0
release**, scheduled for November 2026.

Validation
----------

The series has been validated on both supported STM32MP platforms:
the **STM32MP157F-DK2** board for the STM32MP1 family and the
**STM32MP257F-EV1** board for the STM32MP25 family.

In both cases, bank switches were manually triggered to simulate complete
firmware update cycles. The system correctly identified the active bank from
the FWU metadata and mounted the appropriate root filesystem through dynamic
EXTLINUX selection.

Bank switching was performed using the ``fwumdata`` commands shown below:

.. code-block:: bash

   # Switch to bank B
   fwumdata -a 1 -p 0 -s 1 valid

   # Switch to bank A
   fwumdata -a 0 -p 1 -s 0 valid

In both scenarios, U-Boot reads the updated metadata, identifies the correct
partitions by UUID, and boots the intended bank.

Ecosystem Integration and Future Work
-------------------------------------

The metadata-driven A/B update framework provides the foundation for integrating
FWU metadata handling into different embedded Linux update ecosystems. After the
core implementation in TF-A, U-Boot, and ``meta-st-stmmp``, additional work has
been explored to make FWU metadata handling easier to consume from userspace and
to validate the approach with existing update managers.

The ``libfwumdata`` library was introduced to provide a reusable userspace API
for accessing and modifying FWU metadata [5]_. While the ``fwumdata`` utility is
well suited for command-line operations and manual testing, a library interface
allows update managers and system services to manipulate FWU metadata fields
directly without invoking an external command.

The availability of ``libfwumdata`` enabled its adoption in embedded Linux
build systems. A Buildroot package has been proposed to make the library
available as a standard system component [6]_, and a similar contribution has
been proposed for OpenEmbedded-Core by adding a recipe for ``libfwumdata`` [7]_.

Building on top of this userspace interface, an integration with SWUpdate has
been proposed as a reference use case. The SWUpdate FWU support uses
``libfwumdata`` to update FWU metadata fields during the update workflow,
allowing SWUpdate to manage firmware updates while relying on FWU metadata for
bank selection, trial boot handling, and rollback management [8]_.

The same approach has also been explored in the Mender ecosystem, where
``libfwumdata`` enabled an FWU-based demonstration integration [9]_.

At the time of writing, the SWUpdate and OpenEmbedded-Core contributions are
still under discussion and have not yet been merged upstream. Feedback from
the community is welcome to help identify the most effective approach and guide
the future evolution of FWU support in these projects.

These developments demonstrate how FWU metadata can provide a common foundation
for different update frameworks, including SWUpdate, Mender, and custom update
solutions, while keeping the boot decision process independent from the update
manager implementation.

.. tip::
   Planning an A/B firmware update strategy for STM32MP or other embedded
   platforms? Amarula Solutions designs and upstreams metadata-driven update
   frameworks across U-Boot, TF-A, and Yocto/OE layers.
   `Contact our embedded team <https://www.amarulasolutions.com/contact/>`_

References
----------

.. [1] TF-A FWU A/B support series:
   https://review.trustedfirmware.org/c/TF-A/trusted-firmware-a/+/51367

.. [2] U-Boot support metadata-driven A/B boot for STM32MP25 series:
   https://lore.kernel.org/all/20260430080627.849636-1-dario.binacchi@amarulasolutions.com/

.. [3] U-Boot support metadata-driven A/B boot for STM32MP15 series:
   https://lore.kernel.org/all/20260518065443.2531017-1-dario.binacchi@amarulasolutions.com/

.. [4] U-Boot ``fwumdata`` tool contribution by Kory Maincent (Bootlin):
   https://lore.kernel.org/all/20260223-feature_fwumdata-v4-0-680ea4ad6ce6@bootlin.com/
   https://lore.kernel.org/all/20260326082346.1569343-1-ilias.apalodimas@linaro.org/

.. [5] ``libfwumdata`` repository:
   https://github.com/passgat/libfwumdata

.. [6] Buildroot ``libfwumdata`` package contribution:
   https://lore.kernel.org/all/20260430174619.868510-1-dario.binacchi@amarulasolutions.com/

.. [7] OpenEmbedded-Core ``libfwumdata`` recipe contribution:
   https://patchwork.yoctoproject.org/project/oe-core/patch/20260430175308.868993-1-dario.binacchi@amarulasolutions.com/

.. [8] SWUpdate FWU A/B metadata integration:
   https://groups.google.com/g/swupdate/c/kYr2Hy-f3us

.. [9] Mender FWU demo integration:
   https://github.com/TheYoctoJester/meta-mender-community/tree/wrynose-demos/meta-mender-fwu
