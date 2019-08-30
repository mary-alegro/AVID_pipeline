import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import matplotlib as mpl
import matplotlib.cm as cm
from skimage import img_as_ubyte

nii = nib.load('/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/av23_blockface.nii')
#nii = nib.load('/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/av23_blockface.nii')

#nii = nib.load('/homecreate_heatmap2block.py/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/av23_blockface.nii')
vol = nii.get_data()
vol2 = np.zeros(vol.shape)

#AV1 AT8
# slices = [282, 286, 290, 294, 295, 298, 302, 306, 311, 314, 318, 322, 326, 327, 330, 334, 338, 343, 346, 350, 354, 358,
#           362, 366, 370, 374, 378, 382, 386, 390, 394, 398, 402, 406, 410, 414, 418, 422, 430, 434, 438, 442, 448, 454,
#           458, 462, 466, 470, 474, 478, 482, 486, 490, 494, 498, 502, 506, 510, 514, 518, 522, 526, 530, 534, 538, 542,
#           546, 550, 558, 562, 566, 570, 574, 578, 582, 586, 590, 594, 598, 602, 606, 610, 614, 618, 622, 626, 630, 634,
#           638, 642, 650, 654, 658]

# #AV2 AT8
# slices = [99,107,111,115,119,123,127,131,135,139,143,147,151,155,167,171,175,179,183,187,191,195,199,203,207
#     ,211,215,219,223,231,235,239,243,247,251,255,259,263,267,271,275,283,287,291,295,299,303,307,311,315,319,323
#     ,327,331,335,339,343,347,351,355,363,367,371,375,379,383,387,391,403,407,411,415,419,423,427,431,435,439
#     ,443,447,451,455,459,463,467,471,475,479,483,487,495,499,503,507,511,515,519,523,527,531,535,539,547,551,555
#     ,559,563,567,571,575,579,583,587,591,595,599,603,607,611,615,623,627,631,635,639,643,647,651,655,659,663,667
#     ,675,679,683,687,691,695,699,711,715,719,723,727,731]

# AV1 AT100
slices = [76,84,92,98,100,116,124,132,140,148,156,164,172,180,188,196,204,212,220,228,236,244,252,260,268,276,284,292,300,
         308,316,324,332,348,356,364,372,380,388,396,404,412,420,428,436,444,452,460,468,476,484,492,500,508,516,524,532,
         540,548,556,564,572,580,588,596,604,612,620,628,636,644,652,660,673,676,684,692,700,708,724,732,737,740,745,748,
         753,756]


#slice_name = '/home/maryana/storage2/Posdoc/AVID/AV13/AT8/registered/combined_AT8_{}_heatmap_0719.nii'
#slice_name = '/home/maryana/storage2/Posdoc/AVID/AV23/AT8/registered/combined_AT8_{}_heatmap_aaic.nii'
slice_name = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/registered_files/combined_AT100_{}_heatmap_aaic.nii'

nSlices = len(slices)

for s in range(nSlices):
    id = slices[s]
    if s == nSlices-1:
        id2 = slices[s]
    else:
        id2 = slices[s+1]

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

        for ss in range(id-1,id2-1):
            vol2[:,:,ss] = simg
    except Exception as e:
        print("Error loading slice {}".format(id))
        print(e)


#hm_name='/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/AT8_heatmap2blockface_072019_AAIC.nii'
hm_name='/home/maryana/storage2/Posdoc/AVID/AV23/blockface/nii/AT100_heatmap2blockface_072019_AAIC.nii'
nii2 = nib.Nifti1Image(vol2,nii.affine)
nib.save(nii2,hm_name)
print('Files {} sucessfully saved.'.format(hm_name))