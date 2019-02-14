import glob
import os
import numpy as np
import random



train_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT8/db_training'
test_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT8/db_testing'
val_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT8/db_validation'


train_dir_img = os.path.join(train_dir,'images')
train_dir_masks = os.path.join(train_dir,'masks')
test_dir_img = os.path.join(test_dir,'images')
test_dir_masks = os.path.join(test_dir,'masks')
val_dir_img = os.path.join(val_dir,'images')
val_dir_masks = os.path.join(val_dir,'masks')

if not os.path.exists(test_dir_img):
    os.mkdir(test_dir_img)
if not os.path.exists(test_dir_masks):
    os.mkdir(test_dir_masks)
if not os.path.exists(val_dir_img):
    os.mkdir(val_dir_img)
if not os.path.exists(val_dir_masks):
    os.mkdir(val_dir_masks)

patches = glob.glob(os.path.join(train_dir_img,'*.tif'))
nPatches = len(patches)

nVal = int(np.ceil(0.10*nPatches))
nTest = int(np.ceil(0.10*nPatches))

index = range(nPatches)
random.shuffle(index)

index_test = index[0:nTest]
index_val = index[nTest:nTest+nVal]

print('Moving TEST files:')
for ind in index_test:
    image_name = patches[ind]
    basename = os.path.basename(image_name)
    mask_basename = (basename[:-4] + '_mask.tif')
    mask_name = os.path.join(train_dir_masks,mask_basename)

    new_image_name = os.path.join(test_dir_img,basename)
    new_mask_name = os.path.join(test_dir_masks,mask_basename)

    print('{} to {}'.format(image_name,new_image_name))
    print('{} to {}'.format(mask_name,new_mask_name))

    os.rename(image_name,new_image_name)
    os.rename(mask_name,new_mask_name)

print('Moving VALIDATION files:')
for ind in index_val:
    image_name = patches[ind]
    basename = os.path.basename(image_name)
    mask_basename = (basename[:-4] + '_mask.tif')
    mask_name = os.path.join(train_dir_masks, mask_basename)

    new_image_name = os.path.join(val_dir_img, basename)
    new_mask_name = os.path.join(val_dir_masks, mask_basename)

    print('{} to {}'.format(image_name, new_image_name))
    print('{} to {}'.format(mask_name, new_mask_name))

    os.rename(image_name,new_image_name)
    os.rename(mask_name,new_mask_name)










