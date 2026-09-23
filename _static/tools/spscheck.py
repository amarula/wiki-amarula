#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
#
# spscheck.py - dump the fields of an SPS and check them against the limits the
# kernel enforces when a stateless encoder is handed a parameter set.
#
# Usage:  spscheck.py <file>
#
# Answers: "why did VIDEO_S_EXT_CTRLS fail with EINVAL?"
#
# Setting V4L2_CID_STATELESS_H264_SPS goes through validate_new() in
# drivers/media/v4l2-core/v4l2-ctrls-core.c, which rejects a handful of field
# values outright.  When it does, the ioctl fails, and the failure surfaces at
# the GStreamer level as:
#
#     Driver does not support the selected stream
#
# which says nothing about which field it disliked.  The most common cause by
# far is a stream whose pixel format the hardware cannot decode: a 4:4:4 stream
# from an encoder that was handed a 4:4:4 input has profile_idc 244 and
# chroma_format_idc 3, and the decoder wants 4:2:0.  That is a pipeline mistake,
# not a driver one - see doc/verification.md.
#
# The limits below are transcribed from that function; the comments name the
# rule so that a mismatch can be traced back to the source.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h264parse import load  # noqa: E402

# V4L2_H264_REF_LIST_LEN, from include/uapi/linux/v4l2-controls.h:
# 2 * V4L2_H264_NUM_DPB_ENTRIES.
REF_LIST_LEN = 32

PROFILE_NAMES = {
    66: "Baseline", 77: "Main", 88: "Extended", 100: "High",
    110: "High 10", 122: "High 4:2:2", 244: "High 4:4:4 Predictive",
}


def check_driver(sps):
    """Rules from hantro_try_ctrl() in hantro_drv.c.

    These run in addition to the generic validator below, and they are stricter
    about pixel format: the hardware decodes 4:2:0 8-bit, so any other chroma
    format or bit depth is refused here even though the validator would allow
    it.  This is the layer that rejects a 4:4:4 stream.
    """
    failures = []

    if sps["chroma_format_idc"] > 1:
        failures.append(("chroma_format_idc > 1 (only 4:0:0 and 4:2:0)",
                         sps["chroma_format_idc"], "<= 1"))
    if sps["bit_depth_luma_minus8"] != sps["bit_depth_chroma_minus8"]:
        failures.append(("luma and chroma bit depth mismatch",
                         sps["bit_depth_luma_minus8"], "== chroma"))
    if sps["bit_depth_luma_minus8"] != 0:
        failures.append(("bit_depth_luma_minus8 != 0 (only 8-bit)",
                         sps["bit_depth_luma_minus8"], "== 0"))
    return failures


def check_validator(sps):
    """Return the list of (rule, value, limit) a value violates."""
    failures = []

    profile = sps["profile_idc"]
    chroma = sps["chroma_format_idc"]

    if profile < 122 and chroma > 1:
        failures.append(("chroma_format_idc > 1 needs profile_idc >= 122, "
                         "have profile_idc", profile, ">= 122"))
    if profile < 244 and chroma > 2:
        failures.append(("chroma_format_idc > 2 needs profile_idc >= 244, "
                         "have profile_idc", profile, ">= 244"))
    if chroma > 3:
        failures.append(("chroma_format_idc > 3", chroma, "<= 3"))
    if sps["bit_depth_luma_minus8"] > 6:
        failures.append(("bit_depth_luma_minus8 > 6",
                         sps["bit_depth_luma_minus8"], "<= 6"))
    if sps["bit_depth_chroma_minus8"] > 6:
        failures.append(("bit_depth_chroma_minus8 > 6",
                         sps["bit_depth_chroma_minus8"], "<= 6"))
    if sps["log2_max_frame_num_minus4"] > 12:
        failures.append(("log2_max_frame_num_minus4 > 12",
                         sps["log2_max_frame_num_minus4"], "<= 12"))
    if sps["pic_order_cnt_type"] > 2:
        failures.append(("pic_order_cnt_type > 2", sps["pic_order_cnt_type"],
                         "<= 2"))
    if sps.get("log2_max_pic_order_cnt_lsb_minus4", 0) > 12:
        failures.append(("log2_max_pic_order_cnt_lsb_minus4 > 12",
                         sps["log2_max_pic_order_cnt_lsb_minus4"], "<= 12"))
    if sps["max_num_ref_frames"] > REF_LIST_LEN:
        failures.append(("max_num_ref_frames > V4L2_H264_REF_LIST_LEN",
                         sps["max_num_ref_frames"], f"<= {REF_LIST_LEN}"))
    return failures


def main(argv):
    if len(argv) < 2:
        print("usage: spscheck.py <file>")
        return 1

    path = argv[1]
    _, sps, _, _ = load(path)
    if not sps:
        print(f"{path}: no SPS found")
        return 1

    profile = sps["profile_idc"]
    print(f"{path}")
    print(f"  profile_idc                  {profile}"
          f"{'  (' + PROFILE_NAMES[profile] + ')' if profile in PROFILE_NAMES else ''}")
    print(f"  level_idc                    {sps['level_idc']}")
    print(f"  chroma_format_idc            {sps['chroma_format_idc']}"
          f"  ({'4:2:0' if sps['chroma_format_idc'] == 1 else 'not 4:2:0'})")
    print(f"  bit_depth_luma_minus8        {sps['bit_depth_luma_minus8']}")
    print(f"  bit_depth_chroma_minus8      {sps['bit_depth_chroma_minus8']}")
    print(f"  log2_max_frame_num_minus4    {sps['log2_max_frame_num_minus4']}"
          f"  ({sps['log2_max_frame_num_minus4'] + 4}-bit frame_num)")
    print(f"  pic_order_cnt_type           {sps['pic_order_cnt_type']}")
    print(f"  log2_max_pic_order_cnt_lsb_minus4 "
          f"{sps.get('log2_max_pic_order_cnt_lsb_minus4', '-')}")
    print(f"  max_num_ref_frames           {sps['max_num_ref_frames']}")
    print(f"  coded size                   {sps['width_mbs'] * 16}x"
          f"{sps['height_units'] * 16}")
    print()

    driver_failures = check_driver(sps)
    validator_failures = check_validator(sps)

    if driver_failures:
        print("Refused by the driver, hantro_try_ctrl() "
              "(hantro_drv.c:263):")
        for rule, value, limit in driver_failures:
            print(f"  {rule}: {value}, needs {limit}")
        print()

    if validator_failures:
        print("Refused by the kernel's generic validator, validate_new() "
              "(v4l2-ctrls-core.c):")
        for rule, value, limit in validator_failures:
            print(f"  {rule}: {value}, needs {limit}")
        print()

    if not driver_failures and not validator_failures:
        print("Accepted by both the driver and the kernel validator.")
        return 0

    print("Setting V4L2_CID_STATELESS_H264_SPS will fail with EINVAL, and "
          "userspace reports it as \"Driver does not support the selected "
          "stream\".")
    print()
    if driver_failures:
        print("The driver's rules are about pixel format, so the usual cause "
              "is the encoder's input rather than the encoder: a 4:4:4 or "
              "10-bit source produces a stream the decoder cannot take.  Pin "
              "the format before the encoder, e.g. "
              "video/x-raw,format=I420.")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
