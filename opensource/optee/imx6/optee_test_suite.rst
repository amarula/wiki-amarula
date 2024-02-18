OP-Tee Test suite
#################

optee client
************

.. note::

   Before building optee test suite, make sure you have already built the optee os



Optee client runs on linux side which provides tee-supplicant
clone optee client repo

::

   git clone https://github.com/OP-TEE/optee_client.git

   cd optee_client
 
Setenv cross compile environment

::

   export CROSS_COMPILE=arm-linux-gnueabihf-
   export PATH=/home/shyam/buildroot/output/host/opt/ext-toolchain/bin:$PATH
   
   make
 
Copy all files from out/export/ to sdcard rootfs

::

   cp -vrf out/export/* /path to sd card mount directory/


Optee Test suite
****************

Optee test suite provides benchmark and regression test suite.
 
Clone optee_test repo

::

   git clone https://github.com/OP-TEE/optee_test.git
   
   cd optee_test
 
Set cross compile and optee specific environment variables

::

   export TA_DEV_KIT_DIR=/path to /optee_os/out/arm-plat-imx/export-ta_arm32
   export OPTEE_CLIENT_EXPORT=/path to /optee_client/out/export
   export CROSS_COMPILE_HOST=arm-linux-gnueabihf-
   export CROSS_COMPILE_TA=arm-linux-gnueabihf-
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export PATH=/path to toolchain/bin:$PATH
 
Now we execute make command with `COMPILE_NS_USER` flag. For imx6qdl its 32

::

   ARCH=arm make COMPILE_NS_USER=32
 
Copy all *.ta *.elf in out/* to sd card rootfs /lib/optee_armtz/

::

   cp -vrf `find out/ -name *.ta` /path to sdcard mount directory/lib/optee_armtz/
   cp -vrf `find out/ -name *.elf` /path to sdcard mount directory/lib/optee_armtz/
   cp -vf out/xtest/xtest /path to sdcard mount directory/bin/


Now, insert the sd card and  boot linux with optee.

First run tee-supplicant

::

   tee-supplicant &
 
 
First we run benchmark test with level 0, means minimal tests

::

   xtest -t benchmark
 
 
Test Results:
*************

::

   benchmark_1001 TEE Trusted Storage Performance Test (WRITE)
   -----------------+---------------+----------------
   Data Size (B)    | Time (s)      | Speed (kB/s)
   -----------------+---------------+----------------
   256              |    0.040      |    6.250
   512              |    0.055      |    9.091
   1024             |    0.055      |   18.182
   2048             |    0.100      |   20.000
   4096             |    0.243      |   16.461
   16384            |    1.086      |   14.733
   524288           |   46.275       |   11.064
   1048576          |   95.700      |   10.700
   -----------------+---------------+----------------
   benchmark_1001 OK
    
   * benchmark_1002 TEE Trusted Storage Performance Test (READ)                                   
   -----------------+---------------+----------------
   Data Size (B)    | Time (s)      | Speed (kB/s)
   -----------------+---------------+----------------
   256              |    0.001      |  250.000
   512              |    0.001      |  500.000
   1024             |    0.001      | 1000.000
   2048             |    0.003      |  666.667
   4096             |    0.008      |  500.000
   16384            |    0.033      |  484.848
   524288           |    1.027       |  498.539
   1048576          |    2.035      |  503.194
   -----------------+---------------+----------------
   benchmark_1002 OK
    
   * benchmark_1003 TEE Trusted Storage Performance Test (REWRITE)                                
   -----------------+---------------+----------------
   Data Size (B)    | Time (s)      | Speed (kB/s)
   -----------------+---------------+----------------
   256              |    0.042      |    5.952
   512              |    0.042      |   11.905
   1024             |    0.043      |   23.256
   2048             |    0.286      |    6.993
   4096             |    0.212      |   18.868
   16384            |    0.991      |   16.145
   524288           |   49.030      |   10.443
   1048576          |  102.586      |    9.982
   -----------------+---------------+----------------
   benchmark_1003 OK
    
   * benchmark_2001 TEE SHA Performance test (TA_SHA_SHA1)
   min=262us max=588.333us mean=274.617us stddev=29.5489us (cv 10.76%) (3.55608MiB/s)
   benchmark_2001 OK
    
   * benchmark_2002 TEE SHA Performance test (TA_SHA_SHA226)
   min=411.333us max=763.667us mean=430.237us stddev=36.6874us (cv 8.52726%) (9.07931MiB/s)
   benchmark_2002 OK
    
   * benchmark_2011 TEE AES Performance test (TA_AES_ECB)
   min=319us max=638.334us mean=332.388us stddev=30.8239us (cv 9.27346%) (2.93802MiB/s)
   benchmark_2011 OK
    
   * benchmark_2012 TEE AES Performance test (TA_AES_CBC)
   min=357us max=758us mean=373.566us stddev=34.0887us (cv 9.12523%) (2.61417MiB/s)
   benchmark_2012 OK
    
    
   Result of testsuite benchmark:
   benchmark_1001 OK
   benchmark_1002 OK
   benchmark_1003 OK
   benchmark_2001 OK
   benchmark_2002 OK
   benchmark_2011 OK
   benchmark_2012 OK
    
   24 subtests of which 0 failed
   7 test cases of which 0 failed
   0 test case was skipped
   TEE test application done!
 
 
 
 
 
Now, we run benchmark test with level 15, means all the tests

::

   xtest -t benchmark -l 15
   -----------------+---------------+----------------
    Data Size (B)   | Time (s)      | Speed (kB/s) 
   -----------------+---------------+----------------
         256        |    0.052      |    4.808
         512        |    0.052      |    9.615
        1024        |    0.036      |   27.778
        2048        |    0.098      |   20.408
        4096        |    0.709      |    5.642
       16384        |    0.968      |   16.529
      524288        I/TA: command id: 0, test data size: 256, chunk size: 1024
   |   46.708       |   10.962
     1048576        |   97.244      |   10.530
   -----------------+---------------+----------------
     benchmark_1001 OK
     
   * benchmark_1002 TEE Trusted Storage Performance Test (READ)
   I/TA: start: 3318.376(s), stop: 3318.377(s), delta: 1(ms)
   I/TA: command id: 0, test data size: 512, chunk size: 1024
   I/TA: start: 3318.637(s), stop: 3318.639(s), delta: 2(ms)
   I/TA: command id: 0, test data size: 1024, chunk size: 1024
   I/TA: start: 3318.915(s), stop: 3318.917(s), delta: 2(ms)
   I/TA: command id: 0, test data size: 2048, chunk size: 1024
   I/TA: start: 3319.255(s), stop: 3319.258(s), delta: 3(ms)
   I/TA: command id: 0, test data size: 4096, chunk size: 1024
   I/TA: start: 3319.733(s), stop: 3319.741(s), delta: 8(ms)
   I/TA: command id: 0, test data size: 16384, chunk size: 1024
   I/TA: start: 3320.893(s), stop: 3320.925(s), delta: 32(ms)
   I/TA: command id: 0, test data size: 524288, chunk size: 1024
   I/TA: start: 3367.678(s), stop: 3368.727(s), delta: 1049(ms)
   I/TA: command id: 0, test data size: 1048576, chunk size: 1024
   I/TA: start: 3469.15(s), stop: 3471.55(s), delta: 2040(ms)
   -----------------+---------------+----------------
    Data Size (B)   | Time (s)      | Speed (kB/s) 
   -----------------+---------------+----------------
         256        |    0.001      |  250.000
         512        |    0.002      |  250.000
        1024        |    0.002      |  500.000
        2048        |    0.003      |  666.667
        4096        |    0.008      |  500.000
       16384        |    0.032      |  500.000
      524288        I/TA: command id: 2, test data size: 256, chunk size: 1024
   |    1.049       |  488.084
     1048576        |    2.040      |  501.961
   -----------------+---------------+----------------
     benchmark_1002 OK
     
   * benchmark_1003 TEE Trusted Storage Performance Test (REWRITE)
   I/TA: start: 3471.361(s), stop: 3471.411(s), delta: 50(ms)
   I/TA: command id: 2, test data size: 512, chunk size: 1024
   I/TA: start: 3471.705(s), stop: 3471.747(s), delta: 42(ms)
   I/TA: command id: 2, test data size: 1024, chunk size: 1024
   I/TA: start: 3472.14(s), stop: 3472.55(s), delta: 41(ms)
   I/TA: command id: 2, test data size: 2048, chunk size: 1024
   I/TA: start: 3472.351(s), stop: 3472.450(s), delta: 99(ms)
   I/TA: command id: 2, test data size: 4096, chunk size: 1024
   I/TA: start: 3472.863(s), stop: 3473.97(s), delta: 234(ms)
   I/TA: command id: 2, test data size: 16384, chunk size: 1024
   I/TA: start: 3474.634(s), stop: 3475.460(s), delta: 826(ms)
   I/TA: command id: 2, test data size: 524288, chunk size: 1024
   I/TA: start: 3521.591(s), stop: 3569.728(s), delta: 48137(ms)
   I/TA: command id: 2, test data size: 1048576, chunk size: 1024
   I/TA: start: 3671.322(s), stop: 3772.377(s), delta: 101055(ms)
   -----------------+---------------+----------------
    Data Size (B)   | Time (s)      | Speed (kB/s) 
   -----------------+---------------+----------------
         256        |    0.050      |    5.000
         512        |    0.042      |   11.905
        1024        |    0.041      |   24.390
        2048        |    0.099      |   20.202
        4096        |    0.234      |   17.094
       16384        |    0.826      |   19.370
      524288        |   48.137      |   10.636
     1048576        |  101.055      |   10.133
   -----------------+---------------+----------------
     benchmark_1003 OK
     
   * benchmark_2001 TEE SHA Performance test (TA_SHA_SHA1)
   min=271us max=629.667us mean=283.53us stddev=28.9001us (cv 10.193%) (3.4443MiB/s)
     benchmark_2001 OK
     
   * benchmark_2002 TEE SHA Performance test (TA_SHA_SHA226)
   min=415.333us max=783.334us mean=435.947us stddev=38.411us (cv 8.81094%) (8.96038MiB/s)
     benchmark_2002 OK
     
   * benchmark_2011 TEE AES Performance test (TA_AES_ECB)
   min=329.667us max=676us mean=346.326us stddev=32.3748us (cv 9.34808%) (2.81978MiB/s)
     benchmark_2011 OK
     
   * benchmark_2012 TEE AES Performance test (TA_AES_CBC)
   min=359.667us max=792us mean=376.213us stddev=32.3281us (cv 8.59304%) (2.59577MiB/s)
     benchmark_2012 OK
   +-----------------------------------------------------
   Result of testsuite benchmark:
   benchmark_1001 OK
   benchmark_1002 OK
   benchmark_1003 OK
   benchmark_2001 OK
   benchmark_2002 OK
   benchmark_2011 OK
   benchmark_2012 OK
   +-----------------------------------------------------
   24 subtests of which 0 failed
   7 test cases of which 0 failed
   0 test case was skipped
   TEE test application done!
 
 
 
Now, we run the regression tests with level[0-15] 15

::

   xtest -t regression -l 15
   +-----------------------------------------------------
   Result of testsuite regression:
   regression_1001 OK
   regression_1002 OK
   regression_1003 OK
   regression_1004 OK
   regression_1005 OK
   regression_1006 OK
   regression_1007 OK
   regression_1008 OK
   regression_1009 OK
   regression_1010 OK
   regression_1011 OK
   regression_1012 OK
   regression_1013 OK
   regression_1015 OK
   regression_1016 OK
   regression_1017 OK
   regression_1018 OK
   regression_1019 OK
   regression_2001 OK
   regression_2002 OK
   regression_2003 OK
   regression_2004 OK
   regression_4001 OK
   regression_4002 OK
   regression_4003 OK
   regression_4004 OK
   regression_4005 OK
   regression_4006 OK
   regression_4007 OK
   regression_4008 OK
   regression_4009 OK
   regression_4010 OK
   regression_4011 OK
   regression_4012 OK
   regression_5006 OK
   regression_6001 OK
   regression_6002 OK
   regression_6003 OK
   regression_6004 OK
   regression_6005 OK
   regression_6006 OK
   regression_6007 OK
   regression_6008 OK
   regression_6009 OK
   regression_6010 OK
   regression_6012 OK
   regression_6013 OK
   regression_6014 OK
   regression_6015 OK
   regression_6016 OK
   regression_6017 OK
   regression_6018 OK
   regression_6019 OK
   regression_6020 OK
   regression_7001 OK
   regression_7002 OK
   regression_7003 OK
   regression_7004 OK
   regression_7005 OK
   regression_7006 OK
   regression_7007 OK
   regression_7008 OK
   regression_7009 OK
   regression_7010 OK
   regression_7013 OK
   regression_7016 OK
   regression_7017 OK
   regression_7018 OK
   regression_7019 OK
   regression_8001 OK
   regression_8002 OK
   regression_8101 OK
   regression_8102 OK
   regression_8103 OK
   +-----------------------------------------------------
   16081 subtests of which 0 failed
   74 test cases of which 0 failed
   0 test case was skipped
   TEE test application done!
  
 
SHA performance testing tool

::

   xtest --aes-perf -v

   Starting test: ECB, encrypt, keysize=128 bits, size=1024 bytes, random=no, in place=no, inner loops=1, loops=5000, warm-up=2 s
   min=302.333us max=694us mean=316.77us stddev=30.7425us (cv 9.70496%) (3.08287MiB/s)
   2-sigma interval: 255.286..378.255us (2.58175..3.82537MiB/s)
 
AES performance testing tool

::

   
   xtest --sha-perf -v

   Starting test: SHA1, size=1024 bytes, random=no, unaligned=no, inner loops=1, loops=5000, warm-up=2 s
   min=261.667us max=588.333us mean=273.777us stddev=27.9708us (cv 10.2167%) (3.567MiB/s)
   2-sigma interval: 217.835..329.718us (2.96181..4.48304MiB/s)
