Create U-Boot handle sdram timings dtsi from rkbin on RK3399
############################################################

These steps are derived from the instructions supported by Liviu Dudau <liviu@dudau.co.uk> 
and posted here for public usage as per communication.

Example sdram rkbin:
   rk3399_ddr_933MHz_v1.15.bin

0. The binary contains multiple frequency settings, so you will have to choose
   the one you are interested in

1. Convert the RAM frequency into Hz and use the hexadecimal value to search in
   the bin file. Here 933MHz is 933000000, or 0x379c7340. Depending on what you
   use to view the binary, you might have to convert to the little endian format
   (that's the case for hexdump, so search for 40 73 9c 37). To validate that you're
   not looking at some random data, you can check that you only get 2 matches in
   the bin file (one for single rank and one for dual rank). I haven't checked for
   all combinations, but I think there are only 2 versions. Also look for the data
   around the match, some of the values form a fixed pattern (you can diff the
   attached files to find out which ones don't change, but 0x80181219 for example
   is a good value to look for).

2. Figure out where the start of the data is. The pattern is 02 0a 03 02, so from
   your frequency match walk backwards and choose the *second* instance (pattern
   repeats once)

3. Figure out where the end of the data is. Usually, for the first block that matches,
   it will end before the single/dual rank block starts, as they are consecutive.
   For the v1.15 binary, it looks like it is 6044 bytes. The end pattern is 0x01010000
   0x00000000. There might be another 32bit zero value between the blocks.

4. Extract the DDR timings. For this file, I've used the following commands:

   $ dd if=rk3399_ddr_933MHz_v1.15.bin of=ddr_single_933mhz.bin bs=1 skip=51800 count=6044

   $ dd if=rk3399_ddr_933MHz_v1.15.bin of=ddr_dual_933mhz.bin bs=1 skip=57848 count=6044

5. Converted the binaries to text with:

   $ hexdump -v --format '1/4 "%08x "' ddr_single_933mhz.bin > rk3399-sdram-ddr3-single-1866.dtsi

   $ hexdump -v --format '1/4 "%08x "' ddr_dual_933mhz.bin > rk3399-sdram-ddr3-dual-1866.dtsi

6. Insert the start of the DT fragment into each .dtsi file, edit the initial values (don't forget
   that they are in little endian form) to match what the SPL code expects, convert the frequency
   value from the binary back into MHz (line 38 in the attached dtsi files for reference)
