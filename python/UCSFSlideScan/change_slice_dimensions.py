
import nibabel as nib
import numpy as np

slices = [296,312,328,344,360,376,392,408,424,440,457,472,488,504,520,536,552,568,584,600,616,632,648]
M1 = np.eye(4)
M = M1*np.array([0.0123, 0.0123, 0.122,1])
for slice in slices:
    print('Editing slice {}'.format(slice))
    npy_name = '/home/maryana/storage/Posdoc/AVID/AV13/AT100/full_res/AT100_{}/heat_map/hm_map_0.1/heat_map_0.1_res10.npy'.format(slice)
    nii_name = '/home/maryana/storage/Posdoc/AVID/AV13/AT100/full_res/AT100_{}/heat_map/hm_map_0.1/heat_map_0.1_res10_v2.nii'.format(slice)
    hm = np.load(npy_name)
    hm_nii = nib.Nifti1Image(hm,M)
    nib.save(hm_nii,nii_name)

