import glob
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import skimage.io as io
from skimage import color
from skimage import exposure as exp
from skimage import filters as filt
from skimage import morphology as morph
import mahotas as mht
import os
from skimage import img_as_float, img_as_ubyte
from skimage import transform as xform
import ntpath


MASK_VAL = 255

def apply_masks(imgtiles,masktiles,outtiles):
    #IMGTILES: folder where the histology img tiles are located
    #MASKTILES: folder where the mask tiles are located
    #OUTTILES: folder where masked images are saved

    files_mask = glob.glob(os.path.join(masktiles,'*.tif'))
    files_img = glob.glob(os.path.join(imgtiles,'*.tif'))

    nMasks = len(files_mask)
    nImgs = len(files_img)

    if nMasks != nImgs:
        print("Error: the number of masks and images must match.")
        return
    else:
        print("Found " + str(nImgs) + " images to mask.")

    for f in range(nMasks):
        img_file = os.path.join(imgtiles,files_img[f])
        base_name = ntpath.basename(img_file)
        mask_file = os.path.join(masktiles,'mask_'+base_name)
        mask = io.imread(mask_file)
        img = io.imread(img_file)
        if not (mask.shape[0] == img.shape[0] and mask.shape[1] == mask.shape[1]):
            tmp = mht.imresize(mask,(img.shape[0],img.shape[1]))
            tmp[tmp < 1] = 0
            tmp[tmp > 0] = 255
            mask = tmp.astype('ubyte')


        size = img.shape[0:2]

        R = img[...,0].copy()
        G = img[...,1].copy()
        B = img[...,2].copy()

        R[mask < MASK_VAL] = 0
        G[mask < MASK_VAL] = 0
        B[mask < MASK_VAL] = 0

        R = R.reshape([size[0],size[1],1])
        G = G.reshape([size[0],size[1],1])
        B = B.reshape([size[0],size[1],1])

        img2 = np.concatenate((R,G,B),axis=2)

        out_file = os.path.join(outtiles,base_name)
        #io.imsave(out_file,img2)
        mht.imsave(out_file,img2)
        print("File " + base_name + " saved.")


def main():
    maskdir = '/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/tiles_mask'
    imgdir = '/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/tiles'
    outdir = '/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/tiles_seg'

    apply_masks(imgdir,maskdir,outdir)

    print('Images were successfully processed.')

if __name__ == '__main__':
    main()

