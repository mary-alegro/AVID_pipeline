import glob
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import skimage.io as io
from skimage import color
import skimage.exposure as exp
import mahotas
import os
from skimage import img_as_float, img_as_ubyte
from skimage import transform as xform

#matplotlib.use('TkAgg')


#img_path = "/home/maryana/storage/Posdoc/AVID/AV13/crop_TAU_AT100#440.tif"
img_path = "/home/maryana/storage/Posdoc/AVID/AV13/AT100#440/tiles_seg/AT100#440_67.tif"
#img_path2 = "/Users/maryana/Posdoc/AVID/AV13/res_10.tif"
img = io.imread(img_path)
#R = img[...,0]
#G = img[...,1]
#B = img[...,2]

#gry = color.rgb2gray(img)
#p2, p98 = np.percentile(img, (2, 98))
#img2 = exp.rescale_intensity(img, in_range=(p2, p98))
img2 = exp.equalize_adapthist(img, clip_limit=0.03, kernel_size=[50,50])
#img2 = exp.equalize_adapthist(img)
#R = img2[...,1]
#mask = R<0.25

#pix_mm = 819 #1mm = 819pixels

lab = color.rgb2lab(img2)
L = lab[...,0]
A = lab[...,1]
BB = lab[...,2]

#TAU
#sL = np.concatenate((L[825:835,1315:1325].flatten(),L[595:605,1355:1365].flatten(),L[920:930,1385:1395].flatten()))
#sA = np.concatenate((A[825:835,1315:1325].flatten(),A[595:605,1355:1365].flatten(),A[920:930,1385:1395].flatten()))
#sB = np.concatenate((BB[825:835,1315:1325].flatten(),BB[595:605,1355:1365].flatten(),BB[920:930,1385:1395].flatten()))
sL = np.concatenate((L[2046:2056,2494:2504].flatten(),L[1930:1940,2747:2757].flatten(),L[2214:2224,2872:2882].flatten()))
sA = np.concatenate((A[2046:2056,2494:2504].flatten(),A[1930:1940,2747:2757].flatten(),A[2214:2224,2872:2882].flatten()))
sB = np.concatenate((BB[2046:2056,2494:2504].flatten(),BB[1930:1940,2747:2757].flatten(),BB[2214:2224,2872:2882].flatten()))
mL = np.mean(sL)
mA = np.mean(sA)
mB = np.mean(sB)

img_shape = np.array([img.shape[0],img.shape[1]])
meanL = mL*np.ones(img_shape)
meanA = mA*np.ones(img_shape)
meanB = mB*np.ones(img_shape)

# meanL = mL*np.ones(L.shape)
# meanA = mA*np.ones(A.shape)
# meanB = mB*np.ones(B.shape)

dL = L - meanL
dA = A - meanA
dB = BB - meanB
dEf = np.sqrt(dL**2 + dA**2 + dB**2)
dEf = (dEf - dEf.min())/(dEf.max() - dEf.min())
plt.imshow(dEf)
#
# #BG
# sL = np.concatenate((L[210:220,2460:2470].flatten(),L[1395:1405,2330:2340].flatten(),L[155:165,270:280].flatten()))
# sA = np.concatenate((A[210:220,2460:2470].flatten(),A[1395:1405,2330:2340].flatten(),A[155:165,270:280].flatten()))
# sB = np.concatenate((BB[210:220,2460:2470].flatten(),BB[1395:1405,2330:2340].flatten(),BB[155:165,270:280].flatten()))
# mL = np.mean(sL)
# mA = np.mean(sA)
# mB = np.mean(sB)
# meanL = mL*np.ones(L.shape)
# meanA = mA*np.ones(A.shape)
# meanB = mB*np.ones(B.shape)
# dL = L - meanL
# dA = A - meanA
# dB = B - meanB
# dEb = np.sqrt(dL**2 + dA**2 + dB**2)
# dEb = (dEb - dEb.min())/(dEb.max() - dEb.min())
# plt.imshow(dEb)
#
pass

