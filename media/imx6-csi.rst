MIPI-CSI2 OV5640 Camera
#######################

Build
*****

Use buildroot rootfs with below Linux
::
        git clone https://github.com/amarula/linux-amarula
        cd linux-amarula
        git checkout -b imx6-ov5640 origin/imx6-ov5640
        ARCH=arm make imx_v6_v7_defconfig
        ARCH=arm make LOADADDR=0x10008000 uImage dtbs -j 16

Capture
*******

Once Linux boot, prepare media control chart for finding pipeline setups

On target
::
        media-ctl --print-dot > mipi-ov5640.dot

On host
::
        dot -T png -o mipi-ov5640.png mipi-ov5640.dot

.. image:: /images/imx6-csi.png

Configure the pipeline with default format AYUV32/640x480,this can be alter with any other relevant format to testing with.

Setup MC links
::
        media-ctl --links "'ov5640 2-003c':0->'imx6-mipi-csi2':0[1]"
        media-ctl --links "'imx6-mipi-csi2':1->'ipu1_csi0_mux':0[1]"
        media-ctl --links "'ipu1_csi0_mux':2->'ipu1_csi0':0[1]"
        media-ctl --links "'ipu1_csi0':2->'ipu1_csi0 capture':0[1]"

Configure pads
::
        media-ctl --set-v4l2 "'ov5640 2-003c':0[fmt:UYVY2X8/640x480 field:none]"
        media-ctl --set-v4l2 "'imx6-mipi-csi2':1[fmt:UYVY2X8/640x480 field:none]"
        media-ctl --set-v4l2 "'ipu1_csi0_mux':2[fmt:UYVY2X8/640x480 field:none]"
        media-ctl --set-v4l2 "'ipu1_csi0':2[fmt:AYUV32/640x480 field:none]"

Launch the camera with ipu1_csi0 capture
::
         gst-launch-1.0 -v v4l2src device=/dev/video4 ! autovideosink
