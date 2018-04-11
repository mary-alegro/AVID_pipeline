#!/bin/bash -l

TMP_DIR=/data/magick_tmp

mkdir $TMP_DIR

export MAGICK_TMPDIR=$TMP_DIR
export MAGICK_MEMORY_LIMIT=64Gb

convert -crop 7x14 +repage +adjoin /data/00000_000000_000000.tif /data/tiles/tile_%04d.tif