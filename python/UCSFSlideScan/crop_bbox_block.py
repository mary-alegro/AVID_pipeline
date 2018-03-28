import numpy as np
import matplotlib.pyplot as plt
import skimage.measure as meas
import glob
import skimage.io as io
import os


img_dir = '/home/maryana/storage/Posdoc/AVID/AV23/blockface/aligned/'
out_dir = '/home/maryana/storage/Posdoc/AVID/AV23/blockface/aligned2/'

min_row = 3000
min_col = 3000
max_row = 0
max_col = 0

files = glob.glob(img_dir+'*.png')
for fi in files:
    img = io.imread(fi)
    img_bin = np.zeros(img.shape)
    img_bin[img > 0] = True

    labels = meas.label(img_bin)
    props = meas.regionprops(labels)
    bbox = props[0].bbox

    if bbox[0] < min_row:
        min_row = int(bbox[0])
    if bbox[1] < min_col:
        min_col = int(bbox[1])

    if bbox[2] > max_row:
        max_row = int(bbox[2])
    if bbox[3] > max_col:
        max_col = int(bbox[3])


for fi in files:
    img = io.imread(fi)
    base_name = os.path.basename(fi)
    out_name = out_dir + base_name
    img2 = img[min_row:max_row,min_col:max_col]
    io.imsave(out_name,img2)