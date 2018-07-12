
import os
import h5py
import numpy as np
from PIL import Image
import skimage.io as io
import sys
import matplotlib.pyplot as plt
from skimage import img_as_ubyte


def write_hdf5(arr,outfile):
  with h5py.File(outfile,"w") as f:
    f.create_dataset("image", data=arr, dtype=arr.dtype)


def get_datasets(Nimgs,height,width,channels,imgs_dir,groundTruth_dir,train_test="train"):
    imgs = np.empty((Nimgs,height,width,channels))
    groundTruth = np.empty((Nimgs,height,width,3)) #tau, threads, GM + black bkg
    for path, subdirs, files in os.walk(imgs_dir): #list all files, directories in the path
        for i in range(len(files)):
            #original
            print "original image: " +files[i]
            #img = Image.open(imgs_dir+files[i])
            img_name = os.path.join(imgs_dir,files[i])
            ext = img_name[-3:]
            if ext != 'tif':
                continue

            img = io.imread(img_name)
            #corresponding ground truth
            groundTruth_name = files[i][0:-4] + "_mask.tif"
            print "ground truth name: " + groundTruth_name
            #g_truth = Image.open(groundTruth_dir + groundTruth_name)
            g_truth = io.imread(os.path.join(groundTruth_dir, groundTruth_name))
            g_truth = img_as_ubyte(g_truth)

            img_rows,img_cols = img.shape[0:2]
            if img_rows > height:
                img = img[0:height,:,:]
                g_truth = g_truth[0:height,:]
            if img_cols > width:
                img = img[:,0:width,:]
                g_truth = g_truth[:,0:width]

            #image
            imgs[i, ...] = img

            #convert mask from color to binary mask
            #black background = [255,255,10]
            #roxo gray matter = [198,118,255]
            #verde filamentos TAU = [79,255,130]
            #vermelho celulas TAU = [255,0,0]
            mask_bkg = g_truth[...,2] == 10
            mask_gm = g_truth[...,2] == 255
            mask_thread = g_truth[...,2] == 130
            mask_cell = g_truth[...,2] == 0

            groundTruth[i,:,:,0] = mask_cell * 255
            groundTruth[i,:,:,1] = mask_thread * 255
            groundTruth[i,:,:,2] = (mask_gm | mask_bkg) * 255 #black background and GM together
            #groundTruth[i,:,:,3] = mask_bkg * 255


    print "imgs max: " +str(np.max(imgs))
    print "imgs min: " +str(np.min(imgs))

    print "ground truth and border masks are correctly withih pixel value range 0-255 (black-white)"
    #reshaping for my standard tensors
    imgs = np.transpose(imgs,(0,3,1,2))
    #groundTruth = np.reshape(groundTruth,(Nimgs,1,height,width))
    return imgs, groundTruth

def main():

    if len(sys.argv) != 5:
        print('Usage: prepare_datasets <absolute_path_to_imgs> <absolute_path_to_masks> <dataset_path> <train|test> ')
        exit()

    original_imgs = str(sys.argv[1])
    groundTruth_imgs = str(sys.argv[2]) #row size
    dataset_path = str(sys.argv[3])
    dstype =  str(sys.argv[4])

    # #rectify strings
    # if not original_imgs.endswith('/'):
    #     original_imgs = original_imgs + '/'
    # if not groundTruth_imgs.endswith('/'):
    #     groundTruth_imgs = groundTruth_imgs + '/'
    # if not dataset_path.endswith('/'):
    #     dataset_path = dataset_path + '/'


    file_list = os.listdir(original_imgs)
    Nimgs = len(file_list)
    if Nimgs == 0:
        print("Images folder is empty")
        exit()
    img_tmp = io.imread(os.path.join(original_imgs,file_list[0]))
    height = img_tmp.shape[0]
    width = img_tmp.shape[1]
    if img_tmp.ndim == 2:
        channels = 1
    else:
        channels = img_tmp.shape[2]

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # getting the training datasets
    imgs_train, groundTruth_train = get_datasets(Nimgs,height,width,channels,original_imgs, groundTruth_imgs, dstype)
    print "saving train datasets"
    write_hdf5(imgs_train, os.path.join(dataset_path , "dataset_imgs_" + dstype + ".hdf5"))
    write_hdf5(groundTruth_train, os.path.join(dataset_path, "dataset_groundTruth_" + dstype + ".hdf5"))


if __name__ == '__main__':
    main()