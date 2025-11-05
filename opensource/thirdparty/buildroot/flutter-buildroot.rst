Flutter UI Framework Support in Buildroot
#########################################

Overview
********

The support for the **Flutter** UI framework in the Buildroot embedded Linux build system was primarily developed and contributed by **Adam Duskett** of **Amarula Solutions**. This significant effort introduced the necessary toolchain components and runtime packages to allow developers to cross-compile and run high-performance Flutter applications on custom embedded Linux distributions.

Official support for Flutter was successfully merged and is available starting with **Buildroot version 2023.11**.


Key Components and Packages
***************************

The Buildroot integration includes several critical packages necessary to handle the complex Flutter build system and provide the runtime environment on the target device:

* **flutter-engine**: The core package containing the compiled Flutter engine runtime library (`libflutter_engine.so`). This is the main component deployed to the target device.
* **flutter-sdk-bin**: A set of host tools and plugins required during the cross-compilation process to compile Flutter applications.
* **depot-tools**: Contains the ``gclient`` Python script, which is essential for downloading the Flutter engine source code in the format expected by the Flutter build system.
* **flutter-pi**: A lightweight Flutter embedder for embedded Linux. It typically uses Direct Rendering Infrastructure (DRI) and Kernel Mode Setting (KMS), supporting OpenGL ES and Vulkan.
* **flutter-gallery**: A demonstration application that serves as a template for developers when porting their own Flutter applications.


Technical Implementation Details
********************************

The integration of Flutter posed significant challenges, primarily because Flutter's upstream source acquisition and build process are non-standard for traditional build systems like Buildroot.

Source Acquisition and Reproducibility
======================================

Flutter source code is not released as a standard tarball. It must be downloaded using the ``gclient`` tool from the ``depot-tools`` package, which checks out the source code and its many third-party dependencies. Furthermore, the build process relies on the presence of local **.git directories**.

To ensure Buildroot's requirement for reproducible builds is met, the Flutter packages utilize the following solution:

* A custom script, ``package/flutter-engine/gen-tarball``, was created to run ``gclient`` and package the necessary source files into a Buildroot-compatible tarball for offline use and checksum verification.

Toolchain Dependencies
======================

The Flutter engine is uniquely dependent on specific versions of its toolchain:

* **Bundled Clang Compiler:** The Flutter source tree includes a **patched version of Clang** that *must* be used for compilation. The Buildroot package configuration is set up to use this bundled compiler rather than the default cross-toolchain built by Buildroot to prevent linking errors.
* **GN Build System:** The package also requires the Google Ninja (`gn`) build tool, which is provided by the dependency chain starting with ``depot-tools``.


Usage and Profiling
*******************

Integrating a custom Flutter application into a Buildroot project is typically done by mimicking the structure of the existing ``flutter-gallery`` package and placing the new package definitions in an **External Tree**.

Profiling a Flutter application's performance on the target device is possible by configuring the engine build and runtime:

1.  **Enable Profiling:** Enable the profiling option for the **flutter-engine** package in Buildroot's ``menuconfig``:

    ::

        Libraries ---> Graphics ---> flutter-engine ---> [*] Enable profiling

2.  **Run with VM Service:** Boot the target device and run the application using ``flutter-pi``, enabling the Dart VM service for remote debugging:

    ::

        flutter-pi --profile /usr/share/flutter/${your_app}/profile/ --vm-service-host=0.0.0.0 --vm-service-port=1234

3.  The application output will provide a URL that can be accessed from a remote machine using Dart DevTools for profiling and debugging.
