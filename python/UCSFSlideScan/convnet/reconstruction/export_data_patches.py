
import os
import numpy as np
from PIL import Image
import skimage.io as io
import sys
import matplotlib.pyplot as plt
import sklearn.feature_extraction as fx
from skimage import img_as_ubyte
import glob
import convnet.strided_patches as sp
import tifffile

S = 16 #stride
F = 48 #window size (final patch size)

def create_dataset(orig_imgs_dir, patches_dir, patch_size, stride):

    S = stride
    F = patch_size

    #get training image info
    files = glob.glob(os.path.join(orig_imgs_dir, '*.tif'))
    files.sort(key=lambda f: int(filter(str.isdigit, f)))
    nCh = len(files) #each file is a channel
    tiff = tifffile.TiffFile(files[0])  # load tiff header only
    size = tiff.series[0].shape
    print('Dataset size: {},{},{}'.format(size[0],size[1],nCh))

    #total num. patches
    nPat_rows = int(sp.compute_num_patches(size[0], S))
    nPat_cols = int(sp.compute_num_patches(size[1], S))
    nPatches = nPat_cols*nPat_rows

    tmp_arr_path = os.path.join(patches_dir,'tmp_patches_arr.npy')
    tmp_arr = np.memmap(tmp_arr_path,dtype='float',mode='w+',shape=(nPatches,nCh,F,F))

    #copy data to temporary memory mapped array
    #for c in range(nCh): #each file = 1 channel
    arr_min = sys.maxint
    arr_max = -1
    for c in range(nCh):
        print('Processing channel {}'.format(c))
        file_name = files[c]
        img = io.imread(file_name)
        strided_img = sp.get_strided_view(img, F, S)
        patch_index = 0

        #get min and max values
        tmp_min = img.min()
        if tmp_min < arr_min:
            arr_min = img.min()
        tmp_max = img.max()
        if tmp_max > arr_max:
            arr_max = tmp_max

        for i in range(nPat_rows):
            for j in range(nPat_cols):
                patch = strided_img[i,j,...]
                tmp_arr[patch_index,c,...] = patch

                patch_index += 1

        del strided_img

    min_max = np.array([arr_min,arr_max])
    min_max_file = os.path.join(patches_dir,'min_max.npy')
    np.save(min_max_file,min_max)

    print('Saving patches.')
    #save patches to files
    for p in range(nPatches):
        patch = tmp_arr[p,...]
        patch_name = os.path.join(patches_dir,'patch_{}.npy'.format(p))
        np.save(patch_name,patch)

    del tmp_arr
    print('Finished.')



def main():

    if len(sys.argv) != 5:
        print('Usage: export_data_patches.py <absolute_path_to_imgs> <dataset_path_images> <patch_size> <stride>')
        exit()

    original_imgs_dir = str(sys.argv[1])
    dataset_img_dir = str(sys.argv[2])
    patch_size = int(sys.argv[3])
    stride = int(sys.argv[4])

    create_dataset(original_imgs_dir, dataset_img_dir, patch_size, stride)



if __name__ == '__main__':
    main()