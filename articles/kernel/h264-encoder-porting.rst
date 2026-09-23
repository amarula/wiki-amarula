======================================================================
Porting a Stateless H.264 Encoder: Rockchip VEPU2 and v4l2-h264-enc
======================================================================

.. note:: **TL;DR**

   - Practical notes from bringing up the **H.264 encoder on a Rockchip PX30
     (VEPU2)** against Paul Kocialkowski's **v4l2-h264-enc** stateless encoder
     core, covering where the core and the hardware each write the bitstream
     and how the stream-start position is handed over in bits.
   - Lists the **eight traps** met during bring-up, stated symptom first —
     ``Driver did not ack the request``, ``mb_type ... too large at 0 0``,
     ``deblocking_filter_idc 18 out of range`` — with what each one turned out
     to be.
   - Includes the **verification method**: what an independent decoder's
     messages mean, why a blank NV12 frame renders as uniform green, and a
     two-command test that proves an encoder is reading real pixels.

|

The ``v4l2-h264-enc`` core is hardware-independent and does the H.264 work:
it builds the parameter sets and manages references, rate control and the
RBSP. A backend — one file per SoC under
``drivers/media/platform/verisilicon/`` — programs the hardware's registers
and declares what the hardware can do.

This article is written from the outside in: what the decoder complains
about, and what that turned out to mean. The PX30 specifics are called out;
the questions apply to any hardware.

Which side writes the bitstream — the core or the hardware?
-----------------------------------------------------------

The core and the hardware split the bitstream between them. Guessing that
split wrong was the single most expensive mistake in this port, so establish
it first.

The core writes the AUD, the SPS and the PPS by default, and it will write
the slice header too. Each unit can be handed to the hardware instead, by
setting a capability flag in ``enc->flags``:

.. code-block:: c

   V4L2_H264_ENC_FLAG_HW_AUD
   V4L2_H264_ENC_FLAG_HW_SPS
   V4L2_H264_ENC_FLAG_HW_PPS
   V4L2_H264_ENC_FLAG_HW_SLICE_HEADER

The mechanism is a single early return, in ``rbsp_step_unit()``:

.. code-block:: c

   /* Return if no update is needed or if hardware generates the unit. */
   if (!(enc->rbsp_update & rbsp_update) || enc->flags & hw_flag)
           return 0;

A flag therefore means *the hardware generates this, do not write it*.

.. important::
   **How to find out which units your hardware generates:** read the vendor
   stack, not the documentation. If it reads a slice header *out of the
   encoder's output buffer*, the hardware wrote one. Rockchip's MPP does
   exactly that in ``h264e_slice_read()``, which parses a 32-bit start code,
   then the NAL header, then the slice header, from the buffer the hardware
   just filled. Nobody parses their own output for fields they wrote
   themselves.

On the PX30 the VEPU2 generates the whole slice — start code, NAL header,
slice header and slice data. Only the parameter sets come from the core, so
the backend sets ``V4L2_H264_ENC_FLAG_HW_SLICE_HEADER`` and leaves the rest
alone.

How is the stream-start position handed to the hardware?
--------------------------------------------------------

The hardware is not told "here is the next byte". It is given a position
inside the buffer where it continues the bitstream, and what it produces has
to be bit-continuous with what the core wrote. Four things describe that
position, and all four have to agree:

.. code-block:: c

   strm_bits   = v4l2_h264_enc_rbsp_bits_count(&enc->rbsp); /* core's bits */
   strm_base   = (strm_bits / 8) & ~7U;                  /* 8-byte aligned */
   strm_offset = strm_bits - strm_base * 8;              /* bit in the word */

* **The address** goes to the output stream register as
  ``dst_addr + strm_base`` — aligned *down*, never up to the next byte.
* **The bit offset** goes to ``VEPU_REG_STREAM_START_OFFSET(strm_offset)``.
  It is measured from the aligned address, which is why that register field
  is only six bits wide. Left at zero, the hardware writes over the tail of
  the core's slice header.
