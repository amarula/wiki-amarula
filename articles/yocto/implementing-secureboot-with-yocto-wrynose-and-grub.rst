Implementing Secureboot with Yocto Wrynose and Grub
===================================================
.. raw:: html

    <a href="https://www.amarulasolutions.com/contact" class="contact-button-inline">
        Contact Us
    </a>
    <div class="contact-button-clear"></div>

|
|


A customer recently came to Amarula Solutions with the task of creating
a custom Yocto X64 image with the following features:

- A/B updates integrating Mender (https://mender.io/)
- LUKS with auto-decryption using an onboard TPM
- Read-only file system
- SELinux enabled
- uEFI Secureboot

This was a job that fit our skill-set perfectly, and we were happy to
help! I decided to attack the project in the following order:

- Create a custom layer for the company
- Get the image booting with the following partition schema:

  - EFI (Fat32)
  - BootA (ext4)
  - BootB (ext4)
  - RootfsA (ext4)
  - RootfsB (ext4)
  - /factory (ext4)
  - /data (ext4)

- Add SELinux to the image and set it in permissive mode
- Integrate Mender and ensure updates work
- Add uEFI Secureboot
- Add LUKS with auto-decryption

Perhaps the order of operations wasn’t perfect, but in the end, the
image works and updates properly.

| This is the first blog post in a series detailing how to integrate all
  of the above for a generic x64 image.
| This guide is a great place to start for integrating these features
  into your own image!

Also, there is a link at the bottom of the post for our
meta-amarula-solutions-demo-images github page if you want to dive right
in and start building images immediately! [1]

Why Secureboot?
---------------

| The EU Cyber Resilience Act (CRA) mandates that manufacturers
  “implement secure boot processes verifying the integrity of software
  before execution.”
| The easiest way to deal with this requirement on a X64 device is to
  integrate secureboot into the image using meta-secure-core from
  Wind-River (https://github.com/Wind-River/meta-secure-core) and the
  meta-efi-secure-boot layer.

Problems:
---------

- The documentation for meta-secure-core assumes that you already know a
  lot about Secureboot, module signing, making your own user keys, what
  SELoader/Grub/MokUtil/etc are. For a new user, this is daunting, and
  leads to a lot of frustration.
- Blog posts and examples of how to implement meta-secure-core are
  non-existent or out of date.
- For security purposes, the customer needs to provide their own signing
  keys that we never created.

Solutions:
----------

Let’s start with the basics:

- What is uEFI Secureboot?

  - uEFI Secureboot is a setting in the uEFI. When enabled, the uEFI
    verifies firmware images (such as bootloaders) with certificates
    stored in the uEFI. If the firmware image isn’t signed against a
    certificate stored in the uEFI, then the image fails to load, and
    the boot process stops!

- How do we load certificates into the uEFI?

  - Set Secureboot in the uEFI to enforcing
  - Remove all installed certificates
    **This step is crucial! When all certificates are removed AND uEFI
    Secureboot is set to enforcing, then the uEFI Secureboot is et to a
    special “SetupMode” where it is possible to enroll Secureboot
    certificates into the uEFI!**

- Using grub with meta-secure-core, a small amount of logic is
  automatically prepended before the first entry to check if “SetupMode”
  is active, and if so, automatically provisions the certificates and
  reboots the device.[2]

Building an image with secureboot using Yocto Wrynose
-----------------------------------------------------

The image requires the following:

- Bitbake (https://git.openembedded.org/bitbake)
- openembedded-core (https://git.openembedded.org/openembedded-core)
- meta-openembedded (https://git.openembedded.org/meta-openembedded)

  - meta-oe
  - meta-perl

- meta-secure-core (https://github.com/Wind-River/meta-secure-core.git)

  - meta-efi-secure-boot
  - meta-signing-key

With the above layers checked out and in the same directory, enabling
secureboot is straightforward:

- ``source openembedded-core/oe-init-build-env``

- Setup BBLAYERS in conf/bblayers.conf as such:

  | BBLAYERS ?= ”
  | ${TOPDIR}/../openembedded-core/meta
  | ${TOPDIR}/../meta-openembedded/meta-oe
  | ${TOPDIR}/../meta-openembedded/meta-perl
  | ${TOPDIR}/../meta-secure-core/meta-efi-secure-boot
  | ${TOPDIR}/../meta-secure-core/meta-secure-core-common
  | ${TOPDIR}/../meta-secure-core/meta-signing-key
  | ”

- Add the following to ``conf/local.conf``:

  .. rubric:: UEFI secureboot settings
     :name: uefi-secureboot-settings

  PACKAGE_CLASSES = “package_rpm” DISTRO_FEATURES:remove = “efi”
  DISTRO_FEATURES:append = ” efi-secure-boot modsign” GRUB_SIGN_VERIFY =
  “1” UEFI_SELOADER = “0” UEFI_SB = “1” USER_KEY_SHOW_VERBOSE ?= “1”
  SIGNING_MODEL = “sample”

- See [3] for why UEFI_SELOADER is diabled.

- secure-core-image uses rpm’s for signature/security purposes

- Run ``bitbake secure-core-image``

However, doing all of these steps manually can be a pain, and
reproducibility makes everything much nicer. The go-to solution for
setting all of this up is the kas utility.

Below is an example of a kas-file that will do all of the above for you
in one simple step:

::

   header:
     version: 20
   distro: nodistro
   target:
     - secure-core-image
   repos:
     bitbake:
       url: "https://git.openembedded.org/bitbake"
       branch: 2.18
       signed: false
       layers:
         .: disabled
     openembedded-core:
       url: "https://git.openembedded.org/openembedded-core"
       branch: wrynose
       signed: false
       layers:
         meta:
         meta-selftest:
     meta-openembedded:
       url: "https://git.openembedded.org/meta-openembedded"
       branch: wrynose
       signed: false
       layers:
         meta-oe:
         meta-perl:
     meta-secure-core:
       url: "https://github.com/Wind-River/meta-secure-core.git"
       branch: wrynose
       signed: false
       layers:
         meta-efi-secure-boot:
         meta-secure-core-common:
         meta-signing-key:
   local_conf_header:
     uefi-secure-boot: |
       DISTRO_FEATURES:append = " efi-secure-boot modsign"
       DISTRO_FEATURES:remove = "efi"
       EFI_PROVIDER = "grub-efi"
       MACHINE_FEATURES_NATIVE:append = " efi"
       MACHINE_FEATURES:append = " efi"
       GRUB_SIGN_VERIFY = "1"
       INITRAMFS_IMAGE = "secure-core-image-initramfs"
       PACKAGE_CLASSES = "package_rpm"
       IMAGE_INSTALL:append = " kernel-image-bzimage"
       UEFI_SB = "1"
       UEFI_SELOADER = "0"
     qemu-fixups: |
       IMAGE_INSTALL:append = " ovmf-shell-efi"
       IMAGE_FSTYPES += " wic"
       QB_DEFAULT_FSTYPE = "wic"

- Save the file, in our example, we will name it
  **secure-core-image.yml** and place the file in a top-level kas
  directory for oganization purposes.
- After installing kas, an image can be built with a single command:

  - ``kas build kas/secure-core-image.yml``

- Images are found in build/tmp/deploy/images/qemux86-64/

Running the image in a qemu environment is as easy as
``runqemu secure-core-image ovmf.secboot kvm``

Notes:

- meta-secure-core auto-sets the root password to “toor”
- Once logged in as root, ``mokutil --sb-state`` should output
  “SecureBoot enabled”

Putting it together
-------------------

| While using a kas file with a local_conf_header is convinent, it also
  isn’t well suited for a professional setup.
| Instead, it’s best to make your own meta-layer with a custom distro on
  top of Yocto.
| Check out the meta-amarula-solutions-demo-images github page linked
  below for an example of how to do just that.

Building the demo image is as easy as:

- git clone
  https://github.com/amarula/meta-amarula-solutions-demo-images.git
- cd meta-amarula-solutions-demo-images
- kas build kas/meta-amarula-solutions-demo-images.yaml
- runqemu secureboot-demo-image ovmf.secboot kvm

Replacing the sample signing SIGNING_MODEL
------------------------------------------

| Obviously, it is not a good idea to use sample certificates in
  production! Luckily, meta-secure-core has a bash script to generate
  certificates for you called “create-user-key-store.sh” located at
  meta-signing-key/scripts/create-user-key-store.sh.
| However, the script is a bit less than intuitive to use. A script I
  wrote to use it is below:

::

   #!/usr/bin/env bash
   set -e
   EMAIL="support@mycompany.com"
   PASSWORD="mycompanysupersecretpassword"
   create_user_key_store() {
       ./create-user-key-store.sh \
           -d ./${1}/secureboot \
           -c "demo ${1} Signing Key" \
           -n "demo-${1}-SecureCore" \
           -m "${EMAIL}" \
           -rp "${PASSWORD}" \
           -bgp "${PASSWORD}" \
           -bp "${PASSWORD}" \
           -bn "demo-${1}-Bootloader" \
           -bm "${EMAIL}" \
           -ip "${PASSWORD}" \
           --days 9125
   }
   create_user_key_store "secureboot-demo"

| Saving and running the script in the meta-signing-key/scripts
  generates a secureboot-demo directory with
| custom certificates in a directory tree that meta-secure-core expects.

It is advised to move the new directory to your custom meta layer and do
the following:

- Adjust the MASTER_KEYS_DIR path to match the new directory
- Include the keys.conf file in your image.bb or build/conf/local.conf
  file
- Change ``SIGNING_MODEL = "sample"`` to ``SIGNING_MODEL = "user"``

Now you have the basics of secureboot with grub2 and Yocto Wrynose!
Congratulations!

1: https://github.com/amarula/meta-amarula-solutions-demo-images

2:
https://github.com/Wind-River/meta-secure-core/blob/master/meta-efi-secure-boot/recipes-bsp/grub/grub-efi/efi-secure-boot.inc

3:
https://github.com/Wind-River/meta-secure-core/commit/6d83fbf86fee43ca6510208f7470b04419d4333b
