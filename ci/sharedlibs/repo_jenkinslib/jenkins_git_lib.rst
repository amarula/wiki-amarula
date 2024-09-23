com.amarula.git.Git
********************

Helper class that generalizes Android Build steps.

.. _com.amarula.git.Git-Constructors:

Constructors
============

.. _com.amarula.git.Git-Git(context,environment,Stringurl,Mapoptions=[:]):

Git(context, environment, String url, Map options = [:])
--------------------------------------------------------

Creates new instance for handling operations over a specific git repository.

-  **context** Jenkins steps ('this' in pipeline context)
-  **environment** Jenkins environment variables ('env' variable in pipeline context)
-  **url** URL of the git repository
-  **options** Optional options

   -  **directory** directory where to checkout the content, default is repository name from given URL
   -  **gerritRemoteUrl** Gerrit URL, default is from environment GERRIT_HOST
   -  **history** fetch full history (true), or only last commit (false), default is false

.. _com.amarula.git.Git-Publicmethods:

Public methods
==============

.. _com.amarula.git.Git-getDirectory():

getDirectory()
--------------

Return checkout directory.

.. _com.amarula.git.Git-sync(branch='master'):

sync(branch = 'master')
-----------------------

Checks out given branch or master by default.

-  **branch** Branch name to checkout, default is master

.. _com.amarula.git.Git-GerritChangecheckoutChange(Stringrefspec):

GerritChange checkoutChange(String refspec)
-------------------------------------------

Checks out specific Gerrit change given by parameters.

-  **refspec** Gerrit refspec in form e.g. 'refs/changes/77/3377/2'

Returns: Gerrit change specified by parameter or null if it doesn't exist

.. _com.amarula.git.Git-GerritChangecheckoutChange(defchangeNumber,defpatchsetNumber):

GerritChange checkoutChange(def changeNumber, def patchsetNumber)
-----------------------------------------------------------------

Checks out specific Gerrit change given by parameters.

-  **changeNumber** Gerrit Change number, e.g. '3377'
-  **patchsetNumber** Gerrit patch-set number, e.g. '2', if 0 then the latest patchset is used

Returns: Gerrit change specified by parameters or null if it doesn't exist

.. _com.amarula.git.Git-GerritChangecherrypickChange(Stringrefspec):

GerritChange cherrypickChange(String refspec)
---------------------------------------------

Cherrypicks specific Gerrit change given by parameters.

-  **refspec** Gerrit refspec in form e.g. 'refs/changes/77/3377/2'

Returns: Gerrit change specified by parameter or null if it doesn't exist

.. _com.amarula.git.Git-GerritChangecherrypickChange(defchangeNumber,defpatchsetNumber=0):

GerritChange cherrypickChange(def changeNumber, def patchsetNumber = 0)
-----------------------------------------------------------------------

Cherrypicks specific Gerrit change given by parameters.

-  **changeNumber** Gerrit Change number, e.g. '3377'
-  **patchsetNumber** Gerrit patch-set number, e.g. '2', if 0 or not given the latest patchset is used

Returns: Gerrit change specified by parameters or null if it doesn't exist

| 
