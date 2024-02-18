Optee Demo Applications
#######################


First we clone the repo

::

   git clone https://github.com/linaro-swg/optee_examples.git
    
    
   cd optee_examples
    
    
Set cross compile and optee specific environment variables

::

   cat > optee_test_env.sh
    
   export PATH=/home/shyam/buildroot/output/host/opt/ext-toolchain/bin:$PATH
   export TA_DEV_KIT_DIR=/home/shyam/optee_os/out/arm-plat-imx/export-ta_arm32
   export OPTEE_CLIENT_EXPORT=/home/shyam/optee_client/out/export
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export TEEC_EXPORT=/home/shyam/optee_client/out/export
   export HOST_CROSS_COMPILE=arm-linux-gnueabihf-
   export TA_CROSS_COMPILE=arm-linux-gnueabihf-
    
   source optee_test_env.sh
    
Build examples

::

   ARCH=arm make
    
    
Now, copy optee client side application in sd card

::

   cp -vrf out/ca/* /path to sd card mount directory/
    
    
Now, copy Optee Trusted Application in sdcard rootfs /lib/optee_armz

::

   cp -vrf out/ta/* /path to sdcard mount directory/lib/optee_armtz/


Insert the sd card and `boot linux with optee <https://wiki.amarulasolutions.com/optee/index.html>`_

Run tee-supplicant

::

   tee-supplicant &
    
    
Run optee client side applications starting with prefix optee_example_*
   
::

   /optee_example_hello_world
   D/TA:  TA_CreateEntryPoint:39 has been called
   D/TA:  TA_OpenSessionEntryPoint:68 has been called
   I/TA: Hello World!
   Invoking TA to increment 42
   D/TA:  inc_value:105 has been called
   I/TA: Got value: 42 from NW
   I/TA: Increase value to: 43
   TA incremented value to 43
   I/TA: Goodbye!
   D/TA:  TA_DestroyEntryPoint:50 has been called
