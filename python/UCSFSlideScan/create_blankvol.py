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
import nibabel as nib


def create_vol(out_dir,size,M=np.eye(4)):
    for root, dir, files in os.walk(files_dir):
        nTotal = len(files)
        print('{} file(s) found.'.format(nTotal))
        for fname in fnmatch.filter(files, '*.nii'):
            img_name = os.path.join(root,fname)
            nii = nib.load(img_name)
            img = nii.get_data()

            img2 = np.rot90(img,axes=(1,0))
            img3 = np.flip(img2,axis=1)

            nii2 = nib.Nifti1Image(img3, affine=M)
            nii_name=os.path.join(out_dir,fname)
            nib.save(nii2,nii_name)

def main():
    out_dir = '/home/maryana/storage/Posdoc/AVID/AV13/blockface/nii3'
    M = np.array([[0.123, 0, 0, 0], [0, 0.123, 0, 0], [0, 0, 0.123, 0], [0, 0, 0, 1]])
    size = np.array([864,1296])
    srange = np.array([0,834])
    name_pt = '1181_001-Whole-Brain_{:04d}.png.nii'

    ini_a = srange[0]
    ini_b = srange[1]

    img = np.zeros(size)
    nii = nib.Nifti1Image(img, affine=M)

    for f in range(ini_a,ini_b):
        name = name_pt.format(f+1)
        name_path = os.path.join(out_dir,name)
        nib.save(nii,name_path)



if __name__ == '__main__':
    main()