import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import sys
import skimage.measure as meas


def export_landmarks(lm_file,out_file):
    lm_sitk = sitk.ReadImage(lm_file)
    lmarks = sitk.GetArrayFromImage(lm_sitk)
    labels = np.unique(lmarks)




def main():
    if len(sys.argv) != 3:
        print('Usage: get_landmarks_for_elastix.py <landmarks_nii> <out.pts>')
        exit()
        lmarks_file = str(sys.argv[1])
        out_file = str(sys.argv[2])

if __name__ == '__main__':
    main()