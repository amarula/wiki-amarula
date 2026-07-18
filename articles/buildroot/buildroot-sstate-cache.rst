Buildroot Shared State Cache (sstate-cache)
##############################################

.. note:: **TL;DR**
   - Buildroot now supports a **Yocto-style shared state cache (sstate-cache)** — when enabled, it computes a per-package state signature and caches installation outputs as compressed tarballs. On cache hits, subsequent builds skip downloading, extracting, patching, configuring, and building, directly restoring cached files instead.
   - Covers configuration variables, hash computation, artifact capture/restore via OverlayFS, package infrastructure integration, and RPATH relocation for cache portability.

Overview
********

When enabled, the sstate-cache feature computes a state signature for each
package and caches its installation outputs as compressed tarballs. If
subsequent builds match these signatures, Buildroot skips downloading,
extracting, patching, configuring, and building, directly restoring the
cached files instead.

The implementation is developed and maintained by Amarula Solutions in the
`amarula/buildroot-sstate-cache <https://github.com/amarula/buildroot-sstate-cache/commits/master/>`_
GitHub repository.

.. image:: /images/sstate-cache-buildroot.drawio.png

Configuration Variables
***********************

* **``BR2_SSTATE_CACHE``**: A boolean option added to the Build options menu
  to enable the sstate cache.
* **``BR2_SSTATE_CACHE_DIR``**: A string configuration specifying the cache
  location, which defaults to ``$(HOME)/.buildroot-sstate-cache``.
* **Hash Storage**: Shared state hashes (package signatures) are stored in a
  ``hashes`` subdirectory within this cache location.

Core Components
***************

1. Hash Computation
===================

* **Script**: The ``support/scripts/compute-hash.sh`` script generates a
  per-package SHA256 state signature.
* **Inputs**: The hash is aggregated from the package's recipe ``.mk`` files,
  patches, source tarball, and recursive dependency hashes.
* **Targeted Config Hashing**: The script hashes a targeted subset of 31
  Buildroot ``.config`` key prefixes that affect binary output (e.g.,
  architecture, compiler version, optimization).
* **Cache Invalidation**: Hashing a targeted subset prevents cache
  invalidation when unrelated packages are modified or added.

2. Artifact Capture and Restore
===============================

* **Script**: The ``support/scripts/capture-overlay.sh`` helper handles cache
  artifact creation and restoration.

Subcommands:

* ``check``: Tests if OverlayFS capture is supported via ``unshare -Urm``.
* ``restore``: Extracts cached tarballs to destination directories.
* ``overlay``: Captures artifacts using a user and mount namespace with
  OverlayFS. It mounts OverlayFS over the destination directory, runs the
  install script, and packages the upper layer as an atomic tarball.
* ``capture``: Provides a file-list-based tarball creation fallback for
  systems lacking user namespace support.

3. Package Infrastructure Integration
=====================================

* **Modifications**: Core logic is added to ``package/pkg-generic.mk`` via
  helper macros like ``sstate-compute-hash``, ``sstate-check-cache``, and
  ``sstate-restore-phase``.
* **Stamp Rules**: Stamp rules ranging from ``.stamp_downloaded`` to
  ``.stamp_installed`` are rewritten to generate and use external shell
  scripts.
* **Execution Options**: These generated scripts evaluate whether to use
  cache restoration, OverlayFS capture, or direct script execution.
* **Short-circuiting**: On a cache hit, the downloaded stamp restores all
  phases (host, target, staging, and images) in parallel, and subsequent
  stamps like build and configure are skipped.

4. Relocating RPATHs
====================

* **Script Modifications**: The ``support/scripts/fix-rpath`` script is
  updated to relocate RPATHs from other build directories.
* **Functionality**: When cache artifacts are reused in a different output
  directory, host binaries might point to the old ``HOST_DIR``.
* **Path Replacement**: The script uses ``sed`` to replace any
  ``/<dir>/host/lib`` paths with the current ``$(HOST_DIR)/lib`` path before
  ``patchelf`` makes the path relative.

.. tip::
   Need faster Buildroot builds with shared state caching? Amarula Solutions
   provides Buildroot optimization, sstate-cache configuration, and CI/CD
   integration for reproducible embedded Linux builds.
   `Contact our build systems team <https://www.amarulasolutions.com/contact/>`_
