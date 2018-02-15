import os
import subprocess
import sys
import fnmatch
import skimage.io as io
import tifffile
from misc.XMLUtils import XMLUtils

#
# This script is supposed to run on the cluster
# Script for automatically tiling the full resolution histology images, using Image Magick


PIX_1MM = 819 #1mm= 819 pixels
PIX_5MM = 4095 #5mm = 4095 pixels

def get_mask_info(root_dir):
    file_list = dict()

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root,'*/RES(*'): #it's inside /RES*
            for fn in fnmatch.filter(files,'*_*_*.tif'): #find full resolution images
                if fn.find('res10') == 0: #skip res10 images
                    continue
                file_name = os.path.join(root,fn)
                tiff = tifffile.TiffFile(file_name) #load tiff header only
                size = tiff.series[0].shape
                del tiff
                nB_rows = size[0] / PIX_5MM  # num. of 5mm high blocks along the 'row' dimension
                nB_cols = size[1] / PIX_5MM  # num. of 5mm wide blocks along the 'columns' dimension

                #get masks folder
                path_list = root.split(os.sep)
                nW = len(path_list)
                mask_dir = ''
                for d in range(nW-2):
                    mask_dir+=path_list[d]+os.sep
                mask_dir = os.path.join(mask_dir,'mask/final_mask')

                #check if exists
                if os.path.exists(mask_dir):
                    #find mask file name
                    mask_file = ''
                    for root, dir, files in os.walk(root_dir):
                        for fm in fnmatch.filter(files, '*mask.tif'):  # there should be only one mask file
                            mask_file = os.path.join(root,fm)

                    if mask_file != '':
                        file_list[mask_file] = {'home':root, 'full_size':size, 'tile_grid':[nB_rows, nB_cols]}

                else:
                    continue

    return file_list



def save_metadata(img_name,info_dic,log_file):

    tiles = info_dic['tile_grid']
    tile_info = {'name':'Tiles','attrib':{'grid_rows':str(tiles[0]),'grid_cols':str(tiles[1])}}
    s = info_dic['size']
    img_info = {'name':'Image', 'attrib':{'rows':str(s[0]), 'cols':str(s[0]), 'file':img_name, 'home':info_dic['home'], 'children':[tile_info]}}

    XMLUtils.dict2xmlfile(img_info,log_file)



def process_masks(root_dir):


    #create Image Magick tmp directory
    TMP_DIR = os.path.join(root_dir,'magick_tmp')
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR,0777)

    #export Image Magick env variables
    os.environ['MAGICK_TMPDIR'] = TMP_DIR
    os.environ['MAGICK_MEMORY_LIMIT'] = '64Gb'

    #get file information and tiling grid size
    file_dic = get_mask_info(root_dir)

    for fi in file_dic.keys():

        fdic = file_dic[fi]
        home_dir = fdic['home']
        tile_grid = fdic['tile_grid']

        # Check if file was already processed. If so, skip it.
        if os.path.exists(os.path.join(home_dir, 'mask/final_mask/tiling_info.xml')):
            print('File {} has already been tiled. Nothing to do.'.format(fi))
            continue

        #create tiles directory
        tiles_dir = os.path.join(home_dir,'tiles')
        if not os.path.exists(tiles_dir):
            os.mkdir(tiles_dir, 0777)


        str_tile = '{}x{}@'.format(tile_grid[1],tile_grid[0]) #image magick works with COLSxROWS format
        str_tname = 'tile_%04d.tif' #tile file name pattern
        str_tname = os.path.join(tiles_dir,str_tname)


        log_out_name = os.path.join(home_dir,'stdout_log.txt')
        log_err_name = os.path.join(home_dir,'stderr_log.txt')
        log_out = open(log_out_name,'wb+')
        log_err = open(log_err_name,'wb+')
        # run system process

        print("Tiling file {}".format(fi))
        status = subprocess.call(['convert', '-crop', str_tile, '+repage', '+adjoin', fi, str_tname], env=dict(os.environ), stderr=log_err, stdout=log_out)

        #save metadata (used by export_heatmap_metadata.py)
        meta_file = os.path.join(tiles_dir,'tiling_info.xml')
        save_metadata(fi,fdic,meta_file)


def main():
    if len(sys.argv) != 2:
        print('Usage: tile_images_cluster.py <root_dir>')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are

    #root_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100/full_res'
    #root_dir= '/Users/maryana/Posdoc/AVID/AV13/TEMP'

    process_masks(root_dir)



if __name__ == '__main__':
    main()