Linux DRM Subsystem
===================

.. note:: **TL;DR**
   - Amarula Solutions' **Linux DRM/KMS documentation** — covering the Direct Rendering Manager subsystem for **display drivers, bridges, GPU integration, and display pipelines** on embedded platforms (Allwinner, Rockchip, NXP i.MX).
   - Includes guides on HDMI pipelines, MIPI DSI display interfaces, and runtime display switching.

Amarula Solutions has deep expertise in the Linux DRM subsystem, with maintainer roles
in DSI vendor drivers and contributions to display bridges, panels, and GPU drivers.

.. toctree::
   :maxdepth: 2
   :caption: Related Multimedia Guides

   ../multimedia/hdmi_pilpeline
   ../multimedia/mipi_dsi

Topics covered:

* **Display interfaces** — HDMI, MIPI DSI, eDP, LVDS, RGB
* **GPU drivers** — Etnaviv (Vivante), Mali, Panfrost
* **Display bridges** — HDMI transmitters, MIPI-DSI to LVDS converters
* **Runtime display switching** — 1-to-N muxed display pipelines in Linux DRM

For board-specific display configurations, see the `BSP section <../../../bsp/index.html>`_.

.. tip::
   Need GPU or display driver development for your embedded product?
   Amarula Solutions provides Linux DRM/KMS driver engineering, display
   bridge integration, and mainline GPU driver support for Allwinner,
   Rockchip, and NXP i.MX platforms.
   `Contact our display team <https://www.amarulasolutions.com/contact/>`_
