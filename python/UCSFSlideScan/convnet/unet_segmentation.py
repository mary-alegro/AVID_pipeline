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


TISSUE_THRESH = 0.05

def get_num_pix_tissue(img):  # assumes RGB image
    tmp_img = img[:, :, 0] + img[:, :, 1] + img[:, :, 2]
    tmp_nnz_b = tmp_img.flatten().nonzero()
    nnz_b = float(len(tmp_nnz_b[0]))  # number of non-zero pixel in img
    return nnz_b



def get_folder_list(root_dir):
    folder_list = []

    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root, '*heat_map'):
            folder_list.append(root)

    return folder_list



# def run_prediction(config_file):
#
#     # ========= CONFIG FILE TO READ FROM =======
#     config = ConfigParser.RawConfigParser()
#     #config.read('../configuration_avid_ucsf.txt')
#     # run the training on invariant or local
#     config.read(config_file)
#     path_data = config.get('data paths', 'path_local')
#     path_project = config.get('data paths', 'path_project')
#
#     # original test images (for FOV selection)
#     test_imgs_original = path_data + config.get('data paths', 'test_imgs_original')
#     test_imgs_orig = load_hdf5(test_imgs_original)
#     full_img_height = test_imgs_orig.shape[2]
#     full_img_width = test_imgs_orig.shape[3]
#
#     # dimension of the patches
#     patch_height = int(config.get('data attributes', 'patch_height'))
#     patch_width = int(config.get('data attributes', 'patch_width'))
#     # the stride in case output with average
#     stride_height = int(config.get('testing settings', 'stride_height'))
#     stride_width = int(config.get('testing settings', 'stride_width'))
#     assert (stride_height < patch_height and stride_width < patch_width)
#
#     # model name
#     name_experiment = config.get('experiment name', 'name')
#     path_experiment = path_project + name_experiment + '/'
#     # N full images to be predicted
#     Imgs_to_test = int(config.get('testing settings', 'full_images_to_test'))
#     # Grouping of the predicted images
#     N_visual = int(config.get('testing settings', 'N_group_visual'))
#     # ====== average mode ===========
#     average_mode = config.getboolean('testing settings', 'average_mode')
#
#
#
#     # ============ Load the data and divide in patches
#     patches_imgs_test = None
#     new_height = None
#     new_width = None
#     masks_test = None
#     patches_masks_test = None
#     if average_mode == True:
#         patches_imgs_test, new_height, new_width, masks_test = get_data_testing_overlap(
#             test_imgs_original=test_imgs_original,  # original
#             test_groudTruth=path_data + config.get('data paths', 'test_groundTruth'),  # masks
#             Imgs_to_test=int(config.get('testing settings', 'full_images_to_test')),
#             mean_image_path=path_data + config.get('data paths', 'mean_image'),
#             patch_height=patch_height,
#             patch_width=patch_width,
#             stride_height=stride_height,
#             stride_width=stride_width,
#             is_color=True
#         )
#     else:
#         patches_imgs_test, patches_masks_test = get_data_testing(
#             test_imgs_original=test_imgs_original,  # original
#             test_groudTruth=path_data + config.get('data paths', 'test_groundTruth'),  # masks
#             Imgs_to_test=int(config.get('testing settings', 'full_images_to_test')),
#             patch_height=patch_height,
#             patch_width=patch_width,
#         )
#
#     # ================ Run the prediction of the patches ==================================
#     best_last = config.get('testing settings', 'best_last')
#     # Load the saved model
#     model = model_from_json(open(path_experiment + name_experiment + '_architecture.json').read())
#     model.load_weights(path_experiment + name_experiment + '_' + best_last + '_weights.h5')
#     # Calculate the predictions
#     predictions = model.predict(patches_imgs_test, batch_size=32, verbose=2)
#     print "predicted images size :"
#     print predictions.shape
#
#     # ===== Convert the prediction arrays in corresponding images
#     pred_patches = pred_to_imgs(predictions, patch_height, patch_width, "original")



