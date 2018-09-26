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

slices = [76, 84, 124, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 220, 228, 236, 244, 252, 260,
          268, 276, 284, 292, 300, 308, 316, 332, 348, 356, 372, 380, 388, 396, 404, 420, 428,
          436, 460, 492, 508, 516, 532, 540, 556, 564, 612,636, 644, 652, 660, 668, 676, 684,
          692, 700, 708, 724, 732, 740, 748, 756, 764]

# slices = [99, 103, 107, 111, 115, 119, 123, 127, 131, 135, 139, 143,
#           147, 151, 155, 159, 163, 167, 171, 175, 179, 183, 187, 191, 195, 199, 203, 207, 211, 215, 219, 223, 227, 231,
#           235, 239, 243, 247, 251, 255, 259, 263, 267, 271, 275, 279, 283, 287, 291, 295, 299, 303, 307, 311, 315, 319,
#           323, 327, 331, 335, 339, 343, 347, 351, 355, 359, 363, 367, 371, 375, 379, 383, 387, 391, 395, 399, 403, 407,
#           411, 415, 419, 423, 427, 431, 435, 439, 443, 447, 451, 455, 459, 463, 467, 471, 475, 479, 483, 487, 491, 495,
#           499, 503, 507, 511, 515, 519, 523, 527, 531, 535, 539, 543, 547, 551, 555, 559, 563, 567, 571, 575, 579, 583,
#           587, 591, 595, 599, 603, 607, 611, 615, 619, 623, 627, 631, 635, 639, 643, 647, 651, 655, 659, 663, 667, 675,
#           679, 683, 687, 691, 695, 699, 703, 707, 711, 715, 719, 723, 727, 731]


slice_name='/home/maryana/storage2/Posdoc/AVID/AV23/AT100/full_res/AT100_{}/reg/combined_AT100_{}_heatmap_091218.nii'

for id in slices:

    try:
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
    except:
        print("Error loading slice {}".format(id))


hm_name='/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/AT100_heatmap2blockface_092018.nii'
nii2 = nib.Nifti1Image(vol2,nii.affine)
nib.save(nii2,hm_name)
print('Files {} sucessfully saved.'.format(hm_name))