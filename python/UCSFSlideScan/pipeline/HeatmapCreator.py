import os
import sys
import fnmatch
import skimage.io as io
import tifffile
from misc.XMLUtils import XMLUtils
import logging
import glob
from misc.TiffTileLoader import TiffTileLoader
import numpy as np
from lxml import etree as ET
import  export_heatmap_metadata  as exp_meta

TILE_COORDS_FILE = '/tiles/tile_coordinates.npy' #inside output/RES???/, stores tiles coordinates
TILING_INFO_FILE = '/tiles/tiling_info.xml' #inside output/RES???/, stores gridsize and original file size
TILES_ADJ_METADATA = '/heat_map/TAU_seg_tiles/tiles_metadata.xml' # stores tiles adjacency information
TAU_SEG_DIR = '/heat_map/TAU_seg_tiles'
HISTO_TILE_NAME = 'tile_{:04d}.tif'
SEG_TILE_NAME = 'tile_{:04d}_mask.tif'
HMAP_RES = 0.1 # 0.1mm

class HeatmapCreator(object):

    #Constructor
    def __init__(self,name,root_dir=None,dir_list=None):
        self.stage_name = name
        self.root_dir = root_dir
        self.dir_list = dir_list
        self.nErrors = 0
        self.config = None

        #init logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # create a file handler
        log_name = os.path.join(root_dir,'HeatmapCreator.log')
        handler = logging.FileHandler(log_name)
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(handler)

        #default values
        self.PIX_1MM = 819  # 1mm= 819 pixels
        self.PIX_5MM = 4095  # 5mm = 4095 pixels
        self.HMAP_RES = 0.1


    #run stage method
    def run_stage(self):
        if self.root_dir:
            self.dir_list = self.get_dir_list(self.root_dir)


    def set_config(self,config):
        self.config = config
        if self.config:
            self.MEM_MAX = str(self.config.get('global', 'MAGICK_MEM'))
            self.PIX_1MM = int(self.config.get('global', 'PIX_1MM'))
            self.PIX_5MM = int(self.config.get('global', 'PIX_5MM'))
            self.HMAP_RES = float(self.config.get('heat_map', 'HMAP_RES'))



    def get_dir_list(self, root_dir):
        list_dirs = glob.glob(root_dir + '/*/')
        return list_dirs


    def get_num_white(self, block):
        # num. non zeros in the blue channel
        tmp_nnz_b = block.flatten().nonzero()
        nnz_b = float(len(tmp_nnz_b[0]))  # number of non-zero pixel in BLOCK matrix
        return nnz_b

    def get_num_pix_tissue(self, img):  # assumes RGB image
        tmp_img = img[:, :, 0] + img[:, :, 1] + img[:, :, 2]
        tmp_nnz_b = tmp_img.flatten().nonzero()
        nnz_b = float(len(tmp_nnz_b[0]))  # number of non-zero pixel in img
        return nnz_b



    #compute heat TAU percentages
    def compute_heatmap(self, TAU_seg_dir, hm_name, orig_img_size, coords_map):

        #NPIX_BLOCK = pix_mm
        NPIX_BLOCK = self.HMAP_RES*self.PIX_1MM #num os pix in a block of HMAP_RES resolution (along rows or col dimentions)
        NPIX_BLOCK = int(np.round(NPIX_BLOCK))
        min_val_tissue = 0
        max_val_tissue = 0

        #create a memory mapped matriz the size of the original histo image
        #hm_name = os.path.join(hm_dir,'heatmap_{}.npy'.format(slice_id))
        heatmap_per_tissue = np.memmap(hm_name, dtype='float32', mode='w+', shape=(orig_img_size[0],orig_img_size[1]))

        #iterate over each tile
        nTiles = coords_map.shape[0]
        for nTile in range(nTiles):
            img_name = HISTO_TILE_NAME.format(nTile)
            img_path = os.path.join(TAU_seg_dir, img_name)
            img = io.imread(img_path)

            mask_name = SEG_TILE_NAME.format(nTile)
            mask_path = os.path.join(TAU_seg_dir, mask_name)

            #histo_per_tissue = np.zeros(img.shape[0:2])

            #process tile data
            if os.path.isfile(mask_path):  # run image processing routine if mask exists

                row_up = coords_map[nTile,0]
                col_up = coords_map[nTile,1]
                row_low = coords_map[nTile,2]
                col_low = coords_map[nTile,3]
                rows_tmp = row_low-row_up
                cols_tmp = col_low-col_up

                mask = io.imread(mask_path)
                rows = mask.shape[0]
                cols = mask.shape[1]

                #sanity check, check if size from coordinates file matches tile image size
                if rows_tmp != rows:
                    self.logger.info('Error: Tile row size differs from size caculated from coordinates. Skipping.')
                    continue
                if cols_tmp != cols:
                    self.logger.info('Error: Tile columns size differs from size caculated from coordinates. Skipping.')
                    continue

                #temporary matrix
                histo_per_tissue = np.zeros((rows,cols))

                #compute num. of block in tile along_rows
                nblocks_tile_rows = rows/NPIX_BLOCK
                nblocks_tile_rows = int(np.round(nblocks_tile_rows))

                #compute num. of block along cols
                nblocks_tile_cols = cols/NPIX_BLOCK
                nblocks_tile_cols = int(np.round(nblocks_tile_cols))

                bg_row = 0
                bg_col = 0
                for r in range(nblocks_tile_rows):  # process blocks num. blocks along rows
                    end_row = NPIX_BLOCK * (r + 1)

                    for c in range(nblocks_tile_cols): # num. blocks along cols
                        end_col = NPIX_BLOCK * (c + 1)

                        # last block can be problematic, we have to check if the indices are inside the right range
                        if c == (nblocks_tile_cols - 1):
                            if end_col != cols:
                                end_col = cols

                        if r == (nblocks_tile_rows - 1):
                            if end_row != rows:
                                end_row = rows

                        block_mask = mask[bg_row:end_row, bg_col:end_col]
                        block_img = img[bg_row:end_row, bg_col:end_col, :]

                        nonzero_pix_mask = self.get_num_white(block_mask)  # get number of non-zero pixels in mask
                        #total_pix_block = rows * cols  # total number of pixel in image block
                        npix_tissue_block = self.get_num_pix_tissue(block_img)

                        #percent_total = float(nonzero_pix_mask) / float(total_pix_block)
                        percent_tissue = 0.0 if npix_tissue_block == 0 else (
                                float(nonzero_pix_mask) / float(npix_tissue_block))

                        histo_per_tissue[bg_row:end_row, bg_col:end_col] = percent_tissue * 100

                        bg_col = end_col

                    bg_row = end_row
                    bg_col = 0

            # get min and max values for the entire slice, per amount of tissue
            if histo_per_tissue.min() < min_val_tissue:
                min_val_tissue = histo_per_tissue.min()
            if histo_per_tissue.max() > max_val_tissue:
                max_val_tissue = histo_per_tissue.max()

            # hm2_name = os.path.join(hm_dir, img_name[0:-4] + '_hm_pertissue.npy')
            # np.save(hm2_name, histo_per_tissue)
            heatmap_per_tissue[row_up:row_low,col_up:col_low] = histo_per_tissue[...]


        return min_val_tissue, max_val_tissue




    #get information from XML file created during the histology tiling stage (ImageTiler.py)
    def load_tiling_metadata(self, meta_xml):
        grid_rows, grid_cols, img_rows, img_cols, img_home, img_file = XMLUtils.parse_tiles_metadata(meta_xml)
        return [grid_rows,grid_cols],[img_rows,img_cols]

    #get tile coordinates from the file created during the histology tiling processes (ImageTiler.py)
    def load_tile_coords(self,coords_file):
        coords = np.load(coords_file)
        return coords

    def run_compute_heatmap(self,slice_dir):
        self.logger.info('*** Beginning to compute heatmap {} ***'.format(slice_dir)) #i.e. /.../.../batch1/AT100_456/
        path = os.path.normpath(slice_dir).split(os.sep)
        slice_id = path[-1]
        tau_seg_dir = os.path.join(slice_dir,TAU_SEG_DIR)
        hm_dir = os.path.join(slice_dir,'/heat_map/hm_map_'+str(self.HMAP_RES))
        if os.path.isdir(hm_dir):
            os.mkdir(hm_dir)
        hm_file = os.path.join(hm_dir,'heat_map_'+str(self.HMAP_RES)+'.npy')



















    def create_colormap(self):
        pass

