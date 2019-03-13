import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="0"

#Python
import ConfigParser
from keras.models import model_from_json
import sys
from convnet.util.help_functions import *
from convnet.util.extract_patches import recompone
from convnet.util.extract_patches import recompone_overlap
from convnet.util.extract_patches import get_data_testing
from convnet.util.extract_patches import get_data_testing_overlap,get_data_segmenting_overlap

import fnmatch
from misc.imoverlay import imoverlay as imoverlay
import mahotas as mh
import skimage.io as io
import glob
import matplotlib.pyplot as plt
import cv2

from convnet.util.pre_processing import preproc_color, load_mean_values
from convnet.util.help_functions import pred_to_imgs

def run_slidenet_pred(config_file,img2seg,pred_dir):
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    # path_data = config.get('data paths', 'path_local')
    path_project = config.get('data paths', 'path_project')
    path_model = os.path.join(path_project, config.get('data paths', 'path_model'))

    # dimension of the patches
    patch_height = int(config.get('data attributes', 'patch_height'))
    patch_width = int(config.get('data attributes', 'patch_width'))

    patch_height = 204
    patch_width = 204
    mask_dim = (200, 200)

    # model name
    name_experiment = config.get('experiment name', 'name')
    Imgs_to_test = int(config.get('testing settings', 'full_images_to_test'))
    N_visual = int(config.get('testing settings', 'N_group_visual'))
    average_mode = config.getboolean('testing settings', 'average_mode')
    best_last = config.get('testing settings', 'best_last')

    mean_img_path = os.path.join(path_project, config.get('data paths', 'mean_image'))
    mu = load_mean_values(mean_img_path)

    orig_img = io.imread(img2seg)
    test_img = subtract_mean(orig_img.copy(),mu)
    test_img /= 255.
    print('{} | {}'.format(test_img.min(), test_img.max()))

    test_img = np.reshape(test_img,(1,test_img.shape[0],test_img.shape[1],test_img.shape[2]))
    test_img = np.transpose(test_img,axes=(0,3,1,2))

    # Load the saved model
    model = model_from_json(open(os.path.join(path_model, name_experiment + '_architecture.json')).read())
    model.load_weights(os.path.join(path_model, name_experiment + '_best_weights.h5'))

    predictions = model.predict(test_img, batch_size=1, verbose=2)
    pred = np.reshape(predictions,(1,200,200,2))
    plt.imshow(pred[0,:,:,0])
    pred0 = pred[0,:,:,0]

    basename = os.path.basename(img2seg)
    pred_name = os.path.join(pred_dir,basename+'_pred.npy')
    np.save(pred_name,pred0)



    # mask = pred0 > 0.7
    # mask2 = cv2.resize(mask*255,(204,204),interpolation=cv2.INTER_NEAREST)
    # perim = mh.bwperim(mask2)
    # over = imoverlay(orig_img,perim,[0.1,1,0.1])
    # plt.imshow(over)
    #
    # print "predicted images size :"
    # print predictions.shape


def subtract_mean(data,mu):
    # mu = mu.reshape([1,3,1,1]) #reshape mu array to fit the dataset and allow substraction
    # imgs = imgs-mu

    muR = mu[0]
    muG = mu[1]
    muB = mu[2]

    R = data[...,0]
    G = data[...,1]
    B = data[...,2]

    R = R - muR
    G = G - muG
    B = B - muB

    new_img = np.concatenate((R[...,np.newaxis],G[...,np.newaxis],B[...,np.newaxis]),axis=2)

    return new_img


def list_files(imgs_dir):
    l = glob.glob(os.path.join(imgs_dir,'*.tif'))
    return l



def main():
    if len(sys.argv) != 3:
        print('Usage: slidenet_segmentation_2classes [<image to segment> | <dir with image set>], <config_file.txt>')
        exit()

    img2seg = str(sys.argv[1])
    config_path = str(sys.argv[2])
    pred_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/slidenet_2classes/training/images204'

    if os.path.isfile(img2seg):
        run_slidenet_pred(config_path,img2seg)
    else:
        files = list_files(img2seg)
        for f in files:
            run_slidenet_pred(config_path,f,pred_dir)



if __name__ == '__main__':
    main()