================================
Amarula Solutions Infrastructure
================================

.. note:: **TL;DR**
   - **Turnkey development infrastructure** that Amarula Solutions runs every day for its own embedded Linux, Yocto, Android, and firmware projects — OpenLDAP (central authentication), Gerrit (code review), Gitea (Git hosting), Jenkins (CI/CD), Apache2 (reverse proxy and TLS), a standardized **Pipeline Library**, **Mend SCA** (security and license scanning), and the **reviewAI** and **explain-error** AI plugins.
   - Fully **provisioned as code with Ansible**: the same playbook deploys a single-box Vagrant evaluation environment in about 45 minutes or a distributed production topology — no configuration drift, every change auditable in Git.
   - **100% open source and self-hosted**, with the audit trail, SBOM generation, and vulnerability reporting needed for **EU Cyber Resilience Act (CRA)** compliance.

.. figure:: /images/infrastructure/architecture.png
   :align: center
   :alt: Amarula Solutions Infrastructure architecture — OpenLDAP, Gerrit, Gitea, Jenkins, Apache2, Pipeline Library, Mend SCA, reviewAI and explain-error

   Eight integrated components — from identity to AI, provisioned as code in under an hour.

What is Amarula Solutions Infrastructure?
=========================================

It is the integrated platform behind every Amarula Solutions project: central
identity, code review, Git hosting, CI/CD automation, security scanning, and
AI-assisted development — provisioned from a single Ansible repository instead
of being assembled by hand.

This is not a demo stack. It is the same infrastructure our own engineers use
daily for Gerrit reviews, Jenkins pipelines, and AI-assisted diagnostics, which
is why every component is proven in production before it is offered to a
customer.

The rest of this section documents how pipelines are built on top of the
platform — see :doc:`jenkins`, :doc:`sharedlibs/index`, :doc:`gerrit_trigger`,
and :doc:`docker` for the technical details.

How is the platform architected?
================================

.. list-table::
   :widths: 20 25 55
   :header-rows: 1
   :class: fit-table

   * - Component
     - Role
     - What it provides
   * - **OpenLDAP**
     - Central authentication and SSO
     - One user directory for every tool — permissions are mapped automatically.
   * - **Gerrit 3.x**
     - Code review
     - Patch-set-based review — the model used by Android and the Linux kernel.
   * - **Gitea**
     - Git hosting
     - Self-hosted Git with a GitHub-compatible API and package registry for artifacts.
   * - **Jenkins**
     - CI/CD engine
     - Build orchestration for Yocto, Android, firmware, and applications.
   * - **Apache2**
     - Reverse proxy and TLS
     - Single TLS entry point for all services.
   * - **Pipeline Library**
     - Standardized CI/CD steps
     - Amarula's Groovy shared libraries — build, sync, changelog, UI, and error handling.
   * - **Mend SCA**
     - Security and license scanning
     - Every build scanned for CVEs and licenses; SBOM generated automatically.
   * - **reviewAI + explain-error**
     - AI code review and build diagnostics
     - AI review on every Gerrit patch set; AI root-cause analysis for every Jenkins failure.

How does infrastructure as code work here?
==========================================

Every service, configuration file, and certificate is defined in Ansible and
versioned in Git. Provisioning a complete environment is one command:

.. code-block:: yaml

    # Provision complete infrastructure
    - name: Amarula Solutions Infrastructure
      hosts: all
      become: true
      vars_files:
        - vars/production.yml

      roles:
        - role: ansible-role-openldap
        - role: udi-provision-gerrit
        - role: ansible-role-gitea
        - role: udi-provision-jenkins
        - role: ansible-role-apache2

      tasks:
        - name: Deploy Jenkins LDAP config
          template:
            src: jenkins_config.xml.j2
            dest: /var/lib/jenkins/config.xml
        - name: Enable reverse proxy
          template:
            src: reverse-proxy.conf.j2

The practical consequences:

- **Idempotent** — run the playbook once or a hundred times: the result is identical. No configuration drift.
- **Auditable** — every infrastructure change is a Git commit with full history and accountability.
- **Reviewable** — infrastructure changes go through the same Gerrit review workflow as application code.
- **Repeatable** — tear the environment down and rebuild it identically; disaster recovery is built in.

How does single sign-on work?
=============================

LDAP is the source of truth for identity. Users exist once in the directory, and
Gerrit, Gitea, and Jenkins all authenticate against it:

