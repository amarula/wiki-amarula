Warning-ng Jenkins plugin now can report Yocto vulnerabilities
==============================================================

.. figure:: /images/yocto-vulnerabilities.png
   :align: center
|
|

Amarula Solutions

**Warning-ng plugin Yocto vulnerabilities scanner**

The yocto scanner integration in warning-ng plugin is released

https://plugins.jenkins.io/warnings-ng/releases/

What does it mean for people that are using Jenkins and yocto in their CI?

They can record their issues on a complete dashboard with a simple step

.. code-block:: groovy

    recordIssues sourceCodeRetention: 'LAST_BUILD', tools: [yoctoScanner(pattern: "cves.json")]

Navigate the issues and find what are the vulnerabilities, go through
the link and find the patches,
using devtool to override the project, apply the patches and provide
to their meta layer and then upstream,
have a consistent history of vulnerability on building history.

https://github.com/jenkinsci/warnings-ng-plugin

This is a really small contribution possible only because there are
other people working on opensource.

Stay tuned!
https://www.amarulasolutions.com/quotation/
