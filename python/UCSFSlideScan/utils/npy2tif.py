import glob
import os
import sys
import numpy as np
import cv2
import argparse


def convert_npy(npy_dir):
    list_files = glob.glob(os.path.join(npy_dir,'*.npy'))
    for file_name in list_files:
        mask = np.load(file_name)
        fore = mask[...,0]
        cv2.imwrite(file_name+'.tif',fore)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d','--dir', required=True, help='directory with npy files')
    args = vars(ap.parse_args())
    npy_dir = args['dir']

    convert_npy(npy_dir)


if __name__ == '__main__':
    main()
