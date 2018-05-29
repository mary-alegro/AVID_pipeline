import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt
from lxml import etree as ET
import multiprocessing as mp
import tifffile
import misc.XMLUtils as xml_utils





def get_res_info(root_dir):
    res_folder = []
    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root, '*/RES(*'):  # it's inside /RES*
            res_folder = root
            break

    return res_folder


def compose_image(root_dir):

    print('Processing {}'.format(root_dir))

    res_dir = get_res_info(root_dir)
    tiles_coords_file = os.path.join(res_dir,'tiles/tile_coordinates.npy')
    tiles_meta_file = os.path.join(res_dir,'tiles/tiling_info.xml')
    colormap_dir = os.path.join(root_dir,'heat_map/color_map_0.1')
    tile_file_name = 'tile_{:04d}_h_cmap.tif'

    if not os.path.exists(tiles_coords_file):
        print('Error: File {} does not exist'.format(tiles_coords_file))
        return

    if not os.path.exists(tiles_meta_file):
        print('Error: File {} does not exist'.format(tiles_meta_file))
        return

    tile_coords = np.load(tiles_coords_file).astype('int')
    grid_rows, grid_cols, img_rows, img_cols, img_home, img_file = xml_utils.XMLUtils.parse_tiles_metadata(tiles_meta_file)

    #sanity check
    nTiles1 = grid_rows*grid_cols
    nTiles2 = tile_coords.shape[0]

    if nTiles1 != nTiles2:
        print('Error: number of tiles from metadata is different from number of tiles in coodinates file')
        return

    #create mem mapped giant TIFF file
    tiff_name = colormap_dir+'/heatmap_full_res.tif'
    kwargs = {'bigtiff':True}
    img = tifffile.memmap(tiff_name,shape=(img_rows,img_cols),dtype='uint8',page=None, series=0, mode='r+',**kwargs) 
    for tile_num in range(nTiles2):
        print('Reading tile {}'.format(tile_num))
        tile_name = os.path.join(colormap_dir,tile_file_name.format(tile_num))
        tile = io.imread(tile_name)
        row_up,col_up,row_low,col_low = tile_coords[tile_num,:]
        img[row_up:row_low,col_up:col_low] = tile[:,:]

    img.flush()



def main():
    if len(sys.argv) != 2:
        print('Usage: create_colormap_from_tiles.py <root_dir>')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    compose_image(root_dir)

if __name__ == '__main__':
    main()

