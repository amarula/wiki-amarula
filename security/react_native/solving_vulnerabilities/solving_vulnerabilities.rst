Introduction
------------

Resolving vulnerabilities in React Native applications is crucial to
ensure the security and stability of the codebase. We will explore the
tools and techniques that can aid in resolving vulnerabilities
efficiently. We will highlight the importance of utilizing Yarn
Resolutions in ``package.json``, which allows you to enforce specific
versions of dependencies, overriding the versions specified in the
yarn.lock file. Additionally, we will discuss the benefits of using
Patch-package, a tool that enables you to make modifications to
dependencies without directly modifying the source code in cooperation
with postinstall.  However patch-package should be considered as a last
resort in the fixing crashes/issues or vulnerability resolution process,
when other methods such as enforcing specific versions through Yarn
Resolutions or managing dependency are not sufficient to address the
vulnerabilities. The first step should be to search library repositories
and look for vulnerability fixes.

Challenges
----------

When it comes to resolving vulnerabilities, there are several challenges
that developers may encounter. These challenges include compatibility
issues, dependency management complexity, ensuring dependency
compatibility, resolving transitive dependencies, handling version
conflicts, and the need for testing and continuous monitoring. Let’s
explore each of these challenges in detail and discuss strategies to
overcome them effectively.

Compatibility Issues
~~~~~~~~~~~~~~~~~~~~

Upgrading libraries to their maximum versions might lead to
compatibility issues, as the highest versions may not be compatible with
each other. To tackle this challenge, it is recommended to carefully
test library upgrades in a controlled environment. Incrementally upgrade
libraries one by one, ensuring compatibility as you progress. If
compatibility issues arise, consider using older versions that are known
to work well together or seek alternatives that offer similar
functionality.

Dependency Management
~~~~~~~~~~~~~~~~~~~~~

Managing dependencies in a React Native project can be complex,
especially when different libraries have conflicting or overlapping
dependencies. To overcome this challenge, it is essential to have a
thorough understanding of your project’s dependencies and their
interdependencies. Utilize tools like ``yarn.lock`` to analyze and
resolve dependency conflicts. Consider using dependency management tools
like Yarn resolutions to enforce specific versions and resolve conflicts
effectively.

Dependency Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~

One challenge you may face is ensuring compatibility between different
dependencies when using yarn resolutions. Sometimes, upgrading one
library to resolve a vulnerability can introduce compatibility issues
with other dependencies.

To overcome this challenge, it’s important to carefully review the
documentation and release notes of each dependency. Look for any
breaking changes or compatibility issues that may arise when upgrading a
specific library. Additionally, you can test your application thoroughly
after making version changes to identify and address any compatibility
issues early on.

**Example**: Let’s say you have a vulnerability in the
``react-navigation`` library. Upgrading it to the latest version
(``^6.0.0``) causes compatibility issues with the
``react-native-gesture-handler`` library, which requires a lower version
(``^2.0.0``).

To address this, you can specify a compatible version in the resolutions
field of your ``package.json``:

::

   "resolutions": {
     "react-navigation": "^5.0.0"
   }

Resolving Transitive Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another challenge is resolving vulnerabilities in transitive
dependencies, which are dependencies of your project’s direct
dependencies. Simply upgrading the versions of direct dependencies may
not solve vulnerabilities in their transitive dependencies.

To address this challenge, you can use yarn resolutions to enforce
specific versions for the transitive dependencies as well. Analyze the
vulnerability reports from tools like `mend.io <http://mend.io>`__.
There are another options which are reading from open streams, so it not
may be trustful as `mend.io <http://mend.io>`__, but for quick check can
be just fine to run ``npm audit`` or ``yarn audit`` to identify the
affected transitive dependencies and include them in the resolutions
field of your ``package.json`` file.

**Example:** Let’s say you have a vulnerability in the ``axios``
library, and it has a transitive dependency on ``lodash`` which also has
a vulnerability, but ``axios`` haven’t treat the vulnerability
on ``lodash`` yet.

To resolve this, include the transitive dependency in the resolutions
field of your ``package.json``:

::

   "dependencies": {
        "axios": "^0.21.1"
   }
   "resolutions": {
        "lodash": "^4.17.21"
   }

**Example2**: Resolving vulnerabilities in transitive dependencies can
become complex when multiple direct dependencies are involved, causing a
chain of transitive dependencies. Let’s consider an example to
illustrate this scenario:

Suppose your project has two direct dependencies, "libraryA" and
"libraryB." "LibraryA" has a vulnerability that requires an upgrade (and
has security fix), and it has a transitive dependency on "libraryC."
However, "libraryC" also has a vulnerability that needs to be addressed,
and it has a transitive dependency on "libraryD.". If maintainers
"libraryA" or "libraryB." would ignore vulnerabilities in the libraryC
and libraryC would also ignore vulnerability on  libraryD then you
should use yarn resolution. The big problem could be if there is no fix
at all, then you can use patch package and fix it by yourself (may be
help to other users to make pull request in their gits).

