#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
#
# cif-setup.sh -- bring up the PX30 CIF capture pipeline with a TVP5150
# decoder (bticino C100 / buffalo board), run from the target's shell.
#
# The decoder reports the height of ONE FIELD -- 288 lines for a 625/50 (PAL)
# source, 240 for 525/60 (NTSC) -- and the kernel's link validation requires
# the format on the interface's sink pad to match it exactly, or streamon fails
# with -EPIPE (-32) and the driver only says "failed to start pipeline -32".
#
# The capture, on the other hand, is a whole frame: the interface writes the
# two fields onto alternate lines of one buffer, so the video node reports
# twice the decoder's height and V4L2_FIELD_INTERLACED.  The driver chooses
# the height from the source, so what is set on the video node is a request --
# the geometry to work with is the one that comes back, which is why this
# reads it back instead of assuming.
#
# Usage:
#   cif-setup.sh [-d MEDIA] [-s pal|ntsc] [-f FOURCC] [-p] [-n] [cmd]
#
#   -d MEDIA    media device (default /dev/media0)
#   -s STD      decoder standard: pal (default) or ntsc
#   -f FOURCC   capture pixel format (default NV16, 4:2:2 straight from the
#               decoder; NV12 lets the CIF's scaler halve the chroma)
#   -p          switch the decoder's test pattern on: black picture with valid
#               sync, which is the only source this board has when no video
#               signal is wired to the IF demodulator
#   -n          dry run: print what would be done
#
#   cmd: setup (default)   standard, formats, then show the result
#        show              print the topology of the three entities
#        capture [FRAMES]  capture to /tmp/cif.raw (default 100 frames)
#
# Entity names come from the drivers; override in the environment if they
# change:  SENSOR  IFACE  STREAM
#
# The capture path is ping-pong: two buffers are taken at streamon and the
# driver rotates the rest in.  With fewer than three or four queued buffers
# the queue starves, the frame goes to the dummy buffer and is dropped, so
# capture always asks for --stream-mmap=4.

set -u

MEDIA=/dev/media0
STD=pal
PIXFMT=NV16
PATTERN=no
DRYRUN=no
CMD=setup
FRAMES=100

SENSOR=${SENSOR:-"tvp5150 1-005d"}
IFACE=${IFACE:-"rkcif-dvp0"}
STREAM=${STREAM:-"rkcif-dvp0-id0"}

die() {
	echo "cif-setup: $*" >&2
	exit 1
}

run() {
	if [ "$DRYRUN" = yes ]; then
		echo "  would run: $*"
		return 0
	fi
	echo "  $*"
	"$@" || die "$1 failed"
}

usage() {
	sed -n '3,/^$/p' "$0" | sed 's/^# \{0,1\}//'
}

topology() {
	media-ctl -d "$MEDIA" -p
}

# Device node of the entity whose name contains $1, taken from the topology.
entity_node() {
	topology | awk -v want="$1" '
		/^- entity / { found = index($0, want) ? 1 : 0; next }
		found && /device node name/ { print $NF; exit }
	'
}

# The decoder's source format, as "code width height field".
sensor_geometry() {
	topology | awk -v want="$SENSOR" '
		/^- entity / { found = index($0, want) ? 1 : 0; next }
		found && !done && match($0, /fmt:[^ ]+/) {
			f = substr($0, RSTART + 4, RLENGTH - 4)
			split(f, a, "/")
			split(a[2], b, "x")
			field = "none"
			if (match($0, /field:[a-z_-]+/))
				field = substr($0, RSTART + 6, RLENGTH - 6)
			print a[1], b[1], b[2], field
			done = 1
		}
	'
}

# The geometry the driver gives the capture, as "width height".  It is twice
# the decoder's height for a field-based source.
capture_geometry() {
	v4l2-ctl -d "$VIDEO" --get-fmt-video 2>/dev/null |
		awk '/Width\/Height/ { gsub(/.*: */, ""); gsub(/ /, ""); print; exit }'
}

# Leaves CODE, W, H and FIELD set: what the decoder gives.
read_sensor_geometry() {
	# shellcheck disable=SC2046  # word splitting is the point here
	set -- $(sensor_geometry)
	[ $# -ge 3 ] || die "no format found for \"$SENSOR\": is the decoder bound?"
	CODE=$1
	W=$2
	H=$3
	FIELD=${4:-none}
}

# The driver reads PAL unless the height is a 525/60 one, and the decoder
# reports the geometry of whichever standard it locked to.  If they disagree,
# the capture decodes the sync codes with the wrong timing and never produces
# a frame -- say so here instead of at streamon.
check_standard() {
	case "$STD" in
	pal)
		case "$H" in
		240 | 480)
			die "height ${H} is the 525/60 geometry but the standard is pal: the driver would select NTSC. Set the standard (--set-standard) or pass -s ntsc."
			;;
		esac
		;;
	ntsc)
		case "$H" in
		288 | 576)
			die "height ${H} is the 625/50 geometry but the standard is ntsc: the driver would select PAL. Pass -s pal."
			;;
		esac
		;;
	esac
}