* **The eight bytes at the aligned address go back to the hardware**, packed
  in stream order, so it can merge its first partial byte with the bits the
  core already put there:

  .. code-block:: c

     hdr_msb = p[0] << 24 | p[1] << 16 | p[2] << 8 | p[3];
     hdr_lsb = p[4] << 24 | p[5] << 16 | p[6] << 8 | p[7];

  ``p[0]`` is the first byte of the stream and it lands in the most
  significant byte of the register. Packing this with ``memcpy()`` instead
  makes the stream order depend on the host's endianness — it will look right
  on a little-endian host right up until the hardware reads it.
* **The buffer limit** is written in units of eight bytes and read back in
  bits:

  .. code-block:: c

     vepu_write_relaxed(vpu, ((dst_size - offset8) >> 3) & ~7U,
                        VEPU_REG_STR_BUF_LIMIT);

  The asymmetry is not a typo. It is what the register does.

At completion the hardware reports, in bits, how much *it* wrote, counted
from the bit offset. The frame is the sum:

.. code-block:: c

   bytesused = DIV_ROUND_UP(strm_bits + hw_bits, 8);

MPP does all of this in ``setup_output_packet()``, and it is worth reading
side by side with your backend. One detail there is easy to miss: the offset
it passes in is ``mpp_packet_get_length()``, the length of the
*software-built* packet — the parameter sets and nothing else, because on
this hardware the slice header is not in it.

Which parameter-set fields must agree with the hardware?
--------------------------------------------------------

A hardware encoder that writes the slice header is writing fields whose
values come from the parameter sets. If its idea of those fields differs from
the SPS that goes into the stream, the slice header is subtly wrong and a
decoder misreads everything after the disagreement.

The one that bit here is the picture order count. VEPU2 writes slice headers
with **no** ``pic_order_cnt_lsb``, which means it derives the count from the
frame number — ``pic_order_cnt_type`` 2 — and cannot express type 0 at all.
An SPS saying type 0 tells the decoder to read a field the hardware never
wrote, so it reads four bits too many and every later field is nonsense.

MPP reaches the same conclusion from the other side: for VEPU2 it sets
``poc_type`` and ``hw_poc_type`` both to 2, which is also why its stream
amendment pass — whose whole job is rewriting the slice header — has nothing
to do on this hardware.

.. code-block:: c

   state->sps.pic_order_cnt_type = 2;

.. important::
   **Measure this rather than assume it.** Build the stream, then parse the
   hardware's own slice header under each candidate assumption and keep the
   one that yields sane fields. ``h264parse.py`` does exactly that, and it is
   how the mismatch above was pinned.

   The same run measures the *frame_num* width: this hardware wrote a 16-bit
   frame number, matching the ``log2_max_frame_num_minus4`` of the SPS it was
   handed, and not the 12-bit default MPP configures. It reads the parameter
   sets it is given — so a disagreement is yours to fix in the SPS, not
   something to work around.

The frame number itself does not come from the parameter sets. The hardware
is told it in a register, and it is what gets written into the slice header.
If nothing programs it, every frame claims frame number 0 — and with a
frame-number-derived picture order count, every frame then has the same
count. On VEPU2 that register is ``VEPU_REG_ENC_CTRL3``, carrying the pps id
and the frame number.

What does a backend have to decide per frame?
---------------------------------------------

* **Input format code** — the hardware's own numbering, not fourcc. Take the
  table from the vendor stack rather than guessing: several SoCs share a
  small enum, and its values are not interchangeable with any other enum.
* **The source plane addresses** — one per plane, for planar and semi-planar
  alike. The register names differ between vendors for the same addresses:
  Rockchip's luma/Cb/Cr are the datasheet's plane 0/1/2.
