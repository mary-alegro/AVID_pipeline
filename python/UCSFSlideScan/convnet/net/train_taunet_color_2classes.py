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
import os

from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, UpSampling2D, Reshape, core, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard
from keras import backend as K
from keras.utils.vis_utils import plot_model
from keras.optimizers import SGD, Adam
from TauImageGenerator import TauImageGenerator

import sys
from convnet.util.help_functions import *

#function to obtain data for training/testing (validation)
from convnet.util.extract_patches import get_data_training_4classes


#Define the neural network
def get_taunet_2classes(n_ch, patch_height, patch_width):
    inputs = Input(shape=(n_ch,patch_height,patch_width))
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same',data_format='channels_first')(inputs)
    conv1 = Dropout(0.2)(conv1)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)
    #
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same',data_format='channels_first')(pool1)
    conv2 = Dropout(0.2)(conv2)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)
    #
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same',data_format='channels_first')(pool2)
    conv3 = Dropout(0.2)(conv3)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv3)

    up1 = UpSampling2D(size=(2, 2))(conv3)
    up1 = concatenate([conv2,up1],axis=1)
    conv4 = Conv2D(64, (3, 3), activation='relu', padding='same',data_format='channels_first')(up1)
    conv4 = Dropout(0.2)(conv4)
    conv4 = Conv2D(64, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv4)
    #
    up2 = UpSampling2D(size=(2, 2))(conv4)
    up2 = concatenate([conv1,up2], axis=1)
    conv5 = Conv2D(32, (3, 3), activation='relu', padding='same',data_format='channels_first')(up2)
    conv5 = Dropout(0.2)(conv5)
    conv5 = Conv2D(32, (3, 3), activation='relu', padding='same',data_format='channels_first')(conv5)
    #
    conv6 = Conv2D(2, (1, 1), activation='relu',padding='same',data_format='channels_first')(conv5)
    conv6 = core.Reshape((2,patch_height*patch_width))(conv6)
    conv6 = core.Permute((2,1))(conv6)
    ############
    conv7 = core.Activation('softmax')(conv6)

    model = Model(input=inputs, output=conv7)

    #sgd = SGD(lr=0.01, decay=1e-5, momentum=0.3, nesterov=False)
    sgd = SGD(lr=0.001,decay=1e-5)
    #adam = Adam(lr=0.01)
    #model.compile(optimizer=SGD(lr=0.001), loss='categorical_crossentropy',metrics=['accuracy'])
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def run_training(conf_path):

    config = ConfigParser.RawConfigParser()
    config.read(conf_path)

    #Experiment name
    name_experiment = config.get('experiment name', 'name')
    #training settings
    N_epochs = int(config.get('training settings', 'N_epochs'))
    batch_size = int(config.get('training settings', 'batch_size'))
    path_data = config.get('data paths', 'path_local')
    path_project = config.get('data paths', 'path_project')


    train_imgs_dir = os.path.join(path_data,config.get('data paths', 'train_imgs_original'))
    train_masks_dir = os.path.join(path_data,config.get('data paths', 'train_groundTruth'))
    test_imgs_dir = os.path.join(path_data,config.get('data paths', 'test_imgs_original'))
    test_masks_dir = os.path.join(path_data,config.get('data paths', 'test_groundTruth'))
    mean_img_path = os.path.join(path_data, config.get('data paths', 'mean_image'))
    train_log = os.path.join(path_data, config.get('data paths', 'train_log'))



    # #============ Load the data and divided in patches
    # patches_imgs_train, patches_masks_train = get_data_training_4classes(
    #     DRIVE_train_imgs_original = path_data + config.get('data paths', 'train_imgs_original'),
    #     DRIVE_train_groudTruth = path_data + config.get('data paths', 'train_groundTruth'),  #masks
    #     mean_image_path= path_data + config.get('data paths', 'mean_image'),
    #     patch_height = int(config.get('data attributes', 'patch_height')),
    #     patch_width = int(config.get('data attributes', 'patch_width')),
    #     N_subimgs = int(config.get('training settings', 'N_subimgs')),
    #     inside_FOV = config.getboolean('training settings', 'inside_FOV') #select the patches only inside the FOV  (default == True)
    # )
    # #patches_masks_train = masks_Unet_4classes(patches_masks_train)  # reduce memory consumption

    # #=========== Construct and save the model arcitecture =====
    # n_ch = patches_imgs_train.shape[1]
    # patch_height = patches_imgs_train.shape[2]
    # patch_width = patches_imgs_train.shape[3]

    n_ch = int(config.get('data attributes','num_channels'))
    patch_height = int(config.get('data attributes','patch_height'))
    patch_width = int(config.get('data attributes','patch_width'))
    img_dim = (patch_height,patch_width,n_ch)
    nClasses = int(config.get('data attributes','num_classes'))

    model = get_taunet_2classes(n_ch, patch_height, patch_width)  #the U-net model
    print "Check: final output of the network:"
    print model.output_shape
    json_string = model.to_json()

    model_file = os.path.join(path_project,name_experiment + '_architecture.json')
    best_weights_file = os.path.join(path_project,name_experiment + '_best_weights.h5')
    last_weights_files = os.path.join(path_project,name_experiment + '_last_weights.h5')

    open(model_file, 'w').write(json_string)

    checkpointer = ModelCheckpoint(filepath= best_weights_file, verbose=1, monitor='val_loss', mode='auto', save_best_only=True) #save at each epoch if the validation decreases
    tensorboard = TensorBoard(log_dir=train_log, histogram_freq=0, batch_size=32, write_graph=True, write_grads=False,
                                write_images=False, embeddings_freq=0, embeddings_layer_names=None,
                                embeddings_metadata=None)

    train_gen = TauImageGenerator('train_gen',train_imgs_dir,train_masks_dir,mean_img_path,img_dim,nClasses,batch_size,do_augmentation=True)
    test_gen = TauImageGenerator('test_gen',test_imgs_dir, test_masks_dir, mean_img_path, img_dim, nClasses, batch_size,do_augmentation=False)

    #model.fit(patches_imgs_train, patches_masks_train, nb_epoch=N_epochs, batch_size=batch_size, verbose=2, shuffle=True, validation_split=0.1, callbacks=[checkpointer,tensorboard])
    model.fit_generator(generator=train_gen.get_batch(),
                        validation_data=test_gen.get_batch(),
                        steps_per_epoch=train_gen.__len__(),
                        validation_steps=50,
                        epochs=1000,
                        verbose=1,
                        callbacks = [checkpointer, tensorboard])

    model.save_weights(last_weights_files, overwrite=True)



def main():
    if len(sys.argv) != 2:
        print('Usage: run_prediction <config_file.txt>')
        exit()

    config_path = str(sys.argv[1])
    run_training(config_path)


if __name__ == '__main__':
    main()













