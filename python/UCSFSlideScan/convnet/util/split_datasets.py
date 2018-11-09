import sys
import os
import glob
import numpy as np
import random


def split_dataset(orig_imgs_dir,mask_imgs_dir,data_img_dir,data_mask_dir,ptrain,ptest):

    imgs_list = glob.glob(os.path.join(orig_imgs_dir,'*.tif'))
    nFiles = len(imgs_list)
    nTrain = int(np.round(nFiles*ptrain))
    nTest = int(np.round(nFiles*ptest))

    #shuffle list
    random.shuffle(imgs_list)


    test_list = imgs_list[0:nTest]
    train_list = imgs_list[nTest:nTest+nTrain]


    # print('Creating training set...')
    # for l in train_list:
    #     img_bname = os.path.basename(l)
    #     mask_bname = 'patch_mask' + img_bname[5:-4] + '.npy'
    #     img_name = os.path.join(orig_imgs_dir,img_bname)
    #     new_img_name = os.path.join(data_img_dir,img_bname)
    #
    #     mask_name = os.path.join(mask_imgs_dir,mask_bname)
    #     new_mask_name = os.path.join(data_mask_dir,mask_bname)
    #
    #     print('{} --> {}'.format(img_name,new_img_name))
    #     print('{} --> {}'.format(mask_name,new_mask_name))
    #
    #     # os.rename(img_name,new_img_name)
    #     # os.rename(mask_name,new_mask_name)

    print('Creating testing set...')
    for l in test_list:
        img_bname = os.path.basename(l)
        mask_bname = 'patch_mask' + img_bname[5:-4] + '.npy'
        img_name = os.path.join(orig_imgs_dir, img_bname)
        new_img_name = os.path.join(data_img_dir, img_bname)

        mask_name = os.path.join(mask_imgs_dir, mask_bname)
        new_mask_name = os.path.join(data_mask_dir, mask_bname)

        print('{} --> {}'.format(img_name, new_img_name))
        print('{} --> {}'.format(mask_name, new_mask_name))

        os.rename(img_name,new_img_name)
        os.rename(mask_name,new_mask_name)


def main():

    if len(sys.argv) != 7:
        print('Usage: split_datasets <absolute_path_to_imgs> <absolute_path_to_masks> <dataset_path_images> <dataset_path_masks> <percent_training> <percent_testing>')
        exit()

    original_imgs_dir = str(sys.argv[1])
    mask_imgs_dir = str(sys.argv[2])
    dataset_img_dir = str(sys.argv[3])
    dataset_mask_dir = str(sys.argv[4])
    percent_train = float(sys.argv[5])
    percent_test = float(sys.argv[6])

    split_dataset(original_imgs_dir,mask_imgs_dir,dataset_img_dir,dataset_mask_dir,percent_train,percent_test)




if __name__ == '__main__':
    main()