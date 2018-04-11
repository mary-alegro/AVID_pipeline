import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import matplotlib as mpl
import matplotlib.cm as cm
from skimage import img_as_ubyte

nii = nib.load('/home/maryana/storage/Posdoc/AVID/AV13/blockface/nii/av13_blockface.nii')
vol = nii.get_data()
vol2 = np.zeros(vol.shape)

slices = [360,392,408,504,296,440,457,472,488,552,600,632,648]
slice_name='/home/maryana/storage/Posdoc/AVID/AV13/AT100/full_res/resize_mary/AT100_{}/reg/elastix_AT100_{}_heatmap_bspline.nii'

for id in slices:
    name = slice_name.format(str(id),str(id))
    slice = nib.load(name)
    simg = slice.get_data()
    # norm = mpl.colors.Normalize(vmin=simg.min(),vmax=simg.max())
    # cmap = cm.gray
    # img = cmap(norm(simg))
    # img2 = img_as_ubyte(img)
    # hmap = img2[:, :, 0]    #
    # vol2[:,:,id-1]=hmap
    vol2[:,:,id-1] = simg

hm_name='/home/maryana/storage/Posdoc/AVID/AV13/blockface/nii/heatmap2blockface.nii'
nii2 = nib.Nifti1Image(vol2,nii.affine)
nib.save(nii2,hm_name)
print('Files {} sucessfully saved.'.format(hm_name))