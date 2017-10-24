import glob
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import skimage.io as io
from skimage import color
from skimage imt exposure as exp
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
