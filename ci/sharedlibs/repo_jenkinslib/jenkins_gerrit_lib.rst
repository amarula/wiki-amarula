com.amarula.gerrit.GerritChange
********************************

Represents single Gerrit change with enough information to fetch the change or set review labels.

.. _com.amarula.gerrit.GerritChange-Constructors:

Constructors
============

All constructors are protected and used internally. The instances are created inside other classes and returned to the pipeline.

.. _com.amarula.gerrit.GerritChange-Publicmethods:

Public methods
==============

.. _com.amarula.gerrit.GerritChange-setVerified(Verifiedverified):

setVerified(Verified verified)
------------------------------

Set Verified review label for this change to given value.

-  **verified** value for Verified label, either GerritChange.SUCCESS or GerritChange.FAILURE

.. _com.amarula.gerrit.GerritChange-booleanequals(o):

boolean equals(o)
-----------------

Compares two GerritChange instances.

-  **o** instance to compare

.. _com.amarula.gerrit.GerritChange-StringtoString():

String toString()
-----------------

Returns string in format "<Gerrit Project>/<Change number>/<Current patchset> (<Change Id>)".
