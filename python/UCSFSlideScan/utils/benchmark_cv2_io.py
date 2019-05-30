import time
import glob
import random
import os
import cv2
import skimage.io as io

def main():
    num = 100
    list_files = glob.glob(os.path.join('/home/maryana/storage2/Posdoc/AVID/AT100/db_training/images','*.tif'))

    random.shuffle(list_files)
    elapsed = 0.
    for i in range(num):
        t = time.time()
        img = cv2.imread(list_files[i])
        elapsed += (time.time() - t)
    utime = elapsed/num
    print('OpenCV time:{}'.format(utime))


    random.shuffle(list_files)
    elapsed = 0.
    for i in range(num):
        t = time.time()
        img = io.imread(list_files[i])
        elapsed += (time.time() - t)
    utime = elapsed/num
    print('Skimage time:{}'.format(utime))










if __name__ == '__main__':
    main()