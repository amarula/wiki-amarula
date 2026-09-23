#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
#
# h264parse.py - parse the SPS, PPS and slice headers of an H.264 stream, and
# work out which field widths the encoder actually used.
#
# Usage:  h264parse.py <file> [--nal N] [--poc-type N] [--fnum-bits N]
#
# Answers: "why does the decoder misread the slice header?"
#
# When a hardware encoder writes the slice header itself, its idea of the
# parameter set fields can differ from the SPS that goes into the stream.  The
# symptom is a field near the end of the slice header decoding to nonsense --
# for this driver it was `deblocking_filter_idc 18 out of range`, which is four
# bits further along than it should be, because the encoder wrote no
# pic_order_cnt_lsb while the SPS said to expect one.
#
# Parsing with the SPS's own values reproduces the failure; parsing with the
# encoder's actual assumption makes every field sane.  The script tries the
# alternatives for you and shows which combination is self-consistent, which
# turns a guess into a measurement.
#
# Overrides:
#   --poc-type N    assume pic_order_cnt_type N in the slice header
#   --fnum-bits N   assume frame_num is N bits wide
#
# Sampling the pixel data is a separate question - see doc/verification.md.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nals import detect_framing, iter_annexb, iter_avc  # noqa: E402

# Profiles that carry chroma_format_idc and the scaling lists.
HIGH_PROFILES = (100, 110, 122, 244, 44, 83, 86, 118, 128, 138, 139, 134, 135)

NON_IDR_SLICE = 1
IDR_SLICE = 5
SPS = 7
PPS = 8


class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def u(self, n):
        value = 0
        for _ in range(n):
            byte = self.data[self.pos >> 3]
            value = (value << 1) | ((byte >> (7 - (self.pos & 7))) & 1)
            self.pos += 1
        return value

    def ue(self):
        zeros = 0
        while self.u(1) == 0:
            zeros += 1
        return (1 << zeros) - 1 + (self.u(zeros) if zeros else 0)

    def se(self):
        value = self.ue()
        return (value + 1) // 2 if value & 1 else -(value // 2)


def unescape(payload):
    """Remove emulation prevention bytes (00 00 03 -> 00 00)."""
    out, i = bytearray(), 0
    while i < len(payload):
        if i + 2 < len(payload) and payload[i] == 0 and payload[i + 1] == 0 \
                and payload[i + 2] == 3:
            out += payload[i:i + 2]
            i += 3
        else:
            out.append(payload[i])
            i += 1
    return bytes(out)


def _skip_scaling_list(br, size):
    last, next_scale = 8, 8
    for _ in range(size):
        if next_scale:
            next_scale = (last + br.se() + 256) % 256
        last = last if next_scale == 0 else next_scale


def parse_sps(payload):
    br = BitReader(payload)
    sps = {}
    sps["profile_idc"] = br.u(8)
    br.u(8)  # constraint flags
    sps["level_idc"] = br.u(8)
    sps["sps_id"] = br.ue()

    sps["chroma_format_idc"] = 1
    sps["bit_depth_luma_minus8"] = 0
    sps["bit_depth_chroma_minus8"] = 0

    if sps["profile_idc"] in HIGH_PROFILES:
        sps["chroma_format_idc"] = br.ue()
        if sps["chroma_format_idc"] == 3:
            br.u(1)  # separate_colour_plane_flag
        sps["bit_depth_luma_minus8"] = br.ue()
        sps["bit_depth_chroma_minus8"] = br.ue()
        br.u(1)  # qpprime_y_zero_transform_bypass_flag
        if br.u(1):  # seq_scaling_matrix_present_flag
            for i in range(12 if sps["chroma_format_idc"] == 3 else 8):
                if br.u(1):
                    _skip_scaling_list(br, 16 if i < 6 else 64)

    sps["log2_max_frame_num_minus4"] = br.ue()
    sps["pic_order_cnt_type"] = br.ue()
    if sps["pic_order_cnt_type"] == 0:
        sps["log2_max_pic_order_cnt_lsb_minus4"] = br.ue()
    elif sps["pic_order_cnt_type"] == 1:
        br.u(1)
        br.se()
        br.se()
        for _ in range(br.ue()):
            br.se()

    sps["max_num_ref_frames"] = br.ue()
    br.u(1)  # gaps_in_frame_num_value_allowed_flag
    sps["width_mbs"] = br.ue() + 1
    sps["height_units"] = br.ue() + 1
    frame_mbs_only = br.u(1)
    sps["frame_mbs_only_flag"] = frame_mbs_only
    if not frame_mbs_only:
        br.u(1)
    br.u(1)  # direct_8x8_inference_flag
    sps["frame_cropping"] = br.u(1)
    return sps


