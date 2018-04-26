import os
import sys
import fnmatch
import skimage.io as io
import logging
import glob
from PipelineRunner import  PipelineRunner
from ImageTiler import ImageTiler
from MaskTiler import MaskTiler
from TileMasker import TileMasker
import ConfigParser


def main():
    if len(sys.argv) != 3:
        print('Usage: run_pipeline.py <root_dir> <config_file>')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    conf_file = str(sys.argv[2])

    #create the pipeline
    pipeline = PipelineRunner(root_dir,conf_file)
    img_tiles = ImageTiler('Image Tiling',root_dir)
    mask_tiles = MaskTiler('Mask Resizing and Tiling',root_dir)
    apply_mask = TileMasker('Mask Tiles',root_dir)


    pipeline.add_stage(img_tiles)
    pipeline.add_stage(mask_tiles)
    #pipeline.add_stage(apply_mask)

    #run pipeline
    pipeline.execute()





if __name__ == '__main__':
    main()