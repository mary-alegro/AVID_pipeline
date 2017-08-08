import matplotlib.pyplot as plt
import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
from ImageUtil import compute_mean_image_RGB as compute_mean_image_RGB


def compute_dark_frame(root_dir,out_file):
    files = glob.glob(root_dir+"*.tif")
    master = compute_mean_image_RGB(files)
    # save mean image as numpy array
    np.save(out_file, master)

def main():
    if len(sys.argv) != 3:
        print('Usage: compute_master_dark <absolute_path_to_dark_frames> <absolute_path_to_output_file>')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    out_file = str(sys.argv[2])

    print('Dark frames dir.: ' + root_dir)
    print('Output file:' + out_file)

    compute_dark_frame(root_dir,out_file)

if __name__ == '__main__':
    main()