def parse_pps(payload):
    br = BitReader(payload)
    pps = {}
    pps["pps_id"] = br.ue()
    pps["sps_id"] = br.ue()
    pps["entropy_coding_mode"] = br.u(1)
    pps["bottom_field_pic_order_in_frame_present"] = br.u(1)
    groups = br.ue() + 1
    pps["num_slice_groups"] = groups
    if groups > 1:
        raise ValueError("slice groups are not handled by this parser")
    pps["num_ref_idx_l0_default_active"] = br.ue() + 1
    pps["num_ref_idx_l1_default_active"] = br.ue() + 1
    pps["weighted_pred"] = br.u(1)
    br.u(2)  # weighted_bipred_idc
    pps["pic_init_qp_minus26"] = br.se()
    br.se()  # pic_init_qs_minus26
    pps["chroma_qp_index_offset"] = br.se()
    pps["deblocking_filter_control_present"] = br.u(1)
    br.u(1)  # constrained_intra_pred_flag
    pps["redundant_pic_cnt_present"] = br.u(1)
    return pps


def parse_slice(payload, sps, pps, nal_type, poc_type=None, fnum_bits=None,
                poc_lsb_bits=None):
    """Parse a slice header, optionally against a different assumption."""
    br = BitReader(payload)
    fields = []

    if poc_type is None:
        poc_type = sps["pic_order_cnt_type"]
    if fnum_bits is None:
        fnum_bits = sps["log2_max_frame_num_minus4"] + 4
    if poc_lsb_bits is None:
        poc_lsb_bits = sps.get("log2_max_pic_order_cnt_lsb_minus4", 0) + 4

    fields.append(("first_mb_in_slice", br.ue()))
    fields.append(("slice_type", br.ue()))
    fields.append(("pic_parameter_set_id", br.ue()))
    fields.append(("frame_num", br.u(fnum_bits)))
    if nal_type == IDR_SLICE:
        fields.append(("idr_pic_id", br.ue()))
    if poc_type == 0:
        fields.append(("pic_order_cnt_lsb", br.u(poc_lsb_bits)))
    if pps["redundant_pic_cnt_present"]:
        fields.append(("redundant_pic_cnt", br.ue()))
    fields.append(("dec_ref_pic_marking", br.u(2)))
    fields.append(("slice_qp_delta", br.se()))
    if pps["deblocking_filter_control_present"]:
        idc = br.ue()
        fields.append(("deblocking_filter_idc", idc))
        if idc != 1:
            fields.append(("slice_alpha_c0_offset_div2", br.se()))
            fields.append(("slice_beta_offset_div2", br.se()))
    fields.append(("header_bits_consumed", br.pos))
    return fields


def find_nals(data):
    framing = detect_framing(data)
    walker = iter_annexb(data) if framing == "annexb" else iter_avc(data)
    return framing, [(off, size) for off, size, _ in walker]


def load(path, nal_index=None):
    data = open(path, "rb").read()
    framing, nals = find_nals(data)
    sps = pps = None
    slices = []
    for off, size in nals:
        if size < 1:
            continue
        header = data[off]
        nal_type = header & 0x1f
        body = unescape(data[off + 1:off + size])
        if nal_type == SPS and sps is None:
            sps = parse_sps(body)
        elif nal_type == PPS and pps is None:
            pps = parse_pps(body)
        elif nal_type in (NON_IDR_SLICE, IDR_SLICE):
            slices.append((nal_type, body))
    return framing, sps, pps, slices