* **Reconstruction and reference buffers** — the reconstruction is what the
  hardware writes for this frame and what becomes the reference for the next.
  Both planes are needed, and the chroma plane sits at
  ``aligned_w * aligned_h``, both aligned to the macroblock size. Check it
  against the vendor stack: get it wrong and the colour is subtly wrong
  rather than absent.
* **Endian and byte-swap controls** — per format, from the vendor stack. A
  swapped input does not look like an obviously corrupt picture, which is
  what makes it worth copying exactly.
* **Every slice-header field the hardware writes** — the frame number, the
  pps id, and whatever else its slice header carries. If the backend does not
  program them, the hardware writes zeros.

What the backend does *not* need: a NAL size table, unless it splits a frame
into several slices. VEPU2 codes one slice per frame, so it programs neither
``ADDR_OUTPUT_CTRL`` nor ``SIZE_TABLE_PRESENT``; the NAL size table in the
shared encoder context belongs to the VC8000E backend.

What are the traps, by symptom?
-------------------------------

Written the way you meet them: what the decoder or the driver says, and what
it turned out to be.

``Driver did not ack the request`` — on the first P frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capability flags were being written into ``state->encode.flags``, the
per-frame flag word of the encode parameters control. The namespaces collide:
``V4L2_H264_ENC_FLAG_INTER_PRED`` is ``0x1``, and ``0x1`` in that field means
``V4L2_H264_ENCODE_FLAG_IDR_PIC``. Every frame was marked an IDR — legal for
an I frame, and rejected by the control validator for the first P frame.
Capabilities belong in ``enc->flags``, set once at init.

``Driver did not ack the request`` — with no error anywhere
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The request was never completed. ``hantro_end_prepare_run()`` is what calls
``v4l2_ctrl_request_complete()``, and a ``run()`` that returns early on
failure never reaches it: the buffers get finished but the request does not.
Complete the request on the failing path. Until you do, every failure in the
driver looks like a timeout in userspace.

``mb_type ... too large at 0 0`` — every frame, perfect container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The hardware was appending its own slice header to the one the core had
already written. The decoder parsed the core's header, then read the
hardware's start code, NAL header and slice header as the first macroblock.
What makes this one hard to see is that nothing splits the access unit at the
second header, so the NAL structure, the frame count and the access unit
sizes all look correct.

``deblocking_filter_idc N out of range`` — no frame at all
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A field near the *end* of the slice header decoded to nonsense, which means an
earlier field had the wrong width — a parameter-set disagreement, as above.
Failing on a named field rather than at MB 0 is the distinction that points
here.

A valid container with not one decodable frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The stream start was not byte-aligned, so the hardware wrote over the tail of
the slice header. The container tells you nothing about this; look at the
bit-level handoff.

The hardware wrote its own framing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some encoders have a "stream mode" that makes them emit a start code and
slice header themselves. With a core that also writes them you get two
copies. VEPU2 has ``VEPU_REG_H264_STREAM_MODE``, and it is left off — as MPP
leaves it off.

``v4l2-compliance`` reports failures that mean nothing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It has no support for stateless encoders: its codec detection carries an
``#if 0 /* There are no stateless encoders (yet) */`` and falls through to a
default that returns without checking anything. Its verdict on a stateless
encoder node is not evidence either way. Use a decoder instead.

``Driver does not support the selected stream``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An SPS the driver refused. Two layers of rules apply, and the driver's are
stricter about pixel format than the kernel validator's:
``hantro_try_ctrl()`` rejects any ``chroma_format_idc > 1`` and any bit depth
but 8-bit. A 4:4:4 or 10-bit stream fails there — and that is usually the
*encoder's input* rather than the encoder, since an element handed a 4:4:4
frame will happily encode 4:4:4. ``spscheck.py`` checks both layers and says
which one refused.

One more, quieter: the core writes the SPS and PPS with ``nal_ref_idc`` 0,
which the specification does not allow for NAL types 7 and 8. Decoders
tolerate it — ``h264parse`` rewrites them to zero as well — but ``nals.py``
prints the field, so it is worth a look if a strict decoder ever refuses a
stream that everything else accepts.

