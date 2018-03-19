import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import sys
import skimage.measure as meas

iterationNumbers = 6000
spatialSamples = 6000

#folder = '/home/maryana/storage/Posdoc/AVID/test_elastix/'
folder = '/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/test_elastix/'

ref = sitk.ReadImage(folder+'1181_001-Whole-Brain_0344.png.nii')
mov = sitk.ReadImage(folder+'ants_AT100_344_affine.nii')
#ref_mask = sitk.ReadImage('MASK_1181_001-Whole-Brain_0457_v2.png.nii',sitk.sitkUInt8)


# elastixImageFilter = sitk.ElastixImageFilter()
# elastixImageFilter.SetMovingImage(mov)
# elastixImageFilter.SetFixedImage(ref)
# elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
# elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap("affine"))
# elastixImageFilter.Execute()
# sitk.WriteImage(elastixImageFilter.GetResultImage(),'/home/maryana/storage/Posdoc/AVID/test_elastix/elastix_AT100_457_h2b_noland.nii')

elastixImageFilter = sitk.ElastixImageFilter()
# elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap('translation'))
# elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('rigid'))
# elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('affine'))
#elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('affine'))
elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap('bspline'))
elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('bspline'))
elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('bspline'))
elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('bspline'))
#elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('bspline'))


elastixImageFilter.SetParameter(0,'FinalGridSpacingInPhysicalUnits','15.0')
elastixImageFilter.SetParameter(1,'FinalGridSpacingInPhysicalUnits','11.0')
elastixImageFilter.SetParameter(2,'FinalGridSpacingInPhysicalUnits','7.0')
elastixImageFilter.SetParameter(3,'FinalGridSpacingInPhysicalUnits','5.0')
#elastixImageFilter.SetParameter(4,'FinalGridSpacingInPhysicalUnits','4.0')



elastixImageFilter.SetMovingImage(mov)
elastixImageFilter.SetFixedImage(ref)
#elastixImageFilter.SetFixedMask(ref_mask)


#elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('affine'))

elastixImageFilter.LogToConsoleOn()
#elastixImageFilter.SetParameter("Registration","MultiMetricMultiResolutionRegistration")
# ##elastixImageFilter.SetParameter( "Metric", ("NormalizedMutualInformation", "CorrespondingPointsEuclideanDistanceMetric",))
# #elastixImageFilter.SetParameter(1,"Metric0Weight", "0.0")
# #elastixImageFilter.SetParameter(1,"Metric1Weight", "10.0")
#elastixImageFilter.AddParameter("Metric", "CorrespondingPointsEuclideanDistanceMetric" )
# elastixImageFilter.SetParameter("Metric0Weight", "0")
# elastixImageFilter.SetParameter("Metric1Weight", "0")
# elastixImageFilter.SetParameter("Metric2Weight", "1.0")
#
# elastixImageFilter.SetFixedPointSetFileName("/home/maryana/storage/Posdoc/AVID/test_elastix/ref_ants_ctr.pts")
# elastixImageFilter.SetMovingPointSetFileName("/home/maryana/storage/Posdoc/AVID/test_elastix/mov_ants_ctr.pts")

# elastixImageFilter.SetParameter("MaximumNumberOfIterations" , str(iterationNumbers))
# elastixImageFilter.SetParameter("NumberOfSpatialSamples" , str(spatialSamples))

elastixImageFilter.PrintParameterMap()

elastixImageFilter.Execute()
sitk.WriteImage(elastixImageFilter.GetResultImage(),folder+'elastix_AT100_344_bspline.nii')


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