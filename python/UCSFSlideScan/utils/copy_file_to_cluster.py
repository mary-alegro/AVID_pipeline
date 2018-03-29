import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from skimage import img_as_ubyte
import skimage.color as color
import nibabel as nib



ids = [280,296,312,328,344,360,376,392,408,424,440,457,472,488,504,520,536,553,568,584,600,616,632,648]

storage_path='/home/maryana/R_DRIVE/Experiments/AVID/Cases/1811-001/Master Package 1181-001/Images/1181-001-Stitched'

img_cpath = '/grinberg/scratch/AVID/resize_mary/AT100_280/output/RES(0x0)'
mask_cpath = '/grinberg/scratch/AVID/resize_mary/AT100_280/output/RES(0x0)'


def get_file_name(root_dir):

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root,'*/RES(*'): #it's inside /RES*
            for fn in fnmatch.filter(files,'*_*_*.tif'): #get only full resolution images
                if fn.find('res10') == 0: #skip res10 images
                    continue
                else:
                    file_name = os.path.join(root,fn)
                    break

    return file_name

