import sys
import skimage.io as io
from skimage import color
from skimage import filters as filt
from skimage import morphology as morph
import mahotas as mht
import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_ubyte


def seg_background(img,segname, outname):
    #IMG: RGB image
    #OUTNAME: mask file full path

    #create mask
    lab = color.rgb2lab(img)
    B = lab[...,2]
    B = np.fabs(B)
    level = filt.threshold_triangle(B)
    mask = B>level
    se = morph.disk(5)
    mask2 = mht.open(mask,se)
    se2 = morph.disk(3)
    mask3 = mht.erode(mask2,se2)
    mask4 = mask3*255
    io.imsave(outname,mask4.astype('ubyte'))

    #segment image
    gry = color.rgb2gray(img)
    gry = img_as_ubyte(gry)
    gry[mask3 == False] = 0
    io.imsave(segname,gry)

def main():

    if len(sys.argv) != 4:
        print('Usage: seg_background <rescaled histo> <seg_img> <mask>')
        print('Example: seg_background /AVID/AV13/AT100#440/res_10.tif /AVID/AV13/AT100#440/seg_res_10.tif /AVID/AV13/AT100#440/mask_res_10.tif')
        exit()

    imgname = str(sys.argv[1]) #abs path to where the images are
    segname = str(sys.argv[2])
    outname = str(sys.argv[3]) #row size

    #imgname = "/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/res_10.tif"
    #outname = "/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/mask_res_10.tif"
    img = io.imread(imgname)
    seg_background(img,segname,outname)
    print('Mask successfully saved.')


if __name__ == '__main__':
    main()