show() {
	topology | awk -v a="$SENSOR" -v b="$IFACE" -v c="$STREAM" '
		/^- entity / { p = (index($0, a) || index($0, b) || index($0, c)) }
		p
	'
}

bytes_per_frame() {
	case "$PIXFMT" in
	NV16 | NV61 | NV16M | NV61M) echo $(($1 * $2 * 2)) ;;
	NV12 | NV21 | NV12M | NV21M) echo $(($1 * $2 * 3 / 2)) ;;
	*) echo 0 ;;
	esac
}

while [ $# -gt 0 ]; do
	case "$1" in
	-d) MEDIA=$2; shift 2 ;;
	-s) STD=$2; shift 2 ;;
	-f) PIXFMT=$2; shift 2 ;;
	-p) PATTERN=yes; shift ;;
	-n) DRYRUN=yes; shift ;;
	setup | show | capture)
		CMD=$1
		shift
		if [ "$CMD" = capture ] && [ $# -gt 0 ]; then
			FRAMES=$1
			shift
		fi
		;;
	-h | --help) usage; exit 0 ;;
	*) usage >&2; die "unknown argument: $1" ;;
	esac
done

if [ "$CMD" = show ]; then
	show
	exit 0
fi

SUBDEV=$(entity_node "$SENSOR")
[ -n "$SUBDEV" ] || die "no device node for \"$SENSOR\" in $MEDIA"
VIDEO=$(entity_node "$STREAM")
[ -n "$VIDEO" ] || die "no device node for \"$STREAM\" in $MEDIA"

echo "decoder: $SUBDEV  ($SENSOR)"
echo "capture: $VIDEO  ($STREAM)"

if [ "$CMD" = capture ]; then
	GEO=$(capture_geometry)
	[ -n "$GEO" ] || die "cannot read the capture format: run setup first"
	CAP_W=${GEO%/*}
	CAP_H=${GEO#*/}
	run v4l2-ctl -d "$VIDEO" --stream-mmap=4 --stream-count="$FRAMES" \
		--stream-to=/tmp/cif.raw
	BYTES=$(bytes_per_frame "$CAP_W" "$CAP_H")
	if [ "$DRYRUN" = no ] && [ "$BYTES" -gt 0 ]; then
		GOT=$(wc -c </tmp/cif.raw)
		echo "  /tmp/cif.raw: $GOT bytes = $((GOT / BYTES)) frames of ${CAP_W}x${CAP_H} $PIXFMT"
	fi
	exit 0
fi

# 1. the standard decides the geometry the decoder reports
run v4l2-ctl -d "$SUBDEV" --set-standard "$STD"
if [ "$PATTERN" = yes ]; then
	run v4l2-ctl -d "$SUBDEV" -c test_pattern=1
fi

# 2. read the decoder's geometry back -- do not trust a size typed in by hand
read_sensor_geometry
echo "decoder format: $CODE ${W}x${H} field:$FIELD"
if [ "$DRYRUN" = yes ]; then
	echo "  (dry run: this is the format for the standard currently in the chip,"
	echo "   which is not necessarily $STD yet)"
fi
check_standard

# 3. the same geometry on the CIF's sink pad -- this is the format the source
#    declares, which is what link validation compares.  The source pad mirrors
#    it (rkcif_interface_set_fmt()), so pad 1 needs nothing.  The pad/stream
#    syntax needs media-ctl >= 1.24; older ones take the bare pad number.
SPEC="\"$IFACE\":0/0[fmt:$CODE/${W}x${H} field:$FIELD]"
if [ "$DRYRUN" = yes ]; then
	echo "  would run: media-ctl -d $MEDIA -V '$SPEC'"
else
	echo "  media-ctl -d $MEDIA -V '$SPEC'"
	media-ctl -d "$MEDIA" -V "$SPEC" 2>/dev/null ||
		media-ctl -d "$MEDIA" -V "\"$IFACE\":0[fmt:$CODE/${W}x${H} field:$FIELD]" ||
		die "could not set the CIF sink format"
fi

# 4. the video node: ask for the decoder's field geometry and take what the
#    driver reports back, which is the frame it actually captures
run v4l2-ctl -d "$VIDEO" --set-fmt-video="width=$W,height=$H,pixelformat=$PIXFMT"
if [ "$DRYRUN" = no ]; then
	GEO=$(capture_geometry)
	[ -n "$GEO" ] || die "cannot read the capture format back"
	CAP_W=${GEO%/*}
	CAP_H=${GEO#*/}
	echo "capture: ${CAP_W}x${CAP_H} $PIXFMT (from ${W}x${H} of $FIELD fields)"
	case "$CAP_H" in
	"$H") ;;
	"$((H * 2))")
		echo "  the two fields of a frame are written into one buffer"
		;;
	*) echo "  note: the driver scaled the capture from ${W}x${H}" ;;
	esac
fi

echo
show
echo
echo "next: $0 -s $STD -f $PIXFMT capture 100"
