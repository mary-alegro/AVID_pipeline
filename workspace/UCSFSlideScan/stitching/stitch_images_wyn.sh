#!/bin/bash -l

if [ "$#" -ne 2 ]; then
	echo "Usage: stitch_image_wyn.sh <IMAGE_ROOT_DIR> <SLICE_NAME>"
	exit 0  
fi

#STITCHER_PATH='/home/maryana/bin/TeraStitcher/bin'

ROOT_DIR=$1
SLICE_NAME=$2
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

echo 'Export XML'
python /home/LargeSlideScan/workspace/UCSFSlideScan/python/UCSFSlideScan/create_terastitch_xml.py $ROOT_DIR'/Metadata.txt' $RAW_DIR'/xml_import.xml' '/data/'$SLICE_NAME'/raw'
touch $ROOT_DIR'/expxml'

echo 'Import'
time terastitcher --import --projin="xml_import.xml" --imin_channel="G" 
touch $ROOT_DIR'/import'

echo 'Compute displacement'
time terastitcher --displcompute --projin="xml_import.xml" --imin_channel="G" --noprogressbar 
touch $ROOT_DIR'/displ'

echo 'Compute projection'
time terastitcher --displproj --projin="xml_displcomp.xml" --imin_channel="G" 
touch $ROOT_DIR'/proj'

echo 'Threshold adj'
time terastitcher --displthres --threshold=0.7 --projin="xml_displproj.xml" --imin_channel="G" 
touch $ROOT_DIR'/thres'

echo 'Place tiles'
time terastitcher --placetiles --projin="xml_displthres.xml" --imin_channel="G"
touch $ROOT_DIR'/place'

echo 'Merge'
time teraconverter -s="xml_merging.xml" -d="$OUT_DIR" --sfmt="TIFF (unstitched, 3D)" --dfmt="TIFF (series, 2D)" --libtiff_bigtiff --noprogressbar
touch $ROOT_DIR'/merge'
