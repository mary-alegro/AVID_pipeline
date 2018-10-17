import tifffile
import os
import glob


mask_path = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/slidenet_2classes/training/masks/patches'
img_path = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/slidenet_2classes/training/images/patches'

files = glob.glob(os.path.join(img_path,'*.tif'))
for f in files:
    basename = os.path.basename(f)
    name = basename[5:-4]
    mask_name = os.path.join(mask_path,'patch_mask' + name + '.npy')
    tiff = tifffile.TiffFile(f)
    size = tiff.series[0].shape
    if size[0] < 818 or size[1] < 818:
        print(f)
        print(mask_name)
        os.remove(f)
        os.remove(mask_name)

