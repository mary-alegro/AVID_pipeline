import sys
import nibabel as nib


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: mask_bganglia.py <orig_file.nii> <mask_file.nii>')
        exit()

    orig_file = sys.argv[1]
    mask_file = sys.argv[2]

    orig_nii = nib.load(orig_file)
    mask_nii = nib.load(mask_file)

    orig_img = orig_nii.get_data()
    mask = mask_nii.get_data()
    mask[mask > 0] = 255

    orig_img[mask < 255] = 0

    new_nii = nib.Nifti1Image(orig_img,orig_nii.affine)
    nib.save(new_nii,orig_file+'_no_bganglia.nii')