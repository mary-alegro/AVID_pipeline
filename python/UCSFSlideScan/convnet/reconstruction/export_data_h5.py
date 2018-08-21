import os
import h5py
import glob
import tifffile
import numpy as np
import skimage.io as io
import sys


def write_hdf5(arr,outfile):
  with h5py.File(outfile,"w") as f:
    f.create_dataset("image", data=arr, dtype=arr.dtype)


def save_as_hdf5(img,file_path,file_name):
    new_name = file_name[0:-4] + '.hdf5'
    img_name = os.path.join(file_path,new_name)
    write_hdf5(img,img_name)


def extract_data(imgs_dir,out_file):
    files = glob.glob(os.path.join(imgs_dir,'*.tif'))
    files.sort(key=lambda f: int(filter(str.isdigit, f)))
    nCh = len(files) #each file is a channel
    tiff = tifffile.TiffFile(files[0])  # load tiff header only
    size = tiff.series[0].shape

    print('Volume size: {},{},{}'.format(size[0],size[1],nCh))

    vol = np.empty((size[0], size[1], nCh))

    print('Reading files')

    count = 0
    for fi in files:
        img = io.imread(fi)
        vol[...,count] = img
        count += 1


    print('Saving')

    write_hdf5(vol,out_file)


def main():
    if len(sys.argv) != 3:
        print('Usage: export_data_h5.py <imgs_dir> <out_file>')
        exit()

    imgs_dir = str(sys.argv[1])
    out_file = str(sys.argv[2])

    extract_data(imgs_dir,out_file)


if __name__ == '__main__':
    main()