def run_segmentation(root_dir,config_file):

    dir_list = get_folder_list(root_dir)

    ### Read config

    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    path_data = config.get('data paths', 'path_local')
    path_project = config.get('data paths', 'path_project')

    # original test images (for FOV selection)
    #test_imgs_original = path_data + config.get('data paths', 'test_imgs_original')
    #test_imgs_orig = load_hdf5(test_imgs_original)
    #full_img_height = test_imgs_orig.shape[2]
    #full_img_width = test_imgs_orig.shape[3]

    # dimension of the patches
    patch_height = int(config.get('data attributes', 'patch_height'))
    patch_width = int(config.get('data attributes', 'patch_width'))
    # the stride in case output with average
    #stride_height = int(config.get('testing settings', 'stride_height'))
    #stride_width = int(config.get('testing settings', 'stride_width'))

    # model name
    name_experiment = config.get('experiment name', 'name')
    path_experiment = path_project + '/'
    Imgs_to_test = int(config.get('testing settings', 'full_images_to_test'))
    N_visual = int(config.get('testing settings', 'N_group_visual'))
    average_mode = config.getboolean('testing settings', 'average_mode')
    best_last = config.get('testing settings', 'best_last')

    ### Load model

    #get median values - used in preprocessing


    # Load the saved model
    model = model_from_json(open(path_experiment + name_experiment + '_architecture.json').read())
    #model.load_weights(path_experiment + name_experiment + '_' + best_last + '_weights.h5')
    model.load_weights(path_project + name_experiment + '_best_weights.h5')

    #stride_height = 35
    #stride_width = 35
    stride_height = 20
    stride_width = 20

    #for root, dir, files in os.walk(img_dir):
    for folder in dir_list:

        #check if tiles folder exists
        tiles_dir = os.path.join(folder,'seg_tiles')
        if not os.path.exists(tiles_dir):
            print('Error: tiles folder {} does not exist.'.format(tiles_dir))
            continue

        #create output folder
        out_dir = os.path.join(folder,'TAU_seg_tiles')
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        print('*** Processing files in folder {}'.format(folder))

        #get a list of tif files
        files = glob.glob(os.path.join(tiles_dir,'*.tif'))
        nTotal = len(files)
        print('{} tile(s) to segment.'.format(nTotal))

        for fname in files:

            basename = os.path.basename(fname)
            #overlay = imoverlay(orig_img,bw,[0.3,1,0.3])
            #out_name = os.path.join(out_dir,basename[0:-4]+'_over.tif')
            out_name_seg = os.path.join(out_dir,basename[0:-4]+'_mask.tif')

            test_imgs_original = os.path.join(tiles_dir,fname)
            print('Segmenting image {}.'.format(test_imgs_original))

            # ============ Load the data and divide in patches
            patches_imgs_test = None
            new_height = None
            new_width = None
            masks_test = None
            patches_masks_test = None

            #load image to segment
            #orig_img = load_hdf5(test_imgs_original)
            orig_img = io.imread(test_imgs_original)

            #check if image has enough tissue
            npix_tissue = get_num_pix_tissue(orig_img)
            percent_tissue = npix_tissue / (orig_img.shape[0] * orig_img.shape[1])
            if percent_tissue < TISSUE_THRESH:
                print('Image has too little tissue. Skipping.')
                continue


            mean_img_path = os.path.join(tiles_dir,'mean_image.npy')
            if not os.path.exists(mean_img_path):
                mean_img_path = path_data + config.get('data paths', 'mean_image')


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
                    test_imgs_original=test_imgs_original,  # original
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
            pred_patches = pred_to_imgs(predictions, patch_height, patch_width, "original")
            if average_mode == True:
                pred_imgs = recompone_overlap(pred_patches, new_height, new_width, stride_height,
                                              stride_width)  # predictions
            else:
                pred_imgs = recompone(pred_patches, 13, 12)  # predictions

            img = pred_imgs[0,0,...]
            img = img.reshape([img.shape[0],img.shape[1]])

            if img.shape[0] > orig_img.shape[0]:
                img = img[0:orig_img.shape[0],...]
            if img.shape[1] > orig_img.shape[1]:
                img = img[:,0:orig_img.shape[1]]

            img = 1-img
            mask = img>=0.5
            #bw = mh.bwperim(mask)

            #mask out background just in case
            mask_bkg = orig_img[...,0] < 1.
            mask[mask_bkg == True] = False


            # print('Saving {}'.format(out_name))
            # io.imsave(out_name,overlay)

            print('Saving {}'.format(out_name_seg))
            io.imsave(out_name_seg,(mask*255).astype('uint8'))



def main():
    if len(sys.argv) != 3:
        print('Usage: run_unet_seg <root_dir> <config_file.txt>')
        exit()

    root_dir = str(sys.argv[1])
    config_path = str(sys.argv[2])

    #img_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100#440/hdf5_tiles/'
    #out_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100#440/TAU_seg_tiles'
    #config_path = '/home/maryana/Projects/retina-unet/configuration_avid_ucsf.txt'

    run_segmentation(root_dir,config_path)


if __name__ == '__main__':
    main()
