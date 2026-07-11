==========================================================
Optimizing Android CI: Reducing Build Times by 25% with S3
==========================================================

.. note:: **TL;DR**
   - How Amarula Solutions achieved a **25% reduction in Android CI build times** by integrating **Amazon S3 as a remote Gradle build cache** — sharing build outputs across Jenkins agents and eliminating redundant compilation.
   - Covers **Gradle ``s3-build-cache`` plugin** configuration in Kotlin DSL, Jenkins credential injection for AWS, and plans for a multi-layered caching strategy with the Jenkins Cache Plugin.

How does remote build caching speed up Android CI?
--------------------------------------------------
In large-scale Android and Kotlin Multiplatform (KMP) projects, build times
often become a bottleneck in the CI/CD pipeline. To address this, we have
integrated a remote build cache using Amazon S3. By sharing build outputs
across different Jenkins agents, we have successfully reduced our total
build time by approximately **25%**.

What is the challenge with clean builds?
----------------------------------------
Clean builds in Jenkins are traditionally slow because they start from a
blank slate. Even with local caching on a single node, distributed builds
across multiple nodes often miss the cache, forcing redundant compilation
of unchanged modules.

.. figure:: /images/update-build-time-s3-cache.png
   :align: center

|
|

How do you implement Gradle with S3 caching?
--------------------------------------------
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


What performance gains were achieved?
-------------------------------------
By implementing the remote S3 cache, we observed:

* **Time Savings:** Build stages dropped from ~8 minutes to ~6 minutes.
* **Network Efficiency:** Only modified task outputs are downloaded.
* **Warm Starts:** Every node benefits from the work of previous builds.

What is planned for future caching improvements?
------------------------------------------------
While the Gradle S3 cache handles task-level outputs, we plan to
incorporate the **Jenkins Cache Plugin** in the next release of the
pipeline. This will specifically target **large artifacts** and
external dependencies that fall outside the standard Gradle build cache.

This multi-layered caching strategy will further stabilize our
environment and minimize external network fetches for heavy binary
dependencies.

What is the bottom-line impact?
-------------------------------
A 25% reduction in build time accelerates developer feedback and
optimizes resource usage. Combining Gradle's S3 cache with the
upcoming Jenkins Cache Plugin will provide a comprehensive solution
for high-performance mobile DevOps.

.. tip::
   Need faster CI/CD builds for Android or Kotlin Multiplatform projects?
   Amarula Solutions optimizes build pipelines with remote caching,
   Gradle tuning, and Jenkins infrastructure design.
   `Contact our mobile DevOps team <https://www.amarulasolutions.com/contact/>`_
