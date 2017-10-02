#!/bin/bash -l

if [ "$#" -ne 1 ]; then
	echo "Usage: stitch_image.sh <IMAGE_ROOT_DIR>"
	exit 0  
fi

STITCHER_PATH='/home/maryana/bin/TeraStitcher/bin'

ROOT_DIR=$1
RAW_DIR=$ROOT_DIR'/raw'
OUT_DIR=$ROOT_DIR'/output'

#echo $ROOT_DIR
#echo $RAW_DIR
#echo $OUT_DIR

if [ -d "$OUT_DIR" ]; then
	rm -rf "$OUT_DIR"
fi
mkdir "$OUT_DIR"

cd $RAW_DIR
echo $PWD

echo 'Import'
time $STITCHER_PATH'/terastitcher' --import --projin="xml_import.xml" --imin_channel="G" 

echo 'Compute displacement'
time $STITCHER_PATH'/terastitcher' --displcompute --projin="xml_import.xml" --imin_channel="G" --noprogressbar 
#time $STITCHER_PATH'/terastitcher' --displcompute --projin="xml_import.xml" --imin_channel="G"

echo 'Compute projection'
time $STITCHER_PATH'/terastitcher' --displproj --projin="xml_displcomp.xml" --imin_channel="G" 

echo 'Threshold adj'
time $STITCHER_PATH'/terastitcher' --displthres --threshold=0.7 --projin="xml_displproj.xml" --imin_channel="G" 

echo 'Place tiles'
time $STITCHER_PATH'/terastitcher' --placetiles --projin="xml_displthres.xml" --imin_channel="G"

echo 'Merge'
time $STITCHER_PATH'/teraconverter' -s="xml_merging.xml" -d="$OUT_DIR" --sfmt="TIFF (unstitched, 3D)" --dfmt="TIFF (series, 2D)" --libtiff_bigtiff --noprogressbar