How do you verify an H.264 encoder?
-----------------------------------

Four questions, cheapest first. Each can pass while the next one fails, and
skipping to the last is how an afternoon goes into the wrong layer. The rule
underneath all of them: **a container that muxes without complaint proves
nothing** — ``matroskamux`` will store the most broken bitstream. The arbiter
is a decoder, ideally one that is not the hardware you are bringing up.

Does it encode at all?
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   gst-launch-1.0 videotestsrc num-buffers=50 ! \
       video/x-raw,format=I420,width=720,height=576 ! \
       v4l2slh264enc ! h264parse ! matroskamux ! filesink location=/tmp/out.mkv

   nals.py /tmp/out.mkv

This catches the two things hardest to see otherwise: no slice NAL units at
all — a stream can carry valid parameter sets and a correct frame count with
nothing to decode in between — and the wrong framing. GStreamer writing to
Matroska stores AVC, which has no start codes, so a tool that scans for them
finds data that merely looks like them and reports nonsense. ``nals.py``
detects which framing a file uses and says so.

Does an independent decoder accept it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   ffmpeg -i /tmp/out.mkv -f null -

Silence is success. Each message below means something specific:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ffmpeg says
     - It means
   * - ``error while decoding MB 0 0`` / ``mb_type ... in I slice too large``
     - A header is being read as macroblock data. The first macroblock fails,
       which is exactly where the slice *data* should have started.
   * - ``concealing 1620 DC, 1620 AC, 1620 MV errors``
     - All 1620 macroblocks of a 720x576 frame — the whole frame, not a few.
   * - ``deblocking_filter_idc 18 out of range``
     - A field near the *end* of the slice header. An earlier field had the
       wrong width, so everything after it shifted.
   * - ``mb_skip_run -1 is invalid``
     - The slice data ran out immediately — P frames whose payload is empty
       or unreadable.
   * - ``no frame!`` / ``Could not find codec parameters``
     - Nothing usable came out. Usually a consequence of the above rather
       than a separate fault.
   * - ``No start code is found``
     - The file is AVC, not Annex-B — an input framing problem, not an
       encoder one.

The useful distinction is between the first two rows. Failing **at MB 0**
means the very first thing after the slice header is wrong: a header where
data should be. Failing **later in the header**, on a named field, means the
header parsed correctly up to that point and then went out of step — which
points at a field width. That is the difference between "you wrote an extra
header" and "your parameter sets disagree with the hardware".

Are the pixels right?
^^^^^^^^^^^^^^^^^^^^^

Decode and read the bytes rather than looking at a screen. A green picture is
worth understanding precisely, because "green" is not a vague symptom — it is
arithmetic.

.. code-block:: bash

   gst-launch-1.0 filesrc location=/tmp/out.mkv ! decodebin ! videoconvert ! \
       video/x-raw,format=NV12 ! multifilesink location=/tmp/frame%02d.raw max-files=1

   SZ=$(wc -c < /tmp/frame00.raw)
   dd if=/tmp/frame00.raw bs=$((SZ*2/3)) skip=1 count=16 2>/dev/null | od -x -v

An NV12 frame is luma followed by interleaved chroma, so the chroma plane
starts at two thirds of the file whatever the resolution.

A **blank** NV12 frame is ``Y=0`` with ``U=V=0``. Run that through the BT.601
matrix and it is not black:

.. code-block:: text

   R = 1.164*(0-16) + 1.596*(0-128)                  -> clipped to 0
   G = 1.164*(0-16) - 0.391*(0-128) - 0.813*(0-128)  ~ 136
   B = 1.164*(0-16) + 2.018*(0-128)                  -> clipped to 0

