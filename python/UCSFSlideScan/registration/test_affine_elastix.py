import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import sys
import skimage.measure as meas


ref = sitk.ReadImage('/home/maryana/storage/Posdoc/AVID/test_elastix/1181_001-Whole-Brain_0457.png.nii')
mov = sitk.ReadImage('/home/maryana/storage/Posdoc/AVID/test_elastix/AT100_457_res10.nii')

elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetMovingImage(mov)
elastixImageFilter.SetFixedImage(ref)
elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap("affine"))
elastixImageFilter.Execute()
sitk.WriteImage(elastixImageFilter.GetResultImage(),'/home/maryana/storage/Posdoc/AVID/test_elastix/elastix_AT100_457_h2b_noland.nii')