#Python
from keras.models import model_from_json
from convnet.util.help_functions import *
from convnet.util.extract_patches import get_data_testing_overlap,get_data_segmenting_overlap
import skimage.io as io
import matplotlib.pyplot as plt
import cv2
from keras import backend as K

from misc.TiffTileLoader import sub2ind,ind2sub

def grad_cam(input_model, input_data, cls, layer_name):
    """GradCAM method for visualizing input saliency."""
    y_c = input_model.output[0, cls, 0]
    conv_output = input_model.get_layer(layer_name).output
    grads = K.gradients(y_c, conv_output)[0]
    # Normalize if necessary
    # grads = normalize(grads)
    gradient_function = K.function([input_model.input], [conv_output, grads])

    output, grads_val = gradient_function([input_data])
    output, grads_val = output[0, :], grads_val[0, :, :, :]

    output = np.transpose(output,axes=(1,2,0))
    grads_val = np.transpose(grads_val,axes=(1,2,0))

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    # cam2 = np.zeros(cam.shape)
    # nW = weights.shape[0]
    # for i in range(nW):
    #     cam2 += weights[i] * output[:,:,i]


    # Process CAM
    #cam = cv2.resize(cam, (W, H), interpolation=cv2.INTER_LINEAR)
    cam = np.maximum(cam, 0)
    cam = cam / cam.max()
    return cam

test_file = 'test_tau.tif'
mean_img_path = '/home/maryana/storage2/Posdoc/AVID/AT100/slidenet_2classes/training/mean_image.npy'
orig_img = io.imread(test_file)
patches_imgs_test, new_height, new_width, masks_test = get_data_segmenting_overlap(
    test_img_original=orig_img.astype('float'),
    Imgs_to_test=0,
    mean_image_path= mean_img_path,
    patch_height=204,
    patch_width=204,
    stride_height=1,
    stride_width=1,
    is_color=True
)

# Load the saved model
model = model_from_json(open('/home/maryana/storage2/Posdoc/AVID/AT100/slidenet_2classes/models/AT100_slidenet_architecture.json').read())
model.load_weights('/home/maryana/storage2/Posdoc/AVID/AT100/slidenet_2classes/models/AT100_slidenet_best_weights.h5')

model.summary()

# Calculate the predictions
predictions = model.predict(patches_imgs_test, batch_size=1, verbose=2)
pred_patches = pred_to_imgs(predictions, 200, 200, "original")
pred_patches = pred_patches[0,0,...]

#idx_test = sub2ind([200,200],148,79)

mask = io.imread('test_tau_mask_v2.tif')
indices = np.nonzero(mask.flatten() > 0)
indices2 = np.nonzero(mask > 0)
nIdx = len(indices[0])
cams = np.zeros((200,200,nIdx))
for i in range(nIdx):
    idx_test = indices[0][i]
    cam = grad_cam(model,patches_imgs_test,idx_test,'concatenate_3')
    cams[:,:,i] = cam

final_cam = np.mean(cams,axis=(2))

plt.imshow(final_cam)
plt.show()

