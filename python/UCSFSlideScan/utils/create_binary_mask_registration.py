import os
import glob
import skimage.io as io
import cv2



def create_masks(root_dir):
    files = glob.glob(os.path.join(root_dir,'*.png'))
    for f in files:
        try:
            #img = io.imread(f)
            img = cv2.imread(f)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if img.ndim > 3:
                img = img[:,:,0:3]
            R = img[:,:,0]
            G = img[:,:,1]
            B = img[:,:,2]
            maskR = R == 255
            maskG = G == 255
            maskB = B == 255
            mask = maskR & maskG & maskB
            mask_name = f[:-4] + '_dice_mask.tif'
            io.imsave(mask_name,(mask*255).astype('uint8'))
        except:
            print('Error processing file {}'.format(f))


if __name__ == '__main__':
    root_dir = '/home/maryana/R_DRIVE/Experiments/1_AVID/Cases/1811-001/Master_Package_1181-001/Images/1181-001_BLOCKFACE/blockface_transformed_for_Lea/maks_to_right_hipocampus/done'
    create_masks(root_dir)