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
import skimage.color as color
import nibabel as nib
import re

'''
Creates the blockface volume from individual slices. Assumes slices are coronal. 
'''

def get_block_info(files_dir, name_pt, file_ext='png'):

    list_files = glob.glob(os.path.join(files_dir, '*.' + file_ext))
    nFiles = len(list_files)
    file_tmp = name_pt.format(nFiles/2)
    file_tmp = os.path.join(files_dir,file_tmp)
    tmp = io.imread(file_tmp)

    return tmp.shape[0],tmp.shape[1],nFiles

def create_volume(files_dir, out_name, name_pt, file_ext, dim_x, dim_y, dim_z):
    rows,cols,nFiles = get_block_info(files_dir, name_pt, file_ext)

    print('Blockface size: {}x{}x{} | Dims: X: {} Y: {} Z: {}'.format(cols,rows,nFiles,dim_x,dim_y,dim_z))

    vol = np.zeros((rows, cols, nFiles), dtype='uint8')

    print('Creating volume.')
    for n in xrange(nFiles): #make sure files are always sorted
        img_name = name_pt.format(nFiles)
        img_path = os.path.join(files_dir,img_name)
        img = io.imread(img_path)
        if img.ndim > 2:
            img = img[...,0]

        vol[...,n] = img

    cos_g = np.cos(np.pi / 2)
    sin_g = np.sin(np.pi / 2)
    S = np.array([[dim_x, 0, 0, 0],[0, dim_y, 0, 0],[0, 0, dim_z, 0],[0, 0, 0, 1]]) #scaling (gives voxels size)
    Rx = np.array([[1,0,0,0],[0,cos_g,-sin_g,0],[0,sin_g,cos_g,0],[0,0,0,1]]) #rotations around X
    Ry = np.array([[cos_g, 0, sin_g, 0], [0, 1, 0, 0], [-sin_g, 0, cos_g, 0], [0, 0, 0, 1]]) #rotation around Y
    M = Rx.dot(Ry.dot(S)) #vol affine vox2ras matrix

    print('Saving {}'.format(out_name))
    nii = nib.Nifti1Image(vol,M)
    nib.save(nii,out_name)

def get_file_ext(file_name_pt):
    index = [m.start() for m in re.finditer('\.',file_name_pt)]
    last_idx = index[-1]
    ext = file_name_pt[last_idx+1:]

    return ext


def main():
    if len(sys.argv) != 7:
        print('Usage: create_blockface_vol.py <slices_dir> <file_name_pattern> <x_size> <y_size> <z_size> <nifti_3d_file>')
        exit()
    slices_dir = str(sys.argv[1])  # abs path to where the images are
    name_pt= str(sys.argv[2])
    x_size = float(sys.argv[3])
    y_size = float(sys.argv[4])
    z_size = float(sys.argv[5])
    nii_file = str(sys.argv[6])

    file_ext = get_file_ext(name_pt)

    create_volume(slices_dir, nii_file, name_pt, file_ext, x_size, y_size, z_size)

if __name__ == '__main__':
    main()