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
import compute_heatmap_par as cp_hm



NPIX_MM = 819 #num. pixels in 1mm
NBLOCK_TILE = 5 #tiles are 5x5 grid with 1mm^2 each
MAX_VALUE = 65535 #16bits
N_WORKERS = 2


def get_files_dic(root_dir):
    dir_dic = {}
    list_dirs = glob.glob(root_dir + '/*/')
    for ldir in list_dirs:
        if os.path.isdir(ldir):
            if ldir.find('magick_tmp') != -1:
                continue
            xml_meta_file = os.path.join(ldir, 'heat_map/TAU_seg_tiles/tiles_metadata.xml')
        dir_dic[ldir] = xml_meta_file

    return dir_dic


def run_compute_hm(root_dir):
    case_dir_list = get_files_dic(root_dir)
    for rdir in case_dir_list.keys():
        xml_file = case_dir_list[rdir]

        print('Creating heatmap {}'.format(rdir))
        cp_hm.exec_compute_heatmap(rdir,xml_file)



def main():
    if len(sys.argv) != 2:
        print('Usage: run_compute_heatmap_0.1.py <root_dir> ')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    run_compute_hm(root_dir)


if __name__=='__main__':
    main()