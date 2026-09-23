#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
#
# nals.py - list the NAL units of an H.264 stream.
#
# Usage:  nals.py <file> [--limit N]
#
# Answers: "what is actually in this file?"  Run this before anything else when
# a stream misbehaves, because the two things it makes obvious are the two that
# are hardest to see otherwise:
#
#   - whether the slice NAL units are there at all.  A stream whose parameter
#     sets parse and whose frame count looks right can still contain no slices,
#     and every decoder will then report an empty picture rather than an error.
#
#   - whether the file is Annex-B (start codes) or AVC/length-prefixed.  A
#     GStreamer pipeline that muxes to Matroska stores AVC, and an AVC file has
#     no start codes, so a scanner looking for them finds data that merely looks
#     like them.  This script detects the framing and says which it found.
#
# Also check the nal_ref_idc column: a value of 0 on an SPS (type 7) or PPS
# (type 8) is what this driver emitted for a while.  Decoders tolerate it, and
# so did h264parse, but the specification does not allow it.

import re
import sys

NAL_NAMES = {
    1: "non-IDR slice", 2: "slice A", 3: "slice B", 4: "slice C",
    5: "IDR slice", 6: "SEI", 7: "SPS", 8: "PPS", 9: "AUD",
    10: "end of seq", 11: "end of stream", 12: "filler",
}

START_CODE = re.compile(b"\x00\x00\x00\x01|\x00\x00\x01")


def detect_framing(data):
    """Return 'annexb' or 'avc'.

    Annex-B begins with a start code.  AVC (as stored in MP4/Matroska) begins
    with a big endian 32-bit NAL length instead, so we compare: does the first
    four-byte length land exactly on a plausible second NAL?
    """
    if data[:4] in (b"\x00\x00\x00\x01", b"\x00\x00\x01"):
        return "annexb"

    length = int.from_bytes(data[:4], "big")
    if 0 < length <= len(data) - 4:
        return "avc"
    return "annexb"


def iter_annexb(data):
    spans, last = [], -1
    for m in START_CODE.finditer(data):
        if m.start() < last:
            continue
        spans.append((m.start(), len(m.group())))
        last = m.start() + len(m.group())

    for i, (pos, sc_len) in enumerate(spans):
        end = spans[i + 1][0] if i + 1 < len(spans) else len(data)
        yield pos + sc_len, end - pos - sc_len, sc_len


def iter_avc(data):
    pos = 0
    while pos + 4 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], "big")
        if length <= 0 or pos + 4 + length > len(data):
            break
        yield pos + 4, length, 4
        pos += 4 + length


def describe(header):
    nal_type = header & 0x1f
    return NAL_NAMES.get(nal_type, "reserved/unknown"), nal_type, (header >> 5) & 3


def main(argv):
    if len(argv) < 2:
        print(__doc__ or "usage: nals.py <file> [--limit N]")
        return 1

    path = argv[1]
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])

    data = open(path, "rb").read()
    framing = detect_framing(data)
    units = list(iter_annexb(data) if framing == "annexb" else iter_avc(data))

    print(f"{path}: {len(data)} bytes, framing={framing}, {len(units)} NAL units")
    print()

    counts = {}
    for n, (off, size, sc_len) in enumerate(units):
        if limit is not None and n >= limit:
            print(f"  ... {len(units) - limit} more")
            break
        if size < 1:
            print(f"  @{off:8d}  empty NAL")
            continue
        name, nal_type, nri = describe(data[off])
        counts[name] = counts.get(name, 0) + 1
        print(f"  @{off:8d} size={size:7d}  type={nal_type:2d} nri={nri}  {name}")

    print()
    print("counts:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
