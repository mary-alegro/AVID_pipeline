import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.io as io

from convnet.util.help_functions import *
from keras.models import model_from_json
from convnet.util.extract_patches import get_data_recon_overlap_1ch
from convnet.util.extract_patches import recompone_overlap


def load_hdf5(infile):
  with h5py.File(infile,"r") as f:  #"with" close the file after its nested commands
    return f["image"][()]


def run_reconstruction():

    train_imgs_original = '/home/maryana/storage/Spiralalgea/training/training_led.h5'
    train_groudTruth = '/home/maryana/storage/Spiralalgea/10x_manual/ground_truth_1ch/gd_1ch.h5'
    train_groudTruth_9ch = '/home/maryana/storage/Spiralalgea/10x_manual/test_9ch/test_9ch.h5'
    best_model_path = '/home/maryana/storage/Spiralalgea/best_weights.h5'
    last_model_path = '/home/maryana/storage/Spiralalgea/last_weights.h5'
    model_achitecture = '/home/maryana/storage/Spiralalgea/model_architecture.json'
    test_imgs_original = '/home/maryana/storage/Spiralalgea/testing/testing_led.h5'

    patch_height = 48
    patch_width = 48
    stride_height = 20
    stride_width = 20

    patches_imgs_test, new_height, new_width = get_data_recon_overlap_1ch(
        test_img_original=test_imgs_original,
        patch_height=patch_height,
        patch_width=patch_width,
        stride_height=stride_height,
        stride_width=stride_width
    )

    # Load the saved model
    model = model_from_json(open(model_achitecture).read())
    model.load_weights(best_model_path)

    # Calculate the predictions
    predictions = model.predict(patches_imgs_test, batch_size=32, verbose=2)

    pred_patches = np.empty((predictions.shape[0],1,patch_height,patch_width))
    for i in range(predictions.shape[0]):
        tmp = predictions[i,...]
        tmp = tmp.reshape((patch_height,patch_width))
        pred_patches[i,...] = tmp

    pred_img = recompone_overlap(pred_patches, new_height, new_width, stride_height,stride_width)
    img = np.squeeze(pred_img)
    img_gt = io.imread('/home/maryana/storage/Spiralalgea/10x_manual/test_1ch/test_z_stack.tif')
    gt_hf5 = load_hdf5('/home/maryana/storage/Spiralalgea/10x_manual/test_9ch/test_9ch.h5')


    fig = plt.figure()
    ax1 = fig.add_subplot(4, 3, 1)
    ax1.imshow(img,cmap='gray')
    ax2 = fig.add_subplot(4, 3, 2)
    ax2.imshow(img_gt,cmap='gray')

    for i in range(9):
        ax = fig.add_subplot(4, 3, i+3)
        ax.imshow(gt_hf5[...,i],cmap = 'gray')

    pass

    # fig = plt.figure()
    # ax1 = fig.add_subplot(2, 2, 1)
    # ax1.imshow(...)
    # ax2 = fig.add_subplot(2, 2, 2)
    # ax2.imshow(...)
    # ax3 = fig.add_subplot(2, 2, 3)
    # ax3.imshow(...)
    # ax4 = fig.add_subplot(2, 2, 4)
    # ax4.imshow(...)




def main():

    run_reconstruction()

if __name__ == '__main__':
    main()
