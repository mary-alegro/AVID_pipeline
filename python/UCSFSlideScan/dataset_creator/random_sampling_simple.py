import cv2

import fnmatch
import numpy as np
import os
from PIL import Image
import random
import scipy.misc
from skimage.io import imread
from skimage.color import rgb2gray
from sklearn.feature_extraction import image
import subprocess
import sys 
import tifffile
import matplotlib.pyplot as plt
import skimage.transform as xform

THRESH=0.20


def save_color_images(root_dir):
    file_list = {}
    print("colored tiles pre-parse")
    #save all tiled images in this directory
    for root, dir, files in os.walk(root_dir):
        print("walking file system for colored tiles")
        if fnmatch.fnmatch(root,'*heat_map/seg_tiles'): #we want to fetch the tiles, so verify we are in /tiles*
            print("found colored tiles folder")
            for fn in fnmatch.filter(files,'*_*.tif'): #fetch tif images
                file_list[fn] = root
    return file_list

def fetch_tiles(root_dir):
    file_list =  {}
    print("masked tiles pre-parse")

    #save all tiled images in this directory
    for root, dir, files in os.walk(root_dir):
        print("walking file system for masked tiles")
        if fnmatch.fnmatch(root,'*mask/final_mask/tiles'): #we want to fetch the tiles, so verify we are in /tiles*
            print("found masked tiles folder")
            for fn in fnmatch.filter(files,'*_*.tif'): #fetch tif images
                #file_name = os.path.join(root,fn)
                file_list[fn] = root

    return file_list

def calc_percentage(img_arr):
    print(np.count_nonzero(img_arr))
    print(np.count_nonzero(img_arr==0))
    print(np.prod(img_arr.shape))
    white_matter_percentage = np.count_nonzero(img_arr)/(float(np.prod(img_arr.shape)))
    print('white matter percentage: ' + str(white_matter_percentage))

    return white_matter_percentage


def get_gray_matter(img_arr):
    nonzero = np.nonzero(img_arr)
    coordinates = [(nonzero[0][i], nonzero[1][i]) for i in range(len(nonzero[0]))]
    return coordinates

# def significant_overlap(left, right, top, bottom, patch_points):
#     for point_set in patch_points:
#         x_overlap = max(0, min(patch_points[1], right) - max(patch_points[0], left));
#         y_overlap = max(0, min(patch_points[3], bottom) - max(patch_points[2], top));
#         overlap_area = x_overlap * y_overlap;
#     return (overlap_area/(x_len * y_len) > .1)


def collect_samples(root_dir, x_len, y_len):

    home_dir = os.getcwd()

    x = int(x_len)
    y = int(y_len)

    print("fetching masked tiles")
    #fetch list of all tiles
    masked_file_list = fetch_tiles(root_dir)

    print("fetching colored tiles")
    #fetch list of all tiles
    colored_file_list = save_color_images(root_dir)

    #travel up to base directory after colored tiles traveral
    os.chdir(home_dir)
    print('dir after all tiles collected: ' + os.getcwd())

    print("size of file list = " + str(len(masked_file_list)))

    #parse through all tiles to extract patches
    for fn in masked_file_list:
        os.chdir(masked_file_list[fn])
        tile_arr = cv2.imread(fn)
        tile_thresh = THRESH*tile_arr.shape[0]*tile_arr.shape[1]
        #tile_arr = np.array(file)
        print("read tile array")
        coordinates = get_gray_matter(tile_arr)
        if (len(coordinates) == 0) or (len(coordinates) < tile_thresh):
            os.chdir(home_dir)
            continue

        print("calculated coordinates white matter")

        #determine how many samples are needed based on sampling logic
        needed_samples = 1

        #identifying patch centers
        patches = []
        patch_centers = []
        patch_points = []
        sample_counter = 0
        temp_coordinate = ()

        #avoid infinite loop
        max_tries = 10

        #make sure samples are the same size and do not exceed image boundaries
        while sample_counter < needed_samples and max_tries > 0:

            #calculate a random center and check if it is valid
            temp_coordinate = random.randint(0, len(coordinates) - 1)
            max_tries -= 1
            if (coordinates[temp_coordinate][0] - x/2) < 0 or \
                (coordinates[temp_coordinate][1] - y/2) < 0 or \
                (coordinates[temp_coordinate][0] + x/2) >= len(tile_arr) or \
                (coordinates[temp_coordinate][1] + y/2) >= len(tile_arr[0]):
                continue

            patch_centers.append(temp_coordinate)
            #patch_points.append([left, left, top, bottom])
            sample_counter += 1
		
        #begin patch extraction
        print("beginning patch extraction")
        os.chdir(home_dir)
        print('dir at start of patch extraction: ' + os.getcwd())

        if not os.path.exists('patches'):
            os.makedirs('patches')

        #extract square patches with center coordinate
        for i in range(len(patch_centers)):
            patch_x = coordinates[patch_centers[i]][0] - x/2
            patch_y = coordinates[patch_centers[i]][1] - y/2
            patch = extract_color_patch(patch_x, x, patch_y, y, fn, colored_file_list)
            os.chdir(home_dir)
            os.chdir('patches')
            scipy.misc.imsave('patch' + '_' + fn, cv2.cvtColor(patch, cv2.COLOR_BGR2RGB))

        os.chdir(home_dir)

def extract_color_patch(patch_x, x, patch_y, y, fn, colored_file_list):

    os.chdir(colored_file_list[fn])
    print('dir during actual extraction: ' + os.getcwd())
    colored_tile_arr = cv2.imread(fn)
    #tile_arr = np.array(file)
    print("extract color patch")
    #coordinates = get_white_matter(tile_arr)
    #needed_samples = int(calc_percentage(tile_arr) * 10)
    return colored_tile_arr[patch_x:(patch_x + x), patch_y:(patch_y + y)]


def main():
    #check for user input
    if (len(sys.argv) == 4):
        root_dir = sys.argv[1]
        x_len = sys.argv[2]
        y_len = sys.argv[3]
        print("collected arguments")
        collect_samples(root_dir, x_len, y_len)
    else:
        print("Usage: enter a directory, x length of each sample, y length of each sample")
if __name__ == "__main__":
    main()