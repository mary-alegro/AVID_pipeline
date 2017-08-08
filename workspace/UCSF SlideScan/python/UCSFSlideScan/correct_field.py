import matplotlib.pyplot as plt
import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import ntpath


def do_field_correction(tiles_dir,dark_file,flats_dir,out_dir):

    dark = np.load(dark_file)
    files = glob.glob(tiles_dir + "*.tif")
    nFiles = len(files)
    for f in range(nFiles):
        file_path = files[f] #tile path
        file_name = ntpath.basename(file_path)
        file_name_base = os.path.splitext(file_name)[0]
        flat_name = flats_dir + 'tile_44' + '.npy'
        flat = np.load(flat_name)

        img = io.imread(file_path)
        img = img.astype(float)

        darkR = dark[:, :, 0]
        darkG = dark[:, :, 1]
        darkB = dark[:, :, 2]

        flatR = flat[:, :, 0]
        flatG = flat[:, :, 1]
        flatB = flat[:, :, 2]

        R = img[:, :, 0]
        G = img[:, :, 1]
        B = img[:, :, 2]

        Mr = np.mean(R.flatten())
        i_dr = (R - darkR)
        f_dr = (flatR - darkR)
        c_imgr = Mr * (i_dr / f_dr)
        c_imgr2 = np.round(c_imgr)
        corrR = c_imgr2.astype("uint8")

        Mg = np.mean(G.flatten())
        i_dg = (G - darkG)
        f_dg = (flatG - darkG)
        c_imgg = Mg * (i_dg / f_dg)
        c_imgg2 = np.round(c_imgg)
        corrG = c_imgg2.astype("uint8")

        Mb = np.mean(B.flatten())
        i_db = (B - darkB)
        f_db = (flatB - darkB)
        c_imgb = Mb * (i_db / f_db)
        c_imgb2 = np.round(c_imgb)
        corrB = c_imgb2.astype("uint8")

        cR = corrR.reshape(corrR.shape[0], corrR.shape[1], 1)
        cG = corrG.reshape(corrG.shape[0], corrG.shape[1], 1)
        cB = corrB.reshape(corrB.shape[0], corrB.shape[1], 1)
        corr_img = np.concatenate((cR, cG, cB), axis=2)  # RGB

        out_file = out_dir + file_name
        io.imsave(out_file, corr_img)



def main():
    if len(sys.argv) != 5:
        print('Usage: compute_master_dark <absolute_path_tiles> <absolute_path_master_dark_file> <absolute_path_master_tile_flats> <absolute_path_output_file>')
        exit()

    tiles_dir = str(sys.argv[1])  # abs path to where the images are
    dark_file = str(sys.argv[2])
    flats_dir = str(sys.argv[3])
    out_dir = str(sys.argv[4])

    do_field_correction(tiles_dir,dark_file,flats_dir,out_dir)

if __name__ == '__main__':
    main()