import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import matplotlib as mpl
import matplotlib.cm as cm
from skimage import img_as_ubyte

nii = nib.load('/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/av23_blockface.nii')
vol = nii.get_data()
vol2 = np.zeros(vol.shape)

# slices = [76, 84, 100, 116, 124, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 220, 228, 236, 236, 244, 252, 260,
#           268, 276, 284, 288, 292, 300, 308, 316, 324, 332, 340, 348, 356, 364, 372, 380, 388, 396, 404, 412, 420, 428,
#           436, 452, 460, 468, 476, 484, 492, 500, 508, 516, 524, 532, 540, 548, 556, 564, 572, 580, 588, 596, 604, 612,
#           620, 628, 636, 644, 652, 660, 668, 676, 684, 692, 700, 703, 708, 716, 724, 732, 740, 748, 756, 764, 9298]

slices = [76, 84, 124, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 220, 228, 236, 236, 244, 252, 260,
          268, 276, 284, 292, 300, 308, 316, 332, 348, 356, 372, 380, 388, 396, 404, 420, 428,
          436, 460, 492, 508, 516, 532, 540, 556, 564, 612,636, 644, 652, 660, 668, 676, 684,
          692, 700, 708, 724, 732, 740, 748, 756, 764]

slice_name='/home/maryana/storage2/Posdoc/AVID/AV23/AT100/full_res/AT100_{}/reg/composed_AT100_{}_heatmap.nii'

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

hm_name='/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/AT100_heatmap2blockface.nii'
nii2 = nib.Nifti1Image(vol2,nii.affine)
nib.save(nii2,hm_name)
print('Files {} sucessfully saved.'.format(hm_name))