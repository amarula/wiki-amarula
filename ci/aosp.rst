AOSP Android build project
***************************

Android is multi-configuration Jenkins project. We need to combine repo plugin with matrix plugin.

.. image:: /images/android_aosp_pipeline.png

Important options are:

-  Use custom child workspace in Advanced Project Options
-  Definition of the correct repo manifest as shown in the follow picture
-  Definition of build matrix in order to have the output of all the artifacts

.. image:: /images/android_aosp_pipeline_2.png

Execution shell needs to take in account the variant for clean the project and for the output directory.

.. container:: code panel pdl conf-macro output-block

   .. container:: codeContent panelContent pdl

      .. code:: syntaxhighlighter-pre

         #!/bin/bash -xe

         OUT_DIR=out_$BuildVariant
         export OUT_DIR

         source build/envsetup.sh
         lunch rtc700m-$BuildVariant

         make clean

         # export WITHOUT_HOST_CLANG=true
         CPUS=$(getconf _NPROCESSORS_ONLN)
         echo "Build on " $CPUS " cores machine"
         make -j $CPUS
