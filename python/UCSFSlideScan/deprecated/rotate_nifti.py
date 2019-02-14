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


def convert_png2nii(files_dir,out_dir,M=np.eye(4)):
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
    files_dir='/Users/maryana/Posdoc/AVID/AV23/blockface/aligned'
    out_dir = '/Users/maryana/Posdoc/AVID/AV23/blockface/nii'
    M = np.array([[0.114, 0, 0, 0], [0, 0.114, 0, 0], [0, 0, 0.114, 0], [0, 0, 0, 1]])
    convert_png2nii(files_dir,out_dir,M)


if __name__ == '__main__':
    main()