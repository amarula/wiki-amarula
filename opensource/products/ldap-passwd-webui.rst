==================================
LDAP Password Manager — Web UI
==================================

.. note:: **TL;DR**
   - A lightweight **web-based LDAP and Active Directory password manager** — forked and maintained by Amarula Solutions' engineering team with source code available on GitHub.
   - Provides **end-user self-service password changes** and **administrative user/group management** with Material Design 3 interface, multi-LDAP atomic password changes, and comprehensive security hardening.

.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

.. figure:: /images/ldap-passwd-webui-welcome.png
   :align: center

   Welcome page with navigation cards for password change and administration

|

What is ldap-passwd-webui?
----------------------------

`ldap-passwd-webui <https://github.com/amarula/ldap-passwd-webui>`__ is a
**web-based interface for managing LDAP and Active Directory accounts**,
written in Python with the Bottle micro-framework and the ldap3 library.

Originally created by `Jakub Jirutka <https://github.com/jirutka>`__, the
project was **forked by Amarula Solutions** to extend its capabilities and
adapt it for internal infrastructure needs. It is now actively maintained as
part of Amarula's open source portfolio.

The tool fills a common gap in LDAP-based environments: giving end users a
simple, secure way to change their own passwords without administrator
intervention, while also providing administrators with a lightweight GUI for
managing users and groups — without needing a heavyweight directory management
platform like phpLDAPadmin or Apache Directory Studio.

|

.. figure:: /images/ldap-passwd-webui-password-change.png
   :align: center

   Self-service password change form with strength meter

|

What are the key features?
----------------------------

End-User Features
~~~~~~~~~~~~~~~~~~

- **Self-service password change** — simple form with real-time password
  strength meter and visibility toggle.
- **Responsive Material Design 3** — works comfortably on desktop and mobile
  (down to 375px width), with automatic light and dark theme support.

Administrator Features
~~~~~~~~~~~~~~~~~~~~~~~

- **Admin dashboard** with three tabs: Change Password, Users, and Groups.
- **User management** — create and delete LDAP users (``inetOrgPerson``) with
  optional group assignment.
- **Group management** — create and delete LDAP groups (``groupOfNames`` /
  ``groupOfUniqueNames``), add and remove members.
- **LDAP bind authentication** with group-membership-based authorization.

|

.. figure:: /images/ldap-passwd-webui-admin-dashboard.png
   :align: center

   Admin dashboard — Change Password tab

|

.. figure:: /images/ldap-passwd-webui-admin-create-user.png
   :align: center

   Create user form with optional group membership

|

.. figure:: /images/ldap-passwd-webui-admin-groups.png
   :align: center

   Group management — member listing and add/remove controls

|

Multi-LDAP and Platform Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Supports **OpenLDAP** and **Active Directory / Samba 4 AD**.
- **Atomic multi-LDAP password changes** — change passwords across multiple
  LDAP servers in a single operation, with automatic rollback if any server
  fails.
- Configurable **password complexity policy**: minimum length, uppercase,
  lowercase, digit, and special character requirements.

|

.. figure:: /images/ldap-passwd-webui-dark-mode.png
   :align: center

   Dark mode — automatic via ``prefers-color-scheme``

|

.. figure:: /images/ldap-passwd-webui-mobile.png
   :align: center

   Mobile layout — fully usable at 375px width

|

How does it handle security?
------------------------------

Security was a primary design concern. The application implements defense in
depth across multiple layers:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Security Measure
     - Detail
   * - LDAP Injection Prevention
     - Usernames are escaped per RFC 4515 before LDAP queries
   * - CSRF Protection
     - Cryptographically signed anti-CSRF tokens in SameSite-strict HttpOnly cookies
   * - XSS Prevention
     - All user input and LDAP-sourced error messages are HTML-escaped
   * - Rate Limiting
     - In-memory sliding window: 5 requests per IP, 10 per username per minute
   * - Security Headers
     - CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
   * - Admin Sessions
     - Signed HttpOnly SameSite-strict cookies with 1-hour expiry
   * - Password Complexity
     - Server-side enforcement (not just client-side)
   * - Log Sanitization
     - Usernames logged only as SHA-256 prefix hash
   * - TLS Verification
     - LDAPS/TLS certificate validation, configurable per server

Getting Started
-----------------

Installation
~~~~~~~~~~~~~~

.. code-block:: none

    git clone https://github.com/amarula/ldap-passwd-webui.git
    cd ldap-passwd-webui
    pip install -r requirements.txt

Local Testing with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~

A Docker Compose environment is included for local evaluation:

.. code-block:: none

    docker compose up -d
    docker exec -i ldap-test ldapadd \
        -x -D "cn=admin,dc=example,dc=org" -w admin123 \
        < tests/fixtures/seed.ldif

Test accounts from the seed data:

.. list-table::
   :header-rows: 1
   :widths: 25 25 20 30

   * - Username
     - Password
     - Admin?
     - Purpose
   * - ``admin``
     - ``admin123``
     - Yes
     - Full admin access
   * - ``jdoe``
     - ``user123``
     - Yes
     - Admin user
   * - ``bsmith``
     - ``user123``
     - No
     - Regular user

Configuration
~~~~~~~~~~~~~~

Copy and edit the settings file:

.. code-block:: none

    cp settings.ini.example settings.ini

Key configuration sections:

- **``[html]``** — page title, icon, base path, primary brand color
- **``[password]``** — minimum length and character class requirements
- **``[ldap]`` / ``[ldap:<name>]``** — server host, port, SSL/TLS, base DN, type
  (``ad`` or standard), search filter, TLS verification
- **``[admin]``** — admin group DN, group base DN, admin credentials
- **``[server]``** — WSGI server type (Waitress, Gunicorn, uWSGI), host, port

Multiple LDAP servers can be configured with indexed sections; passwords are
changed atomically across all configured servers.

Production Deployment
~~~~~~~~~~~~~~~~~~~~~~~

For production use, Amarula recommends:

- Run behind **nginx** or **Apache** reverse proxy terminating TLS.
- Set the WSGI server to **Waitress** or **Gunicorn** (not the built-in
  development server).
- Enable ``DEBUG = False`` in the WSGI app to enforce ``Secure`` cookie flag.
- Set ``tls_req_cert = demand`` in the LDAP configuration.
- Configure ``base_path`` when deploying under a sub-path (e.g.,
  ``/ldap-password/``).

|

License and Attribution
-------------------------

- **License:** MIT
- **Upstream:** `jirutka/ldap-passwd-webui <https://github.com/jirutka/ldap-passwd-webui>`__
- **Amarula fork:** `amarula/ldap-passwd-webui <https://github.com/amarula/ldap-passwd-webui>`__

.. tip::
   Need a custom LDAP management solution or help integrating ldap-passwd-webui
   into your infrastructure? Amarula Solutions provides deployment, integration
   support, and custom feature development.
   `Contact us <https://www.amarulasolutions.com/contact/>`_
