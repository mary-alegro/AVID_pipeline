import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from skimage import img_as_ubyte




def compute_colormaps(hist_dir,cmap_dir, vmin, vmax):

    norm = mpl.colors.Normalize(vmin=vmin,vmax=vmax)
    #cmap = cm.nipy_spectral
    cmap = cm.gray


    for root, dir, files in os.walk(hist_dir):
        for fname in fnmatch.filter(files, '*_hm_pertissue.npy'):
            file_path = os.path.join(root, fname)

            arr = np.load(file_path)
            img = cmap(norm(arr))
            img2 = img_as_ubyte(img)

            #remove alpha channel
            R = img2[:,:,0]
            # G = img2[:,:,1]
            # B = img2[:,:,2]
            # r,c = R.shape[0:2]
            # img3 = np.concatenate((R.reshape([r,c,1]),G.reshape([r,c,1]),B.reshape([r,c,1])),axis=2)

            new_name = os.path.join(cmap_dir,fname[0:-15]+'_cmap.tif')
            #io.imsave(new_name,img3)
            io.imsave(new_name,R)


def main():

    #npy_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/hm_tiles'
    #out_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/colormap_tiles'
    npy_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/hm_tiles_0.1'
    out_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/colormap_tiles_0.1'

    vmin = 0
    vmax = 66.1213
    #vmax = 28.7227577641 #per tissue
    #vmax = 1.00780147993 #per tile


    compute_colormaps(npy_dir,out_dir, vmin, vmax)


if __name__ == '__main__':
    main()