To tackle this complex situation, you can utilize yarn resolutions to
enforce specific versions for all the transitive dependencies.  In our
example, you would include the resolutions for both "libraryC" and
"libraryD"  in your package.json. Direct dependency "libraryA", you
would include change in the dependencies block directly (without need of
resolution):

::

    "dependencies":{
        "libraryA":  "^1.5.7",
        "libraryB":  "^2.0.0",
    }
    "resolutions":  {
       "libraryC":  "^3.1.0",
       "libraryD":  "^4.1.0",
    }

By explicitly specifying the versions in the resolutions field, you
ensure that the vulnerable transitive dependencies are resolved,
providing a more secure and stable environment for your project.

Version Conflicts
~~~~~~~~~~~~~~~~~

Resolving vulnerabilities using yarn resolutions can sometimes lead to
version conflicts between different dependencies. This occurs when
multiple dependencies have conflicting requirements for the same
package.

To handle version conflicts, you may need to manually adjust the
versions specified in the resolutions field of your ``package.json``.
Experiment with different versions or consult the documentation of the
conflicting dependencies to find a compatible resolution.

**Example**: Let’s say you have a vulnerability in the
``react-native-image-picker`` library, and resolving it requires
upgrading the ``react-native`` library to a higher version. However,
another library, such as ``react-native-maps``, has a specific version
requirement that conflicts with the upgraded ``react-native`` version.

In this case, you may need to experiment with different versions or
consult the documentation of the conflicting libraries to find a
compatible resolution. For example:

::

   "dependencies": {
        "react-native": "^0.65.0"
   }
   "resolutions": {
        "react-native-maps": "^0.28.0"
   }

Testing and Validation
~~~~~~~~~~~~~~~~~~~~~~

After resolving vulnerabilities, it is crucial to thoroughly test and
validate your application. Ensure that the fixes and upgrades do not
introduce new bugs or regressions. Perform comprehensive testing,
including functional, integration, and security testing, to validate the
effectiveness of the vulnerability resolutions.

Continuous Monitoring
~~~~~~~~~~~~~~~~~~~~~

Resolving vulnerabilities is an ongoing process, as new vulnerabilities
may be discovered in dependencies over time. It’s essential to stay
vigilant and keep your dependencies up to date.

Regularly monitor the vulnerability reports from tools like mend
and continuously schedule the scan via jenkins tool for instance
or ``npm audit`` or ``yarn audit``. Stay informed about security
advisories and updates related to your dependencies. Update your
resolutions and dependencies accordingly to address newly discovered
vulnerabilities.

Resolving Vulnerabilities tools
-------------------------------

When it comes to resolving vulnerabilities, it is crucial to follow a
proper procedure and prioritize the tools accordingly. Yarn is
particularly valuable in this regard because it allows for upgrading
direct dependencies and, as a result, their transitive dependencies.
However, it is important to note that the first step should be to search
library repositories and look for vulnerability fixes.

Utilizing Yarn Resolutions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Yarn provides a feature known as resolutions, which proved to be a
valuable tool in resolving vulnerabilities efficiently. By configuring
the resolutions field in the ``package.json`` file, specific versions of
dependencies can be enforced, overriding the versions specified in the
``yarn.lock`` file. This approach ensures that the required versions are
used, mitigating potential vulnerabilities.

To utilize yarn resolutions, follow these steps:

1. Install Yarn globally if it doesn’t already installed by running the
   following command:
::

   npm install -g yarn

2. Navigate to the root directory of your project.

3. Open the ``package.json`` file and add a ``resolutions`` field if it
   doesn’t already exist. For example:
::

   "resolutions": {
        "**/xmldom": "latest"
   }

In the example above, the ``xmldom`` library is forced to use the latest version.

4. Run the following command to install the dependencies with the enforced resolutions:
::

    yarn install

Using Patch-package
~~~~~~~~~~~~~~~~~~~

Patch-package is a helpful tool that allows for making changes to the
dependencies directly. It provides a mechanism to apply patches to
libraries without modifying the original source code. By utilizing
patch-package, you can address vulnerabilities or make necessary
adjustments specific to your project, while still being able to easily
update the library in the future.

1. Navigate to the root directory of your project.

2. | Install patch-package by running the following command:
   | ``yarn add patch-package``

3. Make the necessary changes to the dependencies in your project. For
   example change react-native index.js file.

4. | Run the following command to generate patch files for the modified
     dependencies:
   | ``yarn patch-package  <package-name>\``
   | Replace ``<package-name>`` with the name of the package you made
     changes to.

5. Commit the generated patch files and include them in your version
   control system.

6. Install postinstall and follow steps below.

7. Whenever you run ``yarn install``, patch-package will automatically
   apply the patches, ensuring your modifications persist even after
   package updates. Beware that patches are on the specific version of
   the package, so whenever package’s version is changed, new patch file
   is required.

