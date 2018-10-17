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
        pred_images = pred[:,:,1]
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

