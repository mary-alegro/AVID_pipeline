import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided
import skimage.io as io
from skimage import img_as_ubyte
import os

def pixel_total(W,F,S):
    F = float(F)
    W = float(W)
    S = float(S)
    o = F-S
    f = F - o
    w = np.ceil(W/S)-1
    s = w*f
    T = F + s
    return T

def compute_padding(W,F,S):
    if S >= F:
        return -1
    T = pixel_total(W,F,S)
    pad = T-W
    return int(pad)

def compute_num_patches(W, S):
    return np.ceil(W/S)


def get_strided_view(arr,F,S):

    W = arr.shape[0] #I'm assuming all arrays are square

    pad = compute_padding(W,F,S)
    nPat = int(compute_num_patches(W, S))

    #pad_cols = np.zeros((int(arr.shape[0]+pad),int(pad)))
    #pad_rows = np.zeros((int(pad),int(arr.shape[1])))
    # arr1 = np.concatenate((arr,pad_rows),axis=0)
    # arr2 = np.concatenate((arr1,pad_cols),axis=1)

    pad_cols = arr[:,arr.shape[1]:arr.shape[1]-(pad+1):-1]
    arr1 = np.concatenate((arr,pad_cols),axis=1)

    pad_rows = arr1[arr1.shape[0]:arr1.shape[0]-(pad+1):-1,:]
    arr2 = np.concatenate((arr1,pad_rows),axis=0)

    arr_strided = as_strided(arr2, shape=(nPat,nPat, F, F), strides=(S*arr2.strides[0],S*arr2.strides[1],arr2.strides[0],arr2.strides[1]))

    return arr_strided