.. code-block:: text

    dc=example,dc=com
    ├── ou=people
    │   ├── cn=Admin        (admin user)
    │   └── cn=...          (other users)
    └── ou=groups
        ├── cn=admins       → Gerrit/Gitea/Jenkins administrator
        └── cn=developers   → regular users

- A new team member is added to LDAP and immediately has access to every tool.
- Membership in the ``admins`` group automatically grants administrator privileges in all tools (``groupOfUniqueNames`` with ``uniqueMember`` DN matching).
- Offboarding is a single LDAP removal — access is revoked everywhere at once.
- Password self-service is available through :doc:`../opensource/products/ldap-passwd-webui`.

How do you go from evaluation to production?
============================================

The same Ansible roles and the same playbook drive both environments; the only
difference is the inventory file.

.. figure:: /images/infrastructure/deployment-models.png
   :align: center
   :alt: Development/evaluation single-box Vagrant inventory next to the distributed production inventory

   The only difference between evaluation and production is the addresses in the inventory file.

Evaluation runs with ``make vagrant`` (about 45 minutes on a laptop); production
deploys with ``make provision``. After provisioning, the full stack is running:

.. code-block:: text

    $ make vagrant

    # ~45 minutes later:
    ✓ OpenLDAP         — ldap://192.168.202.201:389
    ✓ Gerrit           — https://192.168.202.201:8081
    ✓ Gitea            — https://192.168.202.201:3000
    ✓ Jenkins          — https://192.168.202.201:8080
    ✓ Mend SCA         — integrated, scanning every build
    ✓ reviewAI         — active on every patch set
    ✓ explain-error    — explaining every failure
    ✓ Pipeline Library — standardized build patterns

What is included in the CI/CD layer?
====================================

Pipelines are built from Amarula's shared libraries, so every project follows
the same pattern instead of growing its own:

- **repo_jenkins_lib** — Gerrit-driven repo manifest sync, topic cherry-picks, and cross-project builds.
- **com.amarula.build.Build** — manifest checkout, topic cherry-pick, and parallel stage orchestration.
- **changelog_jenkins_lib** — release notes generated automatically from Git history.
- **Mend integration** — credentials injected with ``withCredentials``, Yocto CVE scanner via ``recordIssues``, SBOM generated per build.
- **explainError()** — AI diagnosis of build failures, callable from ``post { failure { ... } }``.
- **throttle and node labels** — resource-aware scheduling with kas-container images from a private registry.

See :doc:`sharedlibs/index` for the complete library documentation and
:doc:`../articles/jenkins/index` for production pipeline examples.

How are security and compliance handled?
========================================

Mend (formerly WhiteSource) performs Software Composition Analysis on every
build: dependencies are checked against a vulnerability database, license
compliance issues are flagged, and an SBOM is generated automatically. Critical
findings block the build; Mend Renovate can open pull requests with version
bumps for outdated packages.

This maps directly onto the **EU Cyber Resilience Act (CRA)**, which applies
from December 2027 to every product with digital elements sold in the EU:

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: fit-table

   * - CRA requirement
     - How the infrastructure helps
   * - Vulnerability reporting within 24 hours
     - Mend SCA produces automated CVE alerts on every build.
   * - SBOM for every release
     - Mend generates an SBOM per build, regenerated automatically.
   * - Security updates delivered separately from features
     - Jenkins pipelines deliver signed, reproducible artifacts.
   * - 10-year documentation
     - Git-versioned infrastructure plus the Gerrit audit trail keeps complete history.
   * - Risk assessments before market placement
     - Gerrit review records and CI results form a documented assessment trail.
   * - CE marking with cybersecurity
     - Full traceability from commit to review, build, scan, and release.

See :doc:`../articles/jenkins/jenkins-mend-pipeline` for the Mend pipeline
walkthrough and :doc:`../opensource/products/meta-mend` for the Yocto layer.

How does AI fit into the workflow?
==================================

Two plugins extend the platform without changing how teams work:

- **reviewai-gerrit-plugin** — AI code review directly in Gerrit. Every patch set is reviewed automatically; findings are posted as inline and patch-level comments. A chatbot sidebar answers questions about a change, and reviews can be triggered from comments with ``/review``, ``/suggest``, and ``/help``, optionally scoped to specific files or commit messages. See :doc:`../opensource/products/reviewai-gerrit-plugin`.
- **explain-error-plugin** — AI build diagnostics in Jenkins. Any failed build can be explained with one click, globally for every failure, or through the ``explainError()`` pipeline step; the explanation can be sent to Slack, email, or dashboards. Experimental auto-fix can generate a fix and open a pull request.

