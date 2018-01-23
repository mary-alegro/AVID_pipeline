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
from skimage import transform as xform
import nibabel as nib



def sub2ind(size,r,c):
    ind = r*size[1]+c
    return ind




def main():

    tile_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/hm_tiles'
    nii_file = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/heat_map_res10.nii'

    final_size = np.array([3762,8170]) #rows,cols
    grid = np.array([9,20]) #rows,cols
    rscale = 0.10

    M = np.array([[0.0122, 0, 0, 0],[0, 0.0122, 0, 0], [0, 0, 0.0122, 0], [0, 0, 0, 1]])

    cols_idx = np.array([[np.zeros(grid[1])],[np.arange(grid[1])]])
    rows_idx = np.array([[np.arange(grid[0])],[np.zeros(grid[0])]])

    #get tiles widths (tiles may have arbitrary widths so I have to read all of them first)
    orig_width = 0
    new_width = 0
    nCols = cols_idx.shape[2]
    for f in range(nCols):
        file_name = os.path.join(tile_dir,'tile_{:04d}_hm_pertissue.npy'.format(f))
        data = np.load(file_name)
        size = np.asarray(data.shape)
        nsize = size*rscale
        new_size = np.array([round(nsize[0]),round(nsize[1])])
        orig_width += size[1]
        new_width += new_size[1]

    #get tiles widths (tiles may have arbitrary widths so I have to read all of them first)
    orig_height = 0
    new_height = 0
    nRows = rows_idx.shape[2]
    for f in range(nRows):
        file_name = os.path.join(tile_dir,'tile_{:04d}_hm_pertissue.npy'.format(f))
        data = np.load(file_name)
        size = np.asarray(data.shape)
        nsize = size * rscale
        new_size = np.array([round(nsize[0]), round(nsize[1])])
        orig_height += size[0]
        new_height += new_size[0]


    #create image
    img = np.zeros((int(new_height),int(new_width)))
    for r in range(grid[0]):
        for c in range(grid[1]):
            file_idx = sub2ind(grid,r,c)
            file_name = os.path.join(tile_dir,'tile_{:04d}_hm_pertissue.npy'.format(file_idx))
            tile = np.load(file_name)

            new_r = int(round(tile.shape[0]*rscale))
            new_c = int(round(tile.shape[1]*rscale))

            tile2 = xform.resize(tile,(new_r,new_c))

            img[r:r+new_r,c:c+new_c] = tile2

    img_final = xform.resize(img,final_size)
    nii_img = nib.Nifti1Image(img_final, affine=M)
    nib.save(nii_img,nii_file)



if __name__ == '__main__':
    main()