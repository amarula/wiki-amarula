com.amarula.gerrit.GerritChange
********************************

.. note:: **TL;DR**
   - Reference for ``GerritChange`` from Amarula Solutions' **repo_jenkins_lib** — represents a single Gerrit change with methods for setting review labels (Verified +1/-1), getting change details, and listing related changes by topic.

Represents single Gerrit change with enough information to fetch the change or set review labels.

.. _com.amarula.gerrit.GerritChange-Constructors:

Constructors
============

All constructors are protected and used internally. The instances are created inside other classes and returned to the pipeline.

.. _com.amarula.gerrit.GerritChange-Publicmethods:

Public methods
==============

**setVerified(int value)**

Sets the Verified label on this change. Values: ``GerritChange.SUCCESS`` (+1) or ``GerritChange.FAILURE`` (-1).

**setReviewFromFile(String filePath)**

Sets a review on this change with comments read from a file.

**getChangeNumber()**

Returns the Gerrit change number.

**getPatchSetNumber()**

Returns the current patch set number.

**getSubject()**

Returns the commit subject line.

.. tip::
   Need Gerrit integration in your Jenkins pipelines? Amarula Solutions
   provides repo_jenkins_lib for automated review workflows, multi-repo
   dependency management, and Gerrit CI/CD integration.
   `Contact our CI/CD team <https://www.amarulasolutions.com/contact/>`_