Both support multiple AI providers — including OpenAI, Anthropic, Google Gemini,
DeepSeek, Amazon Bedrock, Azure OpenAI, and Moonshot — and can run fully local
with Ollama for air-gapped environments, so source code never has to leave the
customer's network.

The resulting workflow:

.. figure:: /images/infrastructure/ai-workflow.png
   :align: center
   :alt: Developer pushes to Gerrit where reviewAI reviews, then human review and merge; Jenkins CI with explain-error and Mend SCA produces the artifact

   AI eliminates the waiting — instant code review, instant failure diagnosis, instant security feedback.

What is the return on investment?
=================================

.. figure:: /images/infrastructure/roi.png
   :align: center
   :alt: ROI summary — 80% reduction in setup time, 3x faster time-to-first-build, 90% fewer configuration errors

   Based on Amarula's own deployment data; the Vagrant evaluation lets you measure ROI on your own infrastructure before committing.

How does the platform compare?
==============================

.. list-table::
   :widths: 26 25 25 24
   :header-rows: 1
   :class: fit-table

   * - Capability
     - Amarula Infrastructure
     - SaaS forges (GitHub/GitLab)
     - Build your own
   * - Deployment time
     - ~45 minutes
     - Days to weeks
     - Weeks to months
   * - Data sovereignty
     - ✅ Your network
     - ❌ Vendor cloud
     - ✅ Your network
   * - No vendor lock-in
     - ✅ 100% open source
     - ❌ Proprietary
     - ✅ But your code
   * - Integrated code review
     - ✅ Gerrit built-in
     - ✅ PR-based model
     - ⚠️ You build it
   * - Central auth (SSO)
     - ✅ LDAP, auto-mapped
     - ✅ SAML/OIDC by tier
     - ⚠️ You integrate it
   * - Built-in SCA security
     - ✅ Mend, every build
     - ⚠️ Dependabot
     - ⚠️ You add it
   * - AI code review
     - ✅ reviewAI
     - ⚠️ Copilot (separate)
     - ❌ Not feasible
   * - AI build diagnostics
     - ✅ explain-error
     - ❌ None
     - ❌ Not feasible
   * - CRA compliance
     - ✅ Full audit trail
     - ⚠️ Partial
     - ⚠️ Your responsibility
   * - Infrastructure as code
     - ✅ One playbook
     - ⚠️ Separate tooling
     - ⚠️ Depends on skill
   * - Pipeline standardization
     - ✅ One shared library
     - ⚠️ Per-repo CI YAML
     - ❌ Ad-hoc per project
   * - Maintenance burden
     - 🟢 Low (Ansible)
     - 🟢 Low (vendor)
     - 🔴 High (your team)

The platform occupies a specific position: the capabilities of a SaaS forge,
the sovereignty of self-hosted software, and AI integrated into the workflow —
all provisioned as code.

How does an engagement work?
============================

.. list-table::
   :widths: 18 12 70
   :header-rows: 1
   :class: fit-table

   * - Phase
     - Timeline
     - What happens
   * - **Discovery**
     - Week 1
     - Half-day workshop to map the current toolchain, team structure, and compliance requirements.
   * - **Tailoring**
     - Weeks 1–2
     - The infrastructure is configured for your network topology, authentication provider, and project structure.
   * - **Deploy**
     - Week 2
     - One command deploys to your hardware — physical, virtual, or cloud — validated together with your team.
   * - **Handover**
     - Week 3
     - Training, documentation, and the Git repository. You own the stack; support continues if needed.

Deliverables include the complete Ansible playbook repository, inventory files
for your topology, a Pipeline Library configured for your projects, Mend SCA
integration, AI review and diagnostics enabled, admin training, and a CRA
documentation package.

Evaluation happens on a Vagrant box before any commitment: we provision your
future infrastructure on a laptop, and you push code through Gerrit review,
trigger Jenkins builds, read AI review comments, and inspect Mend scan results.

.. tip::
   Ready to evaluate your own infrastructure? Amarula Solutions provisions the
   full stack on a Vagrant box so you can measure it on your own projects —
   no obligation, no paperwork.
   `Contact our infrastructure team <https://www.amarulasolutions.com/contact/>`_
