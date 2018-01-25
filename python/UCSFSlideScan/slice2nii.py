# convert a 2d histology/block tiff into a nift file

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


def create_nii(img_file,size,nii_file):

    M = np.array([[size[0], 0, 0, 0],[0, size[1], 0, 0],[0, 0, size[2], 0],[0, 0, 0, 1]])
    img = io.imread(img_file)

    if img.ndim > 2:
        img = color.rgb2gray(img)

    nii = nib.Nifti1Image(img, M)
    nib.save(nii,nii_file)


def main():
    if len(sys.argv) != 6:
        print('Usage: slice2nii.py <tiff_file> <x_size> <y_size> <z_size> <nifti_file>')
        exit()
    img_file = str(sys.argv[1])  # abs path to where the images are
    x_size = float(sys.argv[2])
    y_size = float(sys.argv[3])
    z_size = float(sys.argv[4])
    nii_file = str(sys.argv[5])
    size = np.array([x_size, y_size, z_size, 0])

    create_nii(img_file, size, nii_file)

if __name__ == '__main__':
    main()