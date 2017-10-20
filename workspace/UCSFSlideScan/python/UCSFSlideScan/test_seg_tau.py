import glob
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import skimage.io as io
from skimage import color
from skimage import exposure as exp
import mahotas
import os
from skimage import img_as_float, img_as_ubyte
from skimage import transform as xform

#matplotlib.use('TkAgg')


#img_path = "/home/maryana/storage/Posdoc/AVID/AV13/crop_TAU_AT100#440.tif"
img_path = "/Users/maryana/Posdoc/AVID/AV13/crop_TAU_AT100#440.tif"
img_path2 = "/Users/maryana/Posdoc/AVID/AV13/res_10.tif"
img = io.imread(img_path)
#R = img[...,0]
#G = img[...,1]
#B = img[...,2]

#gry = color.rgb2gray(img)
#p2, p98 = np.percentile(img, (2, 98))
#img2 = exp.rescale_intensity(img, in_range=(p2, p98))
#img2 = exp.equalize_adaphist(img, clip_limit=0.03, kernel_size=[50,50])
#img2 = exp.equalize_adapthist(img, clip_limit=0.03, kernel_size=[50,50])
#img2 = exp.equalize_adapthist(img)
#R = img2[...,1]
#mask = R<0.25

#pix_mm = 819 #1mm = 819pixels


lab = color.rgb2lab(img)
L = lab[...,0]
A = lab[...,1]
BB = lab[...,2]

#TAU
sL = np.concatenate((L[825:835,1315:1325].flatten(),L[595:605,1355:1365].flatten(),L[920:930,1385:1395].flatten()))
sA = np.concatenate((A[825:835,1315:1325].flatten(),A[595:605,1355:1365].flatten(),A[920:930,1385:1395].flatten()))
sB = np.concatenate((BB[825:835,1315:1325].flatten(),BB[595:605,1355:1365].flatten(),BB[920:930,1385:1395].flatten()))
mL = np.mean(sL)
mA = np.mean(sA)
mB = np.mean(sB)

img2 = io.imread(img_path2)
img2_shape = np.array([img2.shape[0],img2.shape[1]])
lab2 = color.rgb2lab(img2)
L2 = lab2[...,0]
A2 = lab2[...,1]
BB2 = lab2[...,2]
meanL = mL*np.ones(img2_shape)
meanA = mA*np.ones(img2_shape)
meanB = mB*np.ones(img2_shape)

# meanL = mL*np.ones(L.shape)
# meanA = mA*np.ones(A.shape)
# meanB = mB*np.ones(B.shape)



dL = L2 - meanL
dA = A2 - meanA
dB = BB2 - meanB
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