RGB(0, 136, 0) — a uniform green. That is why a hardware decoder producing
nothing, or an encoder that wrote nothing, presents as a green screen rather
than a black one. The chroma read above returning ``0000`` is the
confirmation: a real picture has chroma, and a neutral one sits near
``8080``.

To check the luma is real, sample across a row. For a SMPTE colour bar test
pattern at 720 wide — seven bars of about 103 pixels — the luma descends:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - x
     - bar
     - expected luma
   * - 10
     - gray
     - ~0xb4
   * - 110
     - yellow
     - ~0xa9
   * - 210
     - cyan
     - ~0x86
   * - 310
     - green
     - ~0x70
   * - 410
     - magenta
     - ~0x4f
   * - 515
     - red
     - ~0x39
   * - 620
     - blue
     - ~0x16

Seven identical values instead means the luma is flat and the frame is blank.

Is it reading real pixels?
^^^^^^^^^^^^^^^^^^^^^^^^^^

This one needs no decoder, and it separates an encoder-side fault from
everything downstream of it:

.. code-block:: bash

   gst-launch-1.0 videotestsrc pattern=smpte num-buffers=1 ! \
       video/x-raw,format=I420,width=720,height=576 ! \
       v4l2slh264enc keyframe-interval=1 ! h264parse ! filesink location=/tmp/smpte.h264

   gst-launch-1.0 videotestsrc pattern=solid-color num-buffers=1 ! \
       video/x-raw,format=I420,width=720,height=576 ! \
       v4l2slh264enc keyframe-interval=1 ! h264parse ! filesink location=/tmp/flat.h264

   wc -c /tmp/smpte.h264 /tmp/flat.h264

Sharp bars cost an order of magnitude more than a flat field. Measured here:
**25523 bytes against 1698**. If the two come out about equal, the encoder is
being handed a constant whatever the source is, and the fault is on the input
side — before you spend any time on the bitstream. This is also the check
that clears the encoder when a decoder misbehaves.

Which tool answers which question?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Three small Python scripts were written during this bring-up and are
available alongside this article:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Question it answers
   * - `nals.py <../../_static/tools/nals.py>`_
     - What is actually in this file: framing, NAL units, sizes,
       ``nal_ref_idc``.
   * - `h264parse.py <../../_static/tools/h264parse.py>`_
     - Which field widths the encoder used in the slice header, ranked by how
       plausible each assumption is.
   * - `spscheck.py <../../_static/tools/spscheck.py>`_
     - Whether the driver and the kernel validator will accept an SPS, and
       which rule refused it.

``h264parse.py`` is the one that earns its keep. Given a stream whose slice
header does not parse, it re-parses it under the field widths a hardware
encoder is likely to have assumed and ranks the results, which turns "the
fields are wrong" into a specific pair of values. On the stream from this
bring-up it prints the SPS's own assumption reproducing
``deblocking_filter_idc 18``, and names ``poc_type=2, frame_num=16 bits`` as
the only combination with nothing unusual — which is what the hardware was
doing.

Its verdicts are heuristics, and it says so: ``slice_qp_delta`` is not checked
because a non-zero value is perfectly legal, and only an out-of-range field
or a mismatched pps id is treated as hard evidence. Decode the stream to be
sure.

Suggested order when something is wrong
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. ``nals.py`` — are there slices, and is the framing what you think?
#. ``ffmpeg -f null -`` — which of the messages above do you get?
#. If it fails at MB 0, suspect a second header. If it fails on a named
   field, run ``h264parse.py``.
#. If the decoder is silent but the picture is wrong, read the bytes.
#. If it looks like nothing decodes, do the stream-size test before touching
   bitstream code — one command, and it rules out half the problem.

.. tip::
   Porting a hardware video encoder, or integrating a vendor VPU driver into
   mainline Linux? Amarula Solutions does Linux kernel and multimedia driver
   development, mainlining, and BSP integration for Rockchip, NXP i.MX, and
   Allwinner platforms.
   `Contact our kernel team <https://www.amarulasolutions.com/contact/>`_
