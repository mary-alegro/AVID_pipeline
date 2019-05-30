import h5py
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt





def load_hdf5(infile):
  with h5py.File(infile,"r") as f:  #"with" close the file after its nested commands
    return f["image"][()]

def write_hdf5(arr,outfile):
  with h5py.File(outfile,"w") as f:
    f.create_dataset("image", data=arr, dtype=arr.dtype)

#convert RGB image in black and white
def rgb2gray(rgb):
    assert (len(rgb.shape)==4)  #4D arrays
    assert (rgb.shape[1]==3)
    bn_imgs = rgb[:,0,:,:]*0.299 + rgb[:,1,:,:]*0.587 + rgb[:,2,:,:]*0.114
    bn_imgs = np.reshape(bn_imgs,(rgb.shape[0],1,rgb.shape[2],rgb.shape[3]))
    return bn_imgs

#group a set of images row per columns
def group_images(data,per_row):
    assert data.shape[0]%per_row==0
    assert (data.shape[1]==1 or data.shape[1]==3)
    data = np.transpose(data,(0,2,3,1))  #corect format for imshow
    all_stripe = []
    for i in range(int(data.shape[0]/per_row)):
        stripe = data[i*per_row]
        for k in range(i*per_row+1, i*per_row+per_row):
            stripe = np.concatenate((stripe,data[k]),axis=1)
        all_stripe.append(stripe)
    totimg = all_stripe[0]
    for i in range(1,len(all_stripe)):
        totimg = np.concatenate((totimg,all_stripe[i]),axis=0)
    return totimg


#visualize image (as PIL image, NOT as matplotlib!)
def visualize(data,filename):
    assert (len(data.shape)==3) #height*width*channels
    img = None
    if data.shape[2]==1:  #in case it is black and white
        data = np.reshape(data,(data.shape[0],data.shape[1]))
    if np.max(data)>1:
        img = Image.fromarray(data.astype(np.uint8))   #the image is already 0-255
    else:
        img = Image.fromarray((data*255).astype(np.uint8))  #the image is between 0-1
    img.save(filename + '.png')
    return img


#prepare the mask in the right shape for the Unet
def masks_Unet(masks):
    assert (len(masks.shape)==4)  #4D arrays
    assert (masks.shape[1]==1 )  #check the channel is 1
    im_h = masks.shape[2]
    im_w = masks.shape[3]
    masks = np.reshape(masks,(masks.shape[0],im_h*im_w))
    new_masks = np.empty((masks.shape[0],im_h*im_w,2))
    for i in range(masks.shape[0]):
        for j in range(im_h*im_w):
            if  masks[i,j] == 0:
                new_masks[i,j,0]=1
                new_masks[i,j,1]=0
            else:
                new_masks[i,j,0]=0
                new_masks[i,j,1]=1
    return new_masks

def masks_Unet_4classes(masks_orig):
    # masks_orig = [sBatch,4,rows,cols]
    # masks_cnn = [sBatch,rows*cols,4]
    sBatch = masks_orig.shape[0]
    m_rows = masks_orig.shape[2]
    m_cols = masks_orig.shape[3]
    masks_cnn = np.empty((sBatch,m_rows*m_cols,4))
    for i in range(sBatch):
        for c in range(4): # 4 classes
            tmp1 = masks_orig[i,c,...]
            tmp1 = np.reshape(tmp1,(m_rows*m_cols))
            masks_cnn[i,:,c] = tmp1

    return masks_cnn



def pred_to_imgs(pred, patch_height, patch_width, mode="original"):
    #assert (len(pred.shape)==3)  #3D array: (Npatches,height*width,2)
    #assert (pred.shape[2]==2 )  #check the classes are 2
    pred_images = np.empty((pred.shape[0],pred.shape[1]))  #(Npatches,height*width)
    if mode=="original":
        # for i in range(pred.shape[0]):
        #     for pix in range(pred.shape[1]):
        #         pred_images[i,pix]=pred[i,pix,1]
        pred_images = pred[:,:,0]
    elif mode=="threshold":
        for i in range(pred.shape[0]):
            for pix in range(pred.shape[1]):
                if pred[i,pix,1]>=0.5:
                    pred_images[i,pix]=1
                else:
                    pred_images[i,pix]=0
    else:
        print "mode " +str(mode) +" not recognized, it can be 'original' or 'threshold'"
        exit()
    pred_images = np.reshape(pred_images,(pred_images.shape[0],1, patch_height, patch_width))
    return pred_images