# from skimage import filters as filt
# map1 = dEf*255
# map1.max()
# Out[4]:
# 255.0
# map2 = np.round(map1)
# map2
# Out[6]:
# array([[ 128.,  128.,  128., ...,  144.,  149.,  143.],
#        [ 128.,  128.,  128., ...,  139.,  144.,  144.],
#        [ 128.,  128.,  128., ...,  135.,  135.,  140.],
#        ...,
#        [ 167.,  170.,  166., ...,  135.,  135.,  135.],
#        [ 171.,  171.,  169., ...,  135.,  135.,  135.],
#        [ 168.,  173.,  169., ...,  135.,  135.,  135.]])
# map3 = map2.astype('ubyte')
# map3
# Out[8]:
# array([[128, 128, 128, ..., 144, 149, 143],
#        [128, 128, 128, ..., 139, 144, 144],
#        [128, 128, 128, ..., 135, 135, 140],
#        ...,
#        [167, 170, 166, ..., 135, 135, 135],
#        [171, 171, 169, ..., 135, 135, 135],
#        [168, 173, 169, ..., 135, 135, 135]], dtype=uint8)
# plt.imshow(nmap3)
# Traceback (most recent call last):
#   File "/home/maryana/.local/lib/python2.7/site-packages/IPython/core/interactiveshell.py", line 2881, in run_code
#     exec(code_obj, self.user_global_ns, self.user_ns)
#   File "<ipython-input-9-2efe36013d11>", line 1, in <module>
#     plt.imshow(nmap3)
# NameError: name 'nmap3' is not defined
# plt.imshow(map3)
# Out[10]:
# <matplotlib.image.AxesImage at 0x7faad9bfbc10>
# mapf = filt.median(map3)
# plt.imshow(mapf)
# Out[12]:
# <matplotlib.image.AxesImage at 0x7faa6ce21050>
# from skimage import morphology as morph
# se = morph.disk(2)
# se
# Out[15]:
# array([[0, 0, 1, 0, 0],
#        [0, 1, 1, 1, 0],
#        [1, 1, 1, 1, 1],
#        [0, 1, 1, 1, 0],
#        [0, 0, 1, 0, 0]], dtype=uint8)
# mapf = mahotas.open(map3,se)
# plt.imshow(mapf)
# Out[17]:
# <matplotlib.image.AxesImage at 0x7faa6c48e4d0>
# mapf2 = mahotas.close(mapf,se)
# plt.imshow(mapf2)
# Out[19]:
# <matplotlib.image.AxesImage at 0x7faa6c411f10>
# se2 = morph.disk(5)
# mapf3 = mahotas.open(mapf2,se2)
# plt.imshow(mapf3)
# Out[22]:
# <matplotlib.image.AxesImage at 0x7faa6c3aac90>
# mapf4 = mahotas.close(mapf3,se2)
# plt.imshow(mapf4)
# Out[24]:
# <matplotlib.image.AxesImage at 0x7faadefcc7d0>
# plt.imshow(mapf2)
# Out[25]:
# <matplotlib.image.AxesImage at 0x7faa801ce4d0>
# mapmd = filt.median(mapf2)
# plt.imshow(mapmd)
# Out[27]:
# <matplotlib.image.AxesImage at 0x7faa80160610>
# plt.imshow(mapmd)
# Out[28]:
# <matplotlib.image.AxesImage at 0x7faa800c7cd0>
# mask = mapmd<70
# plt.imshow(mask)
# Out[30]:
# <matplotlib.image.AxesImage at 0x7faa800051d0>
# from imoverlay import imoverlay
# overlay = imoverlay(img,mapmd)
# plt.imshow(overlay)
# Out[33]:
# <matplotlib.image.AxesImage at 0x7faa7ab47210>
# overlay = imoverlay(img,mapmd,[0.1,1,0.1])
# plt.imshow(overlay)
# Out[35]:
# <matplotlib.image.AxesImage at 0x7faa7ff8c650>
# mapmd
# Out[36]:
# array([[128, 128, 128, ..., 140, 140, 140],
#        [128, 128, 128, ..., 140, 140, 140],
#        [128, 128, 128, ..., 140, 140, 140],
#        ...,
#        [167, 167, 165, ..., 135, 135, 135],
#        [167, 167, 167, ..., 135, 135, 135],
#        [167, 167, 167, ..., 135, 135, 135]], dtype=uint8)
# overlay = imoverlay(img,mask,[0.1,1,0.1])
# plt.imshow(overlay)
# Out[38]:
# <matplotlib.image.AxesImage at 0x7faa7feffdd0>
# mask = mapmd<60
# plt.imshow(mask)
#
