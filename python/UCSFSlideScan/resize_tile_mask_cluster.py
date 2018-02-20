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
    mask_list = dict()

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root,'*/RES(*'): #it's inside /RES*
            for fn in fnmatch.filter(files,'*_*_*.tif'): #get only full resolution images
                if fn.find('res10') == 0: #skip res10 images
                    continue
                file_name = os.path.join(root,fn)
                tiff = tifffile.TiffFile(file_name) #load tiff header only
                size = tiff.series[0].shape
                # compute tile grid.
                # note that there's always a rounding problem since image size are hardly ever multiples of PIX_5MM
                nB_rows = size[0] / PIX_5MM  # num. of 5mm high blocks along the 'row' dimension
                nB_cols = size[1] / PIX_5MM  # num. of 5mm wide blocks along the 'columns' dimension
                file_list[file_name] = {'home':root, 'size':size, 'tile_grid':[nB_rows, nB_cols]}
                del tiff

    for f in file_list.keys():
        #get masks folder
        home_dir = file_list[f]['home']
        path_list = home_dir.split(os.sep)
        nW = len(path_list)
        mask_dir = ''
        for d in range(nW-2):
            mask_dir+=path_list[d]+os.sep
        mask_dir = os.path.join(mask_dir,'mask/final_mask')
        if os.path.exists(mask_dir):
            mask_file = ''
            for root, dir, files in os.walk(mask_dir):
                for fm in fnmatch.filter(files, '*mask.tif'):  # there should be only one
                    if fm.find('brain') != -1 or fm.find('wm') != -1:
                        continue
                    mask_file = os.path.join(root,fm)

            mask_list[mask_file] = {'home':root, 'full_size':file_list[f]['size'], 'tile_grid':file_list[f]['tile_grid']}

    return mask_list



def save_metadata(img_name,info_dic,log_file):

    tiles = info_dic['tile_grid']
    tile_info = {'name':'Tiles','attrib':{'grid_rows':str(tiles[0]),'grid_cols':str(tiles[1])}}
    s = info_dic['full_size']
    img_info = {'name':'Image', 'attrib':{'rows':str(s[0]), 'cols':str(s[0]), 'file':img_name, 'home':info_dic['home'], 'children':[tile_info]}}

    XMLUtils.dict2xmlfile(img_info,log_file)


def process_masks(root_dir):


    #create Image Magick tmp directory
    TMP_DIR = os.path.join(root_dir,'magick_tmp')
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR,0777)
    #export Image Magick env variables
    os.environ['MAGICK_TMPDIR'] = TMP_DIR
    os.environ['MAGICK_MEMORY_LIMIT'] = '24Gb'

    #get file information and tiling grid size
    file_dic = get_mask_info(root_dir)

    for fi in file_dic.keys():

        fdic = file_dic[fi]
        home_dir = fdic['home']
        full_size = fdic['full_size']
        tile_grid = fdic['tile_grid']

        # Check if file was already processed. If so, skip it.
        if os.path.exists(os.path.join(home_dir, 'mask_tiling_info.xml')):
            print('File {} has already been tiled. Nothing to do.'.format(fi))
            continue

        #create tiles directory
        tiles_dir = os.path.join(home_dir,'tiles')
        if not os.path.exists(tiles_dir):
            os.mkdir(tiles_dir, 0777)

        #
        # Resize
        #
        log_out_name1 = os.path.join(home_dir,'resize_stdout_log.txt')
        log_err_name1 = os.path.join(home_dir,'resize_stderr_log.txt')
        log_out1 = open(log_out_name1,'wb+')
        log_err1 = open(log_err_name1,'wb+')
        size_str = '{}x{}'.format(full_size[1],full_size[0]) #image magick uses cols x rows convention

        filename = os.path.splitext(os.path.basename(fi))[0]
        str_rname = os.path.join(home_dir,filename+'_full_res.tif')

        # run resize system process
        print("Resizing file {}".format(fi))
        status = subprocess.call(['convert', '-resize', size_str, fi, str_rname], env=dict(os.environ), stderr=log_err1, stdout=log_out1)


        #
        # Tile
        #
        log_out_name2 = os.path.join(home_dir,'tile_stdout_log.txt')
        log_err_name2 = os.path.join(home_dir,'tile_stderr_log.txt')
        log_out2 = open(log_out_name2,'wb+')
        log_err2 = open(log_err_name2,'wb+')
        str_tile = '{}x{}@'.format(tile_grid[1],tile_grid[0]) #image magick works with COLSxROWS format
        str_tname = 'tile_%04d.tif' #tile file name pattern
        str_tname = os.path.join(tiles_dir,str_tname)

        #run tiling process
        print("Tiling file {}".format(str_rname))
        status = subprocess.call(['convert', '-crop', str_tile, '+repage', '+adjoin', str_rname, str_tname],
                                 env=dict(os.environ), stderr=log_err2, stdout=log_out2)

        #save metadata (used by export_heatmap_metadata.py)
        meta_file = os.path.join(tiles_dir,'mask_tiling_info.xml')
        save_metadata(str_rname,fdic,meta_file)


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