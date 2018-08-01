import skimage.io as io
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
import glob
import convnet.util.pre_processing as pp
import os
import random
import numpy as np
import keras

class TauImageGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self,images_dir,masks_dir,mean_img,batch_size,do_augmentation=False,augment_percent=0.20):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        #self.mean_image_path = mean_img
        self.batch_size = batch_size
        self.mu = pp.load_mean_values(mean_img)

        #get file names
        self.back_img_list = glob.glob(os.path.join(images_dir, '*_1_*.tif'))
        self.fore_img_list = glob.glob(os.path.join(images_dir, '*_0_*.tif'))
        #get num of bkg and tau tiles
        self.nBack = len(self.back_img_list)
        self.nFore = len(self.fore_img_list)
        #shuffle arrays
        self.shuffle_files()
        self.do_aug = do_augmentation
        self.augment_percent = augment_percent

        if self.batch_size % 2 != 0:
            print('Warning: batch size must be an even number. Adjusting.')
            self.batch_size += 1


    def balance_data(self):
        if self.nFore < self.nBack:
            diff = self.nBack - self.nFore
            idx = np.random.choice(self.nFore,diff,replace=False)
            tmp_list = [self.fore_img_list[i] for i in idx]
            self.fore_img_list.append(tmp_list)
        elif self.nFore > self.nBack:
            diff = self.nFore - self.nBack
            idx = np.random.choice(self.nBack,diff,replace=False)
            tmp_list = [self.back_img_list[i] for i in idx]
            self.back_img_list.append(tmp_list)

    def shuffle_files(self):
        random.shuffle(self.nBack)
        random.shuffle(self.nFore)


    def load_data(self):
        pass


    def __len__(self):
        return int(np.floor((self.nFore + self.nBack) / self.batch_size))

    def on_epoch_end(self):
        self.shuffle_files()

    def __getitem__(self, index):

        if not self.do_aug: #don't do data augmentation
            begin = index*self.batch_size
            end = begin + self.batch_size
            mid = index*int(self.batch_size/2)

            tmp_img_list = self.fore_img_list[begin:mid]
            tmp_img_list.append(self.back_img_list[mid:end])
            random.shuffle(tmp_img_list)


        for fi in tmp_img_list:
            img_name = os.path.basename(fi)











