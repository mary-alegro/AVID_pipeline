#!/bin/bash


arr=(280 296 312 328 344 360 376 392 408 424 440 457 472 488 504 520 536 552 568 584 600 616 632 648)

mask_dir=/home/maryana/storage/Posdoc/AVID/AV13/AT100/res10/final_mask

for id in ${arr[@]};do
	file_name=$mask_dir/'AT100_'$id'_res10_mask.tif'
	dest_dir=/grinberg/scratch/AVID/resize_mary/'AT100_'$id/mask/final_mask
	echo $file_name
	echo $dest_dir
	scp $file_name malegro@wynlog1.compbio.ucsf.edu:$dest_dir;
done;
