import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import sys
import skimage.measure as meas



ref = sitk.ReadImage('/home/maryana/storage/Posdoc/AVID/test_elastix/1181_001-Whole-Brain_0457.png.nii')
mov = sitk.ReadImage('/home/maryana/storage/Posdoc/AVID/test_elastix/ants_AT100_457_affine_centered.nii')

parameterMap = sitk.GetDefaultParameterMap("bspline")
parameterMap['Transform'] = ['SplineKernelTransform']
parameterMap['SplineKernelType'] = ['ThinPlateSpline']

parameterMapVector = sitk.VectorOfParameterMap()
parameterMapVector.append(parameterMap)

elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetParameterMap(parameterMapVector)
elastixImageFilter.LogToConsoleOn()
elastixImageFilter.PrintParameterMap()

elastixImageFilter.SetFixedImage(ref)
elastixImageFilter.SetMovingImage(mov)
elastixImageFilter.SetFixedPointSetFileName('/home/maryana/storage/Posdoc/AVID/test_elastix/ref_ants_ctr.pts')
elastixImageFilter.SetMovingPointSetFileName('/home/maryana/storage/Posdoc/AVID/test_elastix/mov_ants_ctr.pts')

elastixImageFilter.Execute()



sitk.WriteImage(elastixImageFilter.GetResultImage(),'/home/maryana/storage/Posdoc/AVID/test_elastix/elastix_AT100_457_h2b_landmarks.nii')
img = elastixImageFilter.GetResultImage()
np_img = sitk.GetArrayFromImage(img)
np_img[np_img < 0] = 0
ref_img = sitk.GetArrayFromImage(ref)
ref_img[ref_img < 0] = 0

img_to_show = np.zeros((np_img.shape[0],np_img.shape[1],3))
img_to_show[:,:,0] = np_img
img_to_show[:,:,1] = sitk.GetArrayFromImage(ref)

plt.imshow(img_to_show)
plt.show()
pass