==========================================================
Optimizing Android CI: Reducing Build Times by 25% with S3
==========================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>


Introduction
------------

In large-scale Android and Kotlin Multiplatform (KMP) projects, build times
often become a bottleneck in the CI/CD pipeline. To address this, we have
integrated a remote build cache using Amazon S3. By sharing build outputs
across different Jenkins agents, we have successfully reduced our total
build time by approximately **25%**.

The Challenge
-------------

Clean builds in Jenkins are traditionally slow because they start from a
blank slate. Even with local caching on a single node, distributed builds
across multiple nodes often miss the cache, forcing redundant compilation
of unchanged modules.

.. figure:: /images/update-build-time-s3-cache.png
   :align: center

|
|

Implementation: Gradle and S3
-----------------------------

The solution involves updating the Gradle configuration to support S3 as a
storage backend and configuring the Jenkins pipeline to provide the
necessary credentials.

1. Gradle Configuration
~~~~~~~~~~~~~~~~~~~~~~~

We utilized the ``s3-build-cache`` plugin in ``settings.gradle.kts``. The
configuration enables local caching for immediate lookups and remote S3
caching for persistent, shared storage across the team.

.. code-block:: kotlin

    plugins {
        id("com.github.burrunan.s3-build-cache") version "1.9.5"
    }

    val isCiServer = "isCIServer" in System.getenv()
    val accessKeyId = System.getenv("AWS_ACCESS_KEY_ID")
    val secretKey = System.getenv("AWS_SECRET_KEY")

    buildCache {
        local { isEnabled = true }
        remote<com.github.burrunan.s3cache.AwsS3BuildCache> {
            region = "eu-west-1"
            bucket = "amarula-jenkins-cache"
            prefix = "travelSmartCache/"
            isPush = isCiServer
            awsAccessKeyId = accessKeyId
            awsSecretKey = secretKey
        }
    }

2. Jenkins Pipeline Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pipeline injects AWS credentials and sets the ``isCIServer`` flag.
This ensures that only verified builds from the CI environment can
populate the remote cache.

.. code-block:: groovy

    'Build': {
      withCredentials([
          [ $class: 'AmazonWebServicesCredentialsBinding', 
            credentialsId: "job-cacher-amarula",
            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            secretKeyVariable: 'AWS_SECRET_KEY'
          ]
      ]) {
        sh 'export isCIServer=true; ./gradlew clean build --build-cache'
      }
    }


Performance Gains
-----------------

By implementing the remote S3 cache, we observed:

* **Time Savings:** Build stages dropped from ~8 minutes to ~6 minutes.
* **Network Efficiency:** Only modified task outputs are downloaded.
* **Warm Starts:** Every node benefits from the work of previous builds.

Future Work: Jenkins Cache Plugin
---------------------------------

While the Gradle S3 cache handles task-level outputs, we plan to
incorporate the **Jenkins Cache Plugin** in the next release of the
pipeline. This will specifically target **large artifacts** and
external dependencies that fall outside the standard Gradle build cache.

This multi-layered caching strategy will further stabilize our
environment and minimize external network fetches for heavy binary
dependencies.

Conclusion
----------

A 25% reduction in build time accelerates developer feedback and
optimizes resource usage. Combining Gradle's S3 cache with the
upcoming Jenkins Cache Plugin will provide a comprehensive solution
for high-performance mobile DevOps.