def signals(fields, pps):
    """What looks wrong, or merely unusual, about a parse.

    These are heuristics, not rules: a slice_qp_delta of 1 is legal, it is just
    not what an encoder writes for a flat test pattern.  The point is to rank
    candidate field widths against each other, not to pronounce a verdict -
    a decoder is the only authority on that.
    """
    values = dict(fields)
    found = []

    if values.get("first_mb_in_slice") != 0:
        found.append("first_mb_in_slice is not 0")
    if values.get("deblocking_filter_idc", 0) not in (0, 1, 2):
        found.append("deblocking_filter_idc out of range")
    if values.get("slice_type", 0) > 9:
        found.append("slice_type out of range")
    if values.get("pic_parameter_set_id") != pps["pps_id"]:
        found.append("pic_parameter_set_id does not match the PPS")
    if values.get("idr_pic_id", 0) != 0:
        found.append("idr_pic_id is not 0, which encoders normally write")
    return found


def report(fields, label, pps):
    found = signals(fields, pps)
    tail = f"{len(found)} signal(s)" if found else "nothing unusual"
    print(f"--- {label} ---  {tail}")
    for name, value in fields:
        mark = ""
        if name == "deblocking_filter_idc" and value not in (0, 1, 2):
            mark = "   <-- out of range"
        print(f"      {name:32s} {value}{mark}")
    for reason in found:
        print(f"      note: {reason}")
    print()
    return found


def main(argv):
    if len(argv) < 2:
        print("usage: h264parse.py <file> [--poc-type N] [--fnum-bits N]")
        return 1

    path = argv[1]
    override_poc = override_fnum = None
    if "--poc-type" in argv:
        override_poc = int(argv[argv.index("--poc-type") + 1])
    if "--fnum-bits" in argv:
        override_fnum = int(argv[argv.index("--fnum-bits") + 1])

    framing, sps, pps, slices = load(path)
    print(f"{path}: framing={framing}")
    if not sps:
        print("no SPS found")
        return 1
    if not slices:
        print("SPS found but no slice NAL units: the stream carries no picture")
        return 1

    print(f"SPS profile_idc={sps['profile_idc']} poc_type={sps['pic_order_cnt_type']} "
          f"log2_max_frame_num_minus4={sps['log2_max_frame_num_minus4']} "
          f"({sps['log2_max_frame_num_minus4'] + 4}-bit frame_num) "
          f"{sps['width_mbs'] * 16}x{sps['height_units'] * 16}")
    print(f"PPS deblocking_filter_control_present="
          f"{pps['deblocking_filter_control_present']}")
    print()

    nal_type, body = slices[0]
    native_fnum = sps["log2_max_frame_num_minus4"] + 4
    candidates = []

    if override_poc is not None or override_fnum is not None:
        poc = sps["pic_order_cnt_type"] if override_poc is None else override_poc
        fnum = native_fnum if override_fnum is None else override_fnum
        candidates.append((f"poc_type={poc}, frame_num={fnum} bits",
                           parse_slice(body, sps, pps, nal_type,
                                       poc_type=poc, fnum_bits=fnum)))
    else:
        native = parse_slice(body, sps, pps, nal_type)
        candidates.append((f"as the SPS describes it (poc_type="
                           f"{sps['pic_order_cnt_type']}, frame_num="
                           f"{native_fnum} bits)", native))

        if signals(native, pps):
            print("The slice header does not parse as the SPS describes it.\n"
                  "Trying the field widths a hardware encoder may have "
                  "assumed instead:\n")
            tried = {(sps["pic_order_cnt_type"], native_fnum)}
            for poc in (0, 2):
                for fnum in sorted({native_fnum, 12, 16}):
                    if (poc, fnum) in tried:
                        continue
                    tried.add((poc, fnum))
                    try:
                        alt = parse_slice(body, sps, pps, nal_type,
                                          poc_type=poc, fnum_bits=fnum)
                    except Exception as exc:  # ran off a short header
                        print(f"--- poc_type={poc}, frame_num={fnum} bits --- "
                              f"failed: {exc}\n")
                        continue
                    candidates.append((f"poc_type={poc}, frame_num={fnum} bits",
                                       alt))

    scored = [(len(signals(fields, pps)), label, fields)
              for label, fields in candidates]
    for _, label, fields in scored:
        report(fields, label, pps)

    if len(scored) > 1:
        best = min(scored, key=lambda item: (item[0], item[1]))
        print(f"Most plausible: {best[1]}.")
        print("These are heuristics - decode the stream to be sure.")
    return 0 if scored[0][0] == 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
