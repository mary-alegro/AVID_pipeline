###################################################
#
#   Script to:
#   - Load the images and extract the patches
#   - Define the neural network
#   - define the training
#
##################################################


import numpy as np
import ConfigParser

from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, UpSampling2D, Reshape, core, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard
from keras import backend as K
from keras.utils.vis_utils import plot_model
from keras.optimizers import SGD
from ReconImageGenerator import ReconImageGenerator

import sys
#sys.path.insert(0, './util/')
from convnet.util.help_functions import *

#function to obtain data for training/testing (validation)
from convnet.util.extract_patches import get_data_training_rec1

def reshape_gd_1ch(masks):
    new_masks = np.empty((masks.shape[0],masks.shape[2]*masks.shape[3],masks.shape[1]))
    for i in range(masks.shape[0]):
        tmp = masks[i,...]
        new_masks[i,...] = tmp.reshape((tmp.shape[1]*tmp.shape[2],1))
    return new_masks

#Define the neural network
def get_recnet(n_ch, patch_height, patch_width):
    inputs = Input(shape=(n_ch,patch_height,patch_width))
    conv1 = Conv2D(320, (3, 3), activation='relu', padding='same',data_format='channels_first')(inputs)
    conv1 = Dropout(0.2)(conv1)
    conv1 = Conv2D(320, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)
    #
    conv2 = Conv2D(640, (3, 3), activation='relu', padding='same',data_format='channels_first')(pool1)
    conv2 = Dropout(0.2)(conv2)
    conv2 = Conv2D(640, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)
    #
    conv3 = Conv2D(1280, (3, 3), activation='relu', padding='same',data_format='channels_first')(pool2)
    conv3 = Dropout(0.2)(conv3)
    conv3 = Conv2D(1280, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv3)

    up1 = UpSampling2D(size=(2, 2))(conv3)
    up1 = concatenate([conv2,up1],axis=1)
    conv4 = Conv2D(640, (3, 3), activation='relu', padding='same',data_format='channels_first')(up1)
    conv4 = Dropout(0.2)(conv4)
    conv4 = Conv2D(640, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv4)
    #
    up2 = UpSampling2D(size=(2, 2))(conv4)
    up2 = concatenate([conv1,up2], axis=1)
    conv5 = Conv2D(320, (3, 3), activation='relu', padding='same',data_format='channels_first')(up2)
    conv5 = Dropout(0.2)(conv5)
    conv5 = Conv2D(320, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv5)
    #
    conv6 = Conv2D(1, (1, 1), activation='relu',padding='same',data_format='channels_first')(conv5)
    conv6 = core.Reshape((1,patch_height*patch_width))(conv6)
    conv6 = core.Permute((2,1))(conv6)
    ############
    #conv7 = core.Activation('softmax')(conv6)

    model = Model(input=inputs, output=conv6)

    #sgd = SGD(lr=0.01, decay=1e-5, momentum=0.3, nesterov=False)
    sgd = SGD(lr=0.001)
    #model.compile(optimizer=SGD(lr=0.001), loss='categorical_crossentropy',metrics=['accuracy'])
    #model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer=sgd, loss='mae', metrics=['mae'])

    return model


def run_training(conf_path=''):


    # train_imgs_original = '/home/maryana/Downloads/Spiralalgea/training/training_led.h5'
    # train_groudTruth = '/home/maryana/Downloads/Spiralalgea/10x_manual/ground_truth_1ch/gd_1ch.h5'
    #
    #
    # patches_imgs_train, patches_masks_train = get_data_training_rec1(
    #      DRIVE_train_imgs_original = train_imgs_original,
    #     DRIVE_train_groudTruth = train_groudTruth,  #masks
    #     #mean_image_path= '',
    #     patch_height = 48,
    #     patch_width = 48,
    #     N_subimgs = 2000,
    #     inside_FOV = False)
    # patches_masks_train = reshape_gd_1ch(patches_masks_train)  # reduce memory consumption

    img_dim = (48, 48, 275)
    n_ch = img_dim[2]
    patch_height = img_dim[0]
    patch_width = img_dim[1]
    model = get_recnet(n_ch, patch_height, patch_width)  #the U-net model
    print "Check: final output of the network:"
    print model.output_shape

    best_model_path = '/home/maryana/storage/Spiralalgea/best_weights.h5'
    last_model_path = '/home/maryana/storage/Spiralalgea/last_weights.h5'
    model_achitecture = '/home/maryana/storage/Spiralalgea/model_architecture.json'
    train_log = '/home/maryana/storage/Spiralalgea/logs'

    #plot_model(model, to_file= path_project + '_model.png')   #check how the model looks like
    json_string = model.to_json()
    open(model_achitecture, 'w').write(json_string)

    checkpointer = ModelCheckpoint(filepath= best_model_path, verbose=1, monitor='val_loss', mode='auto', save_best_only=True) #save at each epoch if the validation decreased
    tensorboard = TensorBoard(log_dir=train_log, histogram_freq=0, batch_size=32, write_graph=True, write_grads=False,
                                write_images=False, embeddings_freq=0, embeddings_layer_names=None,
                                embeddings_metadata=None)

    train_img_dir = '/home/maryana/storage/Spiralalgea/training/training_patches'
    gt_img_dir = '/home/maryana/storage/Spiralalgea/10x_manual/ground_truth_1ch/ground_truth_1ch_patches'
    test_train_img_dir = '/home/maryana/storage/Spiralalgea/training/training_test_patches'
    test_gt_img_dir = '/home/maryana/storage/Spiralalgea/10x_manual/ground_truth_1ch/gt_test_1ch_patches'
    minmax_img = '/home/maryana/storage/Spiralalgea/training/min_max.npy'
    minmax_gt = '/home/maryana/storage/Spiralalgea/10x_manual/ground_truth_1ch/min_max.npy'
    nClasses = 1  # actually, num. ground truth channels(# LEDs)
    batch_size = 32

    train_gen = ReconImageGenerator('train_gen',train_img_dir, gt_img_dir, minmax_img, minmax_gt, img_dim, batch_size, nClasses)
    test_gen = ReconImageGenerator('test_gen',test_train_img_dir, test_gt_img_dir, minmax_img, minmax_gt, img_dim, batch_size, nClasses)
    model.fit_generator(generator=train_gen.get_batch(),
                        validation_data=test_gen.get_batch(),
                        steps_per_epoch=train_gen.__len__(),
                        validation_steps=50,
                        epochs=1000,
                        verbose=1,
                        callbacks=[checkpointer, tensorboard])

    #model.fit(patches_imgs_train, patches_masks_train, nb_epoch=1000, batch_size=32, verbose=2, shuffle=True, validation_split=0.1, callbacks=[checkpointer,tensorboard])

    model.save_weights(last_model_path, overwrite=True)



def main():
    # if len(sys.argv) != 2:
    #     print('Usage: run_prediction <config_file.txt>')
    #     exit()
    #
    # config_path = str(sys.argv[1])
    #run_training(config_path)
    run_training()


if __name__ == '__main__':
    main()













