import matplotlib.pyplot as plt
import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import ntpath
from ImageUtil import compute_mean_image_RGB as compute_mean_image_RGB


def compute_flat_frame(root_dir,out_dir):
    folders = glob.glob(root_dir+'\\*\\')
    nFolds = len(folders)
    dir = folders[0]
    files = glob.glob(dir+'*.tif')
    nFiles = len(files) #assume tiles in different dirs have the same naming pattern
    for f in range(nFiles): #process one stack of tiles at a time
        file_path = files[f]
        file_name = ntpath.basename(file_path)
        file_list = []
        for d in range(nFolds):
            tile_name = folders[d]+file_name
            file_list.append(tile_name)

        file_name_base = os.path.splitext(file_name)[0]
        out_file = out_dir + file_name_base + '.npy'
        master = compute_mean_image_RGB(file_list)
        np.save(out_file,master)


def main():
    if len(sys.argv) != 3:
        print('Usage: compute_master_dark <absolute_path_to_flat_acqs> <absolute_path_to_output_dir>')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    out_file = str(sys.argv[2])

    print('Flat frames acq dir.: ' + root_dir)
    print('Output dir:' + out_file)

    compute_flat_frame(root_dir,out_file)



if __name__ == '__main__':
    main()