Postinstall Scripts
~~~~~~~~~~~~~~~~~~~

Postinstall scripts can be used to automate tasks after the installation
of dependencies. By leveraging this feature, you can perform additional
checks or actions to ensure the security and stability of the project.
For example, running vulnerability scans or applying necessary patches
can be automated using postinstall scripts.

1. Navigate to the root directory of your project.

2. | Install patch-package by running the following command:
   | ``yarn add postinstall-postinstall``

3. Open the ``package.json`` file in your project.

4. | Add a ``postinstall`` into block with script that includes the
     necessary commands. For example:
   | ``"scripts":  {  "postinstall":  "patch-package"  }``

5. Save the changes to ``package.json``.

6. Run ``yarn install`` and the postinstall script will execute
   automatically.

Clearing Cache
--------------

Clearing the yarn cache and native part caches can help in recovering
from potential issues related to cached dependencies and can also
resolve certain problems that arise due to conflicting or outdated cache
entries.

**Important notice. You should be vigilant and make it a habit to
regularly clean the cache of your project to avoid potential issues,
bugs, crashes and ensure optimal performance.**

Mend
----

Whitesource contains configuration file which set the behavior of the Unified Agent scan.

`Here <https://docs.mend.io/bundle/unified_agent/page/unified_agent_configuration_parameters.html>`__
you can find the complete option documentation, but I highlighted most
common config options:

**npm.resolveLockFile** - Whether the Unified Agent will rely on the
manifest (**package.json**) and lock file (**package-lock.json**) for
the resolution and not rely on NPM commands. If the lock file is
missing, the detection will be based on the **node_modules** folder.

**resolveAllDependencies** -

Whether to enable or disable by default all dependency resolvers for a
scan. Default value is True.

| For example, when the following parameters are set, only npm
  dependencies will be resolved in this case:
| *resolveAllDependencies*\ =\ *false*
| *npm.resolveDependencies*\ =\ *true*
| *#maven.resolveDependencies\ *\ **=**\ *\ false*

Maven would be normally True (thats default value), but it will be
overwritten with the False value of resolveAllDependencies.

**forceCheckAllDependencies** - Force checks all policies for all
dependencies introduced to the Mend projects.

**excludes** - Whether to exclude specific files from the scan. If a
directory is specified to be excluded, no manifest files located in the
directory will be picked up by the different resolvers.

**fileSystemScan** - Performs a file system scan for source files and
binaries, in addition to the package manager based
dependencies resolution. The files to be scanned can be controlled by
the includes and excludes parameters and the resolver-specific
*ignoreSourceFiles* parameters.

**maven.resolveDependencies**  - Whether to resolve Maven dependencies,
requires "pom.xml".

**gradle.resolveDependencies** - Whether to resolve Gradle dependencies.
Requires build.gradle or build.gradle.kts.

**gradle.includedConfigurations** -

Enables you to determine which dependency configurations to include in
the scan.

The format is according to the following:

-  Exact configuration names to include.

| Values should be space-delimited.
| For example:

gradle.includedConfigurations= compileOnly testCompileOnly

Includes configurations named "compileOnly" and "testCompileOnly".

-  Configurations can include regular expressions.

For example:

gradle.includedConfigurations=.\ **Only.**

Includes all configuration names that contain the string "Only"

**npm.resolveDependencies**  - Whether to resolves NPM/yarn/pnpm
dependencies.

**npm.includeDevDependencies** - Whether to include dev dependencies.

**cocoapods.resolveDependencies** - Whether to resolve CocoaPods
dependencies (using CocoaPods).

**cocoapods.ignoreSourceFiles** - When using the dependency resolver, it
will only include package dependencies, not source files.

**docker.scanImages** -

Runs scans on all or specified images.

When set to True, only Docker image scan will occur. This will include
the detection of Linux packages, and a general scan of the image file
system for package managers’ based resolution and identification of
source files/binaries.

**docker.scanTarFiles** - Used when the user supplies the .tar file of a
Docker image.

**docker.scanContainers** -

| Scan all or specified containers.
| When set to True, only Docker container scan will occur. This will
  include the detection of Linux packages, and a general scan of the
  container file system for package managers’ based resolution and
  identification of source files/binaries.

Before starting a container scan, run the command "docker ps -a" to
check for listed containers.

**scanPackageManager** -

Scans Linux packages by their file name and version. Supported package
types are Debian, RPM, Alpine, Arch Linux, and DNF.

Depending on the package type, one of the following commands will be
run:

-  Debian: dpkg -l

-  RPM: rpm -qa

-  Alpine: apk -vv info

-  Arch Linux: pacman -Q

-  DNF/ centOS:8 - no command, image should contain at least journal.log
   file (installation log) and rpm.dnf.log file (in case of system
   packages update was executed).