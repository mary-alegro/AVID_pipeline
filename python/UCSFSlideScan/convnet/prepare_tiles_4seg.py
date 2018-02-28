
import os
import h5py
import numpy as np
from PIL import Image
import skimage.io as io
import sys
import matplotlib.pyplot as plt
import fnmatch
from shutil import copyfile

PIX_MIN = 0.015

def write_hdf5(arr,outfile):
  with h5py.File(outfile,"w") as f:
    f.create_dataset("image", data=arr, dtype=arr.dtype)


def save_as_hdf5(img,file_path,file_name):
    new_name = file_name[0:-4] + '.hdf5'
    img_name = os.path.join(file_path,new_name)
    write_hdf5(img,img_name)


def run_prepare(tiles_dir, out_dir, bkg_out_dir, file_ext):

    nHDF5 = 0
    nBkg = 0

    for root, dir, files in os.walk(tiles_dir):

        nTotal = len(files)
        print('{} tile(s) found.'.format(nTotal))

        for fname in fnmatch.filter(files, '*.'+file_ext):
            img_path = os.path.join(root,fname)
            img = io.imread(img_path)
            npix = float(img.shape[0] * img.shape[1])
            R = img[:,:,0]
            G = img[:,:,1]
            B = img[:,:,2]

            #num. non zeros in the red channel
            tmp_nnz_r = R.flatten().nonzero()
            nnz_r = float(len(tmp_nnz_r[0]))
            pnnz_r = nnz_r/npix

            #num. non zeros in the green channel
            tmp_nnz_g = G.flatten().nonzero()
            nnz_g = float(len(tmp_nnz_g[0]))
            pnnz_g = nnz_g/npix

            #num. non zeros in the blue channel
            tmp_nnz_b = B.flatten().nonzero()
            nnz_b = float(len(tmp_nnz_b[0]))
            pnnz_b = nnz_b/npix

            if pnnz_r > PIX_MIN or pnnz_g > PIX_MIN or pnnz_b > PIX_MIN: #if any one of the channels has information, go to processing
                save_as_hdf5(img,out_dir,fname)
                nHDF5+=1
            else: #else, it's a background image
                new_path = os.path.join(bkg_out_dir,fname)
                copyfile(img_path,new_path)
                nBkg+=1

    print('{} files were saved as HDF5.'.format(nHDF5))
    print('{} files were saved as background.'.format(nBkg))


def main():
    if len(sys.argv) != 5:
         print('Usage: run_prediction <tiles_dir> <out_hdf5_dir> <TAU_seg_dir> <img_ext>')
         exit()
    
    tiles_dir = str(sys.argv[1])
    out_dir = str(sys.argv[2])
    bkg_out_dir  = str(sys.argv[3])
    img_ext = str(sys.argv[4])

    #tiles_dir='/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/AT100440/seg_tiles'
    #out_dir='/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/AT100440/hdf5_tiles'
    #bkg_out_dir = '/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/AT100440/TAU_seg_tiles'
    #img_ext = 'tif'

    run_prepare(tiles_dir,out_dir,bkg_out_dir,img_ext)

if __name__ == '__main__':
    main()
