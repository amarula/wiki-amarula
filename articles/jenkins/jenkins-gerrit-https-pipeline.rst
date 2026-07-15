Streamlining CI/CD: HTTPS Support in Gerrit-Trigger with Amarula Solutions' Jenkins Pipeline
==================================================================================================

.. note:: **TL;DR**
   - The **Gerrit-Trigger plugin** now supports **HTTPS** (PR #1017), replacing SSH-based repository cloning and event streaming — eliminating firewall issues and simplifying credential management across Jenkins worker nodes.
   - Combined with **Amarula Solutions' Jenkins shared libraries** (``ci_scripts``, ``repo_jenkins_lib``), teams get a **scalable, containerized Gerrit verification pipeline** with Bazel-based build and test orchestration.

|


In modern Continuous Integration and Continuous Deployment (CI/CD) workflows, seamless
communication between code review systems and automation servers is paramount. For teams
relying on Gerrit and Jenkins, the **Gerrit-Trigger** plugin has long been the backbone
of this integration. With recent community developments — specifically the introduction
of HTTPS support in the Gerrit-Trigger plugin via Pull Request #1017 — and robust
pipeline abstractions like the **Amarula Solutions shared library**, teams can construct
highly scalable, secure, and maintainable pipelines.

The Shift to HTTPS in Gerrit-Trigger (PR #1017)
-----------------------------------------------

Historically, Jenkins and Gerrit integrations leaned heavily on SSH for repository
cloning and event streaming. While effective, SSH can present challenges in tightly
controlled corporate networks where outbound SSH ports (like 29418) are blocked by
firewalls. Furthermore, managing SSH keys across multiple Jenkins worker nodes can
be cumbersome.

`Pull Request #1017 <https://github.com/jenkinsci/gerrit-trigger-plugin/pull/1017>`_
on the ``jenkinsci/gerrit-trigger-plugin`` repository ("RFC: Feat/add https support")
introduces a modernized approach by allowing the plugin to leverage HTTPS.

This update provides several architectural benefits:

* **Firewall Friendly**: HTTPS (port 443) is universally open, eliminating the need
  for special firewall rules.
* **Simplified Authentication**: Utilizing REST API credentials or application passwords
  over HTTPS simplifies credential management compared to distributing and rotating SSH keys.
* **Improved Stability**: Leveraging HTTP/REST endpoints often results in more robust
  connection handling during network fluctuations compared to persistent SSH event streams.

Integrating the Amarula Solutions Jenkins Library
-------------------------------------------------

To handle complex build environments seamlessly, organizations like Amarula Solutions
utilize shared Jenkins libraries. This approach abstracts repetitive boilerplate code,
ensuring uniform pipeline behavior across multiple projects.

By utilizing Amarula's ``@Library('ci_scripts')`` and ``@Library('repo_jenkins_lib')``,
developers can leverage pre-built classes like the ``Verification`` class to orchestrate
their Gerrit checks.

Walkthrough of an Amarula Gerrit-Trigger Pipeline
-------------------------------------------------

Using the provided `checks-jenkins.Jenkinsfile <https://github.com/amarula/checks-jenkins/blob/master/.jenkins/checks-jenkins.Jenkinsfile>`_ as a blueprint, we can see how an
elegant Gerrit validation pipeline is structured using HTTPS and Amarula's tools:

1. Environment and Credential Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The pipeline begins by defining the target Jenkins node and establishing the
environment variables for Gerrit. Critically, instead of SSH keys, it maps a
credential ID (``'gerrithub'``) to the ``JENKINS_GERRIT_REST_API_CREDENTIAL_ID``
environment variable, showcasing a REST/HTTPS-driven authentication flow.

2. Pipeline Options and Docker Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``Verification`` class is initialized and provided with a set of options.
This includes specifying a containerized build environment
(``dockerImage: 'gerrit-plugin-builder:1.0'``) and configuring the remote URL
(``gerritRemoteUrl: 'https://gerrithub.io'``) to ensure all checkouts happen
over HTTPS.

3. The Setup Stage
^^^^^^^^^^^^^^^^^^

Because Bazel expects plugins to be nested within a specific Gerrit workspace
structure, the script executes a sophisticated setup phase:

* It moves the current plugin source out of the way into a ``plugin-source/`` directory.
* It executes a shallow git clone of the Gerrit core repository directly into the
  workspace using the specified Gerrit tag (``v3.14.0``).
* It creates a symlink from the isolated ``plugin-source`` directly into
  ``WORKSPACE/plugins/checks-jenkins``. This clever trick ensures that Bazel
  resolves the plugin targets correctly from the workspace root.

4. Building and Testing with Bazel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the workspace successfully mapped, the pipeline uses Bazel to compile and
verify the plugin:

* **Build**: It calculates the available processors (``nproc``) and dynamically
  assigns them to the Bazel build command
  (``bazel build //plugins/checks-jenkins/...``).
* **Test**: Testing requires a specific environment. Because the web test runner
  utilizes ``sh_binary`` targets rather than standard ``sh_test`` targets, standard
  discovery via ``bazel test`` falls short. Instead, the pipeline directly invokes
  them using ``bazel run //plugins/checks-jenkins/web:web_test_runner``.

5. Failure Handling
^^^^^^^^^^^^^^^^^^^

Finally, if any of these stages report a ``FAILURE`` or ``UNSTABLE`` status, the
Amarula library seamlessly catches it and triggers an ``explainError()`` function,
providing immediate, actionable feedback directly to the Gerrit interface.

Conclusion
----------

The addition of HTTPS support in Gerrit-Trigger via PR #1017 represents a
significant step forward in CI/CD networking and security. When combined with a
highly structured pipeline library like Amarula Solutions' ``ci_scripts``, teams
can bypass legacy SSH headaches, standardize their build containers, and execute
complex Bazel workflows with minimal footprint.

.. tip::
   Building Gerrit-Jenkins CI/CD pipelines for embedded or plugin development?
   Amarula Solutions designs and maintains HTTPS-based Gerrit verification
   pipelines with containerized Bazel builds and shared Jenkins libraries.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
