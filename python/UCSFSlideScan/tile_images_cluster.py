import os
import subprocess
import sys
import fnmatch
import skimage.io as io
import tifffile
from XMLUtils import XMLUtils

#
# This script is supposed to run on the cluster
# Script for automatically tiling the full resolution histology images, using Image Magick


#subprocess.check_call(['sqsub', '-np', sys.argv[1], '/path/to/executable'],
#                      env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))

PIX_1MM = 819 #1mm= 819 pixels
PIX_5MM = 4095 #5mm = 4095 pixels

def get_img_info(root_dir):
    file_list = {}

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root,'*/RES(*'): #it's inside /RES*
            for fn in fnmatch.filter(files,'*_*_*.tif'): #get only full resolution images
                file_name = os.path.join(root,fn)
                tiff = tifffile.TiffFile(file_name) #load tiff header only
                size = tiff.series[0].shape
                # compute tile grid.
                # note that there's always a rounding problem since image size are hardly ever multiples of PIX_5MM
                nB_rows = size[0] / PIX_5MM  # num. of 5mm high blocks along the 'row' dimension
                nB_cols = size[1] / PIX_5MM  # num. of 5mm wide blocks along the 'columns' dimension
                file_list[file_name] = {'home':root, 'size':size, 'tile_grid':[nB_rows, nB_cols]}
                del tiff

    return file_list

# def compute_tile_sizes(file_dic):
#     for k in file_dic.keys():
#         dic = file_dic[k]
#         size = dic['size']
#         rows = size[0]
#         cols = size[1]
#
#         #compute tile grid.
#         #note that there's always a rounding problem since image size are hardly ever multiples of PIX_5MM
#         nB_rows = rows/PIX_5MM #num. of 5mm high blocks along the 'row' dimension
#         nB_cols = cols/PIX_5MM #num. of 5mm wide blocks along the 'columns' dimension
#
#         dic['tile_grid'] = [nB_rows,nB_cols]
#         file_dic[k] = dic
#         #return file_dic

def save_metadata(img_name,info_dic,log_file):

    tiles = info_dic['tile_grid']
    tile_info = {'name':'Tiles','attrib':{'grid_rows':str(tiles[0]),'grid_cols':str(tiles[1])}}
    s = info_dic['size']
    img_info = {'name':'Image', 'attrib':{'rows':str(s[0]), 'cols':str(s[0]), 'file':img_name, 'home':info_dic['home'], 'children':[tile_info]}}

    xmlUtil = XMLUtils()
    xmlUtil.dict2xmlfile(img_info,log_file)



def tile_images(root_dir):

    #create Image Magick tmp directory
    TMP_DIR = os.path.join(root_dir,'magick_tmp')
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR,0777)

    #export Image Magick env variables
    os.environ['MAGICK_TMPDIR'] = TMP_DIR
    os.environ['MAGICK_MEMORY_LIMIT'] = '16Gb'

    #get file information and tiling grid size
    file_dic = get_img_info(root_dir)

    for fi in file_dic.keys():

        fdic = file_dic[fi]
        home_dir = fdic['home']
        tile_grid = fdic['tile_grid']

        #create tiles directory
        tiles_dir = os.path.join(home_dir,'tiles')
        if not os.path.exists(tiles_dir):
            os.mkdir(tiles_dir, 0777)



        str_tile = '{}x{}@'.format(tile_grid[1],tile_grid[0]) #image magick works with COLSxROWS format
        str_tname = 'tile_%04d.tif' #tile file name pattern
        str_tname = os.path.join(tiles_dir,str_tname)

        #run system process
        subprocess.check_call(['convert', '-crop', str_tile, '+repage', '+adjoin', fi, str_tname], env=dict(os.environ))

        #save metadata (used by export_heatmap_metadata.py)
        save_metadata(fi,fdic,os.path.join(tiles_dir,'tiling_info.xml'))




def main():
    # if len(sys.argv) != 2:
    #     print('Usage: tile_images_cluster.py <root_dir>')
    #     exit()
    #
    # root_dir = str(sys.argv[1])  # abs path to where the images are

    root_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100/full_res'

    tile_images(root_dir)



if __name__ == '__main__':
    main()