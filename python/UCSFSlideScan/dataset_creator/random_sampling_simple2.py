import cv2

import fnmatch
import numpy as np
import os
import random
import scipy.misc
import sys
import matplotlib.pyplot as plt
import skimage.transform as xform
from misc.XMLUtils import XMLUtils
from misc.TiffTileLoader import TiffTileLoader
import skimage.io as io
import tifffile
import glob

THRESH=0.20


def get_files_info(root_dir):
    dirs = glob.glob(os.path.join(root_dir,'*'))
    file_dic = {}
    for d in dirs:
        mask_tiles_dir = os.path.join(d,'mask/final_mask/tiles')
        seg_tiles_dir = os.path.join(d,'heat_map/seg_tiles')
        patch_mask_dir = os.path.join(d,'mask/patches_mask')

        #find RES* folder
        output_dir = os.path.join(d,'output')
        res_dir = ''
        for root, dir, files in os.walk(output_dir):
            if fnmatch.fnmatch(root,'*/RES(*'): #it's inside /RES*
                res_dir = root
                break
        histo_tiles_dir = os.path.join(res_dir,'tiles')
        metadata_xml = os.path.join(histo_tiles_dir,'tiling_info.xml')

        #get patches mask
        patch_mask = None
        if os.path.exists(patch_mask_dir):
            files = glob.glob(os.path.join(patch_mask_dir,'*.tif'))
            if files:
                patch_mask = files[0] # there should be only one
            if not os.path.exists(patch_mask):
                patch_mask = None


        if os.path.exists(mask_tiles_dir) and os.path.exists(seg_tiles_dir) and os.path.exists(metadata_xml):
            file_dic[d] = {'mask_tiles':mask_tiles_dir, 'seg_tiles':seg_tiles_dir, 'patch_mask':patch_mask, 'xml_file':metadata_xml}

    return file_dic





# def save_color_images(root_dir):
#     file_list = {}
#     print("colored tiles pre-parse")
#     #save all tiled images in this directory
#     for root, dir, files in os.walk(root_dir):
#         print("walking file system for colored tiles")
#         if fnmatch.fnmatch(root,'*heat_map/seg_tiles'): #we want to fetch the tiles, so verify we are in /tiles*
#             print("found colored tiles folder")
#             for fn in fnmatch.filter(files,'*_*.tif'): #fetch tif images
#                 file_list[fn] = root
#
#     return file_list


# def fetch_tiles(root_dir):
#     file_list =  {}
#     print("masked tiles pre-parse")
#
#     #save all tiled images in this directory
#     for root, dir, files in os.walk(root_dir):
#         print("walking file system for masked tiles")
#         if fnmatch.fnmatch(root,'*mask/final_mask/tiles'): #we want to fetch the tiles, so verify we are in /tiles*
#             print("found masked tiles folder")
#             for fn in fnmatch.filter(files,'*_*.tif'): #fetch tif images
#                 #file_name = os.path.join(root,fn)
#                 file_list[fn] = root
#
#     return file_list




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

    dirs_list = get_files_info(root_dir)

    for sliceid in dirs_list.keys():
        print('Extracting patches from {}'.format(sliceid))
        slice_dic = dirs_list[sliceid]
        mask_tiles_dir = slice_dic['mask_tiles']
        seg_tiles_dir = slice_dic['seg_tiles']
        patch_mask = slice_dic['patch_mask']
        xml_file = slice_dic['xml_file']

        #fetch list of all mask tiles
        masked_file_list = glob.glob(os.path.join(mask_tiles_dir,'*.tif'))

        #fetch list of all histo tiles
        colored_file_list = glob.glob(os.path.join(seg_tiles_dir,'*.tif'))

        if patch_mask:
            #read metadata
            grid_rows, grid_cols, img_rows, img_cols, img_home, img_file = XMLUtils.parse_tiles_metadata(xml_file)

            # read patches mask and compute virtual tile coords
            tiffLoader = TiffTileLoader()
            tiffLoader.open_file(patch_mask)
            tiffLoader.compute_tile_coords(grid_rows,grid_cols)


        #travel up to base directory after colored tiles traveral
        os.chdir(home_dir)
        print('dir after all tiles collected: ' + os.getcwd())

        print("size of file list = " + str(len(masked_file_list)))

        #parse through all tiles to extract patches
        count = 0
        for fn in masked_file_list:

            count+=1
            #os.chdir(masked_file_list[fn])

            #get tile number from file name
            filename = os.path.basename(fn) #tile names are always 'tile_????.tif'
            idx1 = filename.find('_')
            idx2 = filename.find('.')
            snum =  filename[idx1+1:idx2]
            snum = int(snum)

            #load tile
            tile_arr = cv2.imread(fn)
            if tile_arr.ndim > 1:
                tile_arr = tile_arr[...,0]
            #set minumum amount of pixels necessary in each tile
            tile_thresh = THRESH * tile_arr.shape[0] * tile_arr.shape[1]

            if patch_mask:
                #load respective tile from patch mask
                tile_pmask_small = tiffLoader.get_tile_by_num(snum)
                #resize patch mask tile to match full res tile size
                tile_pmask = xform.resize(tile_pmask_small,tile_arr.shape,preserve_range=True).astype('uint8')

                tile_arr[tile_pmask < 10] = 0 #zero out pixels outside the ROI

            # get grey matter coordinates
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
                patch = extract_color_patch(patch_x, x, patch_y, y, (count-1), colored_file_list)
                os.chdir(home_dir)
                os.chdir('patches')
                scipy.misc.imsave('patch' + '_' + str((count-1))+'.tif', cv2.cvtColor(patch, cv2.COLOR_BGR2RGB))

            os.chdir(home_dir)

def extract_color_patch(patch_x, x, patch_y, y, fn, colored_file_list):

    #os.chdir(colored_file_list[fn])
    print('dir during actual extraction: ' + os.getcwd())
    colored_tile_arr = cv2.imread(colored_file_list[fn])
    #tile_arr = np.array(file)
    print("extract color patch")
    #coordinates = get_white_matter(tile_arr)
    #needed_samples = int(calc_percentage(tile_arr) * 10)
    return colored_tile_arr[patch_x:(patch_x + x), patch_y:(patch_y + y)]


# def test_coords_per_tile():
#     root_dir = '/home/maryana/storage/Posdoc/AVID/AV13/TEMP2/AT100_424'
#     coords_file = os.path.join(root_dir,'output/RES(0x0)/tiles/tile_coordinates.npy')
#     meta_xml_file = os.path.join(root_dir,'output/RES(0x0)/tiles/tiling_info.xml')
#     patches_mask_file = os.path.join(root_dir,'mask/patches_mask/AT100_424_res10_patches_mask.tif')
#     percent_from_mask = 0.95
#     npatches_total = 100
#
#     tile_coords_full = np.load(coords_file).astype('int')
#     grid_rows, grid_cols, img_rows, img_cols, img_home, img_file = XMLUtils.parse_tiles_metadata(meta_xml_file)
#     tiffLoader = TiffTileLoader()
#     tiffLoader.open_file(patches_mask_file)
#     tiffLoader.compute_tile_coords(grid_rows, grid_cols)
#
#     mask_patches = io.imread(patches_mask_file)
#     if mask_patches.ndim > 2:
#         mask_patches = mask_patches[...,0]
#     roi_row, roi_col = (mask_patches > 0).nonzero()
#     bkg_row,bkg_col = (mask_patches <= 0).nonzero()
#
#     nRoi = len(roi_row)
#     nBkg =






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