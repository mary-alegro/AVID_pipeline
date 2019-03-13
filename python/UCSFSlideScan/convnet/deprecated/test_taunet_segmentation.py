###################################################
#
#   Script to
#   - Calculate prediction of the test dataset
#   - Calculate the parameters to evaluate the prediction
#
##################################################

#Python
import ConfigParser
#Keras
from keras.models import model_from_json
#scikit learn
import sys
#sys.path.insert(0, './util/')
# help_functions.py
from convnet.util.help_functions import *
# extract_patches.py
from convnet.util.extract_patches import recompone
from convnet.util.extract_patches import recompone_overlap
from convnet.util.extract_patches import get_data_testing
from convnet.util.extract_patches import get_data_testing_overlap,get_data_segmenting_overlap
# pre_processing.py
import os
import fnmatch
from misc.imoverlay import imoverlay as imoverlay
import mahotas as mh
import skimage.io as io
import glob


def run_segmentation(image_file,mean_img_path,out_name_seg,config_file):

    ### Read config
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    path_data = config.get('data paths', 'path_local')
    path_project = config.get('data paths', 'path_project')

    # dimension of the patches
    patch_height = int(config.get('data attributes', 'patch_height'))
    patch_width = int(config.get('data attributes', 'patch_width'))


    # model name
    name_experiment = config.get('experiment name', 'name')
    path_experiment = path_project + '/'
    Imgs_to_test = int(config.get('testing settings', 'full_images_to_test'))
    N_visual = int(config.get('testing settings', 'N_group_visual'))
    average_mode = config.getboolean('testing settings', 'average_mode')
    best_last = config.get('testing settings', 'best_last')

    # Load the saved model
    model = model_from_json(open(path_experiment + name_experiment + '_architecture.json').read())
    #model.load_weights(path_experiment + name_experiment + '_' + best_last + '_weights.h5')
    model.load_weights(path_project + name_experiment + '_best_weights.h5')

    stride_height = 20
    stride_width = 20
    new_height = None
    new_width = None

    orig_img = io.imread(image_file)

    if average_mode == True:
        patches_imgs_test, new_height, new_width, masks_test = get_data_segmenting_overlap(
                    #test_img_original=test_imgs_original,  # image path to segment
                    test_img_original=orig_img.astype('float'),  # image path to segment
                    Imgs_to_test=int(config.get('testing settings', 'full_images_to_test')),
                    mean_image_path=mean_img_path,
                    patch_height=patch_height,
                    patch_width=patch_width,
                    stride_height=stride_height,
                    stride_width=stride_width,
                    is_color=True
        )
    else:
        patches_imgs_test, patches_masks_test = get_data_testing(
                    test_imgs_original=orig_img,  # original
                    test_groudTruth=path_data + config.get('data paths', 'test_groundTruth'),  # masks
                    Imgs_to_test=int(config.get('testing settings', 'full_images_to_test')),
                    patch_height=patch_height,
                    patch_width=patch_width,
        )


            # ================ Run the prediction of the patches ==================================


            # Calculate the predictions
    predictions = model.predict(patches_imgs_test, batch_size=32, verbose=2)
    print "predicted images size :"
    print predictions.shape

            # ===== Convert the prediction arrays in corresponding images
    pred_patches,pred_patches2,pred_patches3 = pred_to_imgs_3classes(predictions, patch_height, patch_width, "original")
    if average_mode == True:
        pred_imgs = recompone_overlap(pred_patches, new_height, new_width, stride_height,stride_width)  # predictions
        pred_imgs2 = recompone_overlap(pred_patches2, new_height, new_width, stride_height, stride_width)  # predictions
        pred_imgs3 = recompone_overlap(pred_patches3, new_height, new_width, stride_height, stride_width)  # predictions
    else:
        pred_imgs = recompone(pred_patches, 13, 12)  # predictions

    img = pred_imgs[0,0,...]
    img = img.reshape([img.shape[0],img.shape[1]])

    if img.shape[0] > orig_img.shape[0]:
        img = img[0:orig_img.shape[0],...]
    if img.shape[1] > orig_img.shape[1]:
        img = img[:,0:orig_img.shape[1]]

    img = 1-img
    mask = img>=0.8
    #bw = mh.bwperim(mask)

    #mask out background just in case
    mask_bkg = orig_img[...,0] < 1.
    mask[mask_bkg == True] = False


    # print('Saving {}'.format(out_name))
    # io.imsave(out_name,overlay)

    print('Saving {}'.format(out_name_seg))
    io.imsave(out_name_seg,(mask*255).astype('uint8'))



def main():
    # if len(sys.argv) != 3:
    #     print('Usage: run_unet_seg <root_dir> <config_file.txt>')
    #     exit()
    #
    # root_dir = str(sys.argv[1])
    # config_path = str(sys.argv[2])

    img_file = '/home/maryana/storage2/Posdoc/AVID/AV13/crop_TAU_AT100#440.tif'
    mean_img = '/home/maryana/storage2/Posdoc/AVID/AV13/training/images/mean_image.npy'
    out_img = '/home/maryana/storage2/Posdoc/AVID/AV13/test_taunet.tif'
    config_path = '/home/maryana/storage2/Posdoc/AVID/AV13/configuration_avid_ucsf.txt'

    run_segmentation(img_file,mean_img,out_img,config_path)


if __name__ == '__main__':
    main()
