import sys
import skimage.io as io
from skimage import color
from skimage import filters as filt
from skimage import morphology as morph
import mahotas




def seg_background(img,outname):
    #IMG: RGB image
    #OUTNAME: mask file full path

    lab = color.rgb2lab(img)
    B = lab[...,2]
    level = filt.threshold_triangle(B)
    mask = B>level
    se = morph.disk(5)
    mask2 = mahotas.open(mask,se)
    mask3 = mask2*255
    io.imsave(outname,mask3.astype('ubyte'))

def main():

    if len(sys.argv) != 3:
        print('Usage: seg_background <rescaled histo> <mask>')
        print('Example: seg_background /AVID/AV13/AT100#440/res_10.tif /AVID/AV13/AT100#440/mask_res_10.tif')
        exit()

    imgname = str(sys.argv[1]) #abs path to where the images are
    outname = str(sys.argv[2]) #row size

    #imgname = "/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/res_10.tif"
    #outname = "/Volumes/SUSHI_HD/SUSHI/AVID/AV13/AT100#440/mask_res_10.tif"
    img = io.imread(imgname)
    seg_background(img,outname)
    print('Mask successfully saved.')


if __name__ == '__main__':
    main()


