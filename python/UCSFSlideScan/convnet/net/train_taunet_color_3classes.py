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

import sys
from convnet.util.help_functions import *

#function to obtain data for training/testing (validation)
from convnet.util.extract_patches import get_data_training_4classes

import tensorflow as tf
#sess = tf.Session()
sess = tf.Session(config=tf.ConfigProto(inter_op_parallelism_threads=int(os.environ['NUM_INTER_THREADS']),
                                        intra_op_parallelism_threads=int(os.environ['NUM_INTRA_THREADS'])))
K.set_session(sess)


#Define the neural network
def get_taunet(n_ch, patch_height, patch_width):
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
    conv6 = Conv2D(3, (1, 1), activation='relu',padding='same',data_format='channels_first')(conv5)
    conv6 = core.Reshape((3,patch_height*patch_width))(conv6)
    conv6 = core.Permute((2,1))(conv6)
    ############
    conv7 = core.Activation('softmax')(conv6)

    model = Model(input=inputs, output=conv7)

    #sgd = SGD(lr=0.01, decay=1e-5, momentum=0.3, nesterov=False)
    sgd = SGD(lr=0.01,decay=1e-5)
    #adam = Adam(lr=0.01)
    #model.compile(optimizer=SGD(lr=0.001), loss='categorical_crossentropy',metrics=['accuracy'])
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def run_training(conf_path):

    #========= Load settings from Config file
    config = ConfigParser.RawConfigParser()
    #config.read('../configuration_avid_ucsf.txt')
    config.read(conf_path)
    #patch to the datasets
    path_data = config.get('data paths', 'path_local')
    #Experiment name
    name_experiment = config.get('experiment name', 'name')
    #training settings
    N_epochs = int(config.get('training settings', 'N_epochs'))
    batch_size = int(config.get('training settings', 'batch_size'))
    path_data = config.get('data paths', 'path_local')
    path_project = config.get('data paths', 'path_project')


    #============ Load the data and divided in patches
    patches_imgs_train, patches_masks_train = get_data_training_4classes(
        DRIVE_train_imgs_original = path_data + config.get('data paths', 'train_imgs_original'),
        DRIVE_train_groudTruth = path_data + config.get('data paths', 'train_groundTruth'),  #masks
        mean_image_path= path_data + config.get('data paths', 'mean_image'),
        patch_height = int(config.get('data attributes', 'patch_height')),
        patch_width = int(config.get('data attributes', 'patch_width')),
        N_subimgs = int(config.get('training settings', 'N_subimgs')),
        inside_FOV = config.getboolean('training settings', 'inside_FOV') #select the patches only inside the FOV  (default == True)
    )
    #patches_masks_train = masks_Unet_4classes(patches_masks_train)  # reduce memory consumption


    #=========== Construct and save the model arcitecture =====
    n_ch = patches_imgs_train.shape[1]
    patch_height = patches_imgs_train.shape[2]
    patch_width = patches_imgs_train.shape[3]
    model = get_taunet(n_ch, patch_height, patch_width)  #the U-net model
    print "Check: final output of the network:"
    print model.output_shape
    #plot_model(model, to_file= path_project + '_model.png')   #check how the model looks like
    json_string = model.to_json()
    open(path_project + name_experiment + '_architecture.json', 'w').write(json_string)

    #============  Training ==================================
    checkpointer = ModelCheckpoint(filepath= path_project + name_experiment + '_best_weights.h5', verbose=1, monitor='val_loss', mode='auto', save_best_only=True) #save at each epoch if the validation decreases
    tensorboard = TensorBoard(log_dir='/home/maryana/storage2/Posdoc/AVID/AV13/training/logs', histogram_freq=0, batch_size=32, write_graph=True, write_grads=False,
                                write_images=False, embeddings_freq=0, embeddings_layer_names=None,
                                embeddings_metadata=None)

    model.fit(patches_imgs_train, patches_masks_train, nb_epoch=N_epochs, batch_size=batch_size, verbose=2, shuffle=True, validation_split=0.1, callbacks=[checkpointer,tensorboard])

    #========== Save and test the last model ===================
    model.save_weights(path_project + name_experiment + 'AVID_last_weights.h5', overwrite=True)
    #test the model
    # score = model.evaluate(patches_imgs_test, masks_Unet(patches_masks_test), verbose=0)
    # print('Test score:', score[0])
    # print('Test accuracy:', score[1])


def main():
    if len(sys.argv) != 2:
        print('Usage: run_prediction <config_file.txt>')
        exit()

    config_path = str(sys.argv[1])
    run_training(config_path)


if __name__ == '__main__':
    main()













