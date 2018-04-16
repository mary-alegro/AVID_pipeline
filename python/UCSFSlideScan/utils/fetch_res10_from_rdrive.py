import os
import subprocess
import sys
import fnmatch
import skimage.io as io
import tifffile
from misc.XMLUtils import XMLUtils
import logging
import glob
import ConfigParser
import shutil

def get_img_info(root_dir):
    file_list = {}

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root, '*/RES(*'):  # it's inside /RES*
            for fn in fnmatch.filter(files, '*_res10.tif'):  # get only full resolution images
                file_name = os.path.join(root, fn)
                file_list[file_name] = {'home': root}
    return file_list


def fetch_files(root_dir,dest_dir):

    file_list = get_img_info(root_dir)

    for fi in file_list.keys():
        fdic = file_list[fi]
        home_dir = fdic['home']
        file_name = os.path.basename(fi)
        new_path = os.path.join(dest_dir,file_name)
        print('Copying {} to {}'.format(fi,new_path))
        shutil.copyfile(fi,new_path)


def main():

    root_dir = '/home/maryana/R_DRIVE/Experiments/AVID/Cases/1181-002/Master Package 1181-002/Images/Stitched/AT100'
    dest_dir = '/home/maryana/storage/Posdoc/AVID/AV23/AT100/res10'
    fetch_files(root_dir,dest_dir)

if __name__ == '__main__':
    main()