def pred_to_imgs_3classes(pred, patch_height, patch_width, mode="original"):
    pred_images_c1 = np.empty((pred.shape[0],pred.shape[1]))  #(Npatches,height*width)
    pred_images_c2 = np.empty((pred.shape[0], pred.shape[1]))  # (Npatches,height*width)
    pred_images_c3 = np.empty((pred.shape[0], pred.shape[1]))  # (Npatches,height*width)
    if mode=="original":
        pred_images_c1 = pred[:,:,0]
        pred_images_c2 = pred[:, :, 1]
        pred_images_c3 = pred[:, :, 2]
    elif mode=="threshold":
        # for i in range(pred.shape[0]):
        #     for pix in range(pred.shape[1]):
        #         if pred[i,pix,1]>=0.5:
        #             pred_images[i,pix]=1
        #         else:
        #             pred_images[i,pix]=0
        pass
    else:
        print "mode " +str(mode) +" not recognized, it can be 'original' or 'threshold'"
        exit()
    pred_images_c1 = np.reshape(pred_images_c1,(pred_images_c1.shape[0],1, patch_height, patch_width))
    pred_images_c2 = np.reshape(pred_images_c2, (pred_images_c2.shape[0], 1, patch_height, patch_width))
    pred_images_c3 = np.reshape(pred_images_c3, (pred_images_c3.shape[0], 1, patch_height, patch_width))
    return pred_images_c1,pred_images_c2,pred_images_c3


def pad_image(img,pad_r,pad_c):
    #rows
    top_pad = img[0:pad_r,...]
    top_pad = top_pad[::-1,...]
    botton_pad = img[img.shape[0]:img.shape[0]-(pad_r+1):-1,...]
    img2 = np.concatenate((top_pad,img,botton_pad),axis=0)
    #cols
    left_pad = img2[:,0:pad_c,:]
    left_pad = left_pad[:,::-1,:]
    right_pad = img2[:,img2.shape[1]:img2.shape[1]-(pad_c+1):-1,:]
    img3 = np.concatenate((left_pad,img2,right_pad),axis=1)

    return img3


# from http://jamesgregson.ca/extract-image-patches-in-python.html

def extract_grayscale_patches( img, shape, offset=(0,0), stride=(1,1) ):
    """Extracts (typically) overlapping regular patches from a grayscale image

    Changing the offset and stride parameters will result in images
    reconstructed by reconstruct_from_grayscale_patches having different
    dimensions! Callers should pad and unpad as necessary!

    Args:
        img (HxW ndarray): input image from which to extract patches

        shape (2-element arraylike): shape of that patches as (h,w)

        offset (2-element arraylike): offset of the initial point as (y,x)

        stride (2-element arraylike): vertical and horizontal strides

    Returns:
        patches (ndarray): output image patches as (N,shape[0],shape[1]) array

        origin (2-tuple): array of top and array of left coordinates
    """
    px, py = np.meshgrid( np.arange(shape[1]),np.arange(shape[0]))
    l, t = np.meshgrid(
        np.arange(offset[1],img.shape[1]-shape[1]+1,stride[1]),
        np.arange(offset[0],img.shape[0]-shape[0]+1,stride[0]) )
    l = l.ravel()
    t = t.ravel()
    x = np.tile( px[None,:,:], (t.size,1,1)) + np.tile( l[:,None,None], (1,shape[0],shape[1]))
    y = np.tile( py[None,:,:], (t.size,1,1)) + np.tile( t[:,None,None], (1,shape[0],shape[1]))
    return img[y.ravel(),x.ravel()].reshape((t.size,shape[0],shape[1])), (t,l)

def reconstruct_from_grayscale_patches( patches, origin, epsilon=1e-12 ):
    """Rebuild an image from a set of patches by averaging

    The reconstructed image will have different dimensions than the
    original image if the strides and offsets of the patches were changed
    from the defaults!

    Args:
        patches (ndarray): input patches as (N,patch_height,patch_width) array

        origin (2-tuple): top and left coordinates of each patch

        epsilon (scalar): regularization term for averaging when patches
            some image pixels are not covered by any patch

    Returns:
        image (ndarray): output image reconstructed from patches of
            size ( max(origin[0])+patches.shape[1], max(origin[1])+patches.shape[2])

        weight (ndarray): output weight matrix consisting of the count
            of patches covering each pixel
    """
    patch_width  = patches.shape[2]
    patch_height = patches.shape[1]
    img_width    = np.max( origin[1] ) + patch_width
    img_height   = np.max( origin[0] ) + patch_height

    out = np.zeros( (img_height,img_width) )
    wgt = np.zeros( (img_height,img_width) )
    for i in range(patch_height):
        for j in range(patch_width):
            out[origin[0]+i,origin[1]+j] += patches[:,i,j]
            wgt[origin[0]+i,origin[1]+j] += 1.0

    return out/np.maximum( wgt, epsilon ), wgt

