import glob
import os


train_dir = '/home/maryana/storage2/Posdoc/AVID/AV13/AT100/db_training'
test_dir = '/home/maryana/storage2/Posdoc/AVID/AV13/AT100/db_testing'
val_dir = '/home/maryana/storage2/Posdoc/AVID/AV13/AT100/db_validation'

patches = glob.glob(os.path.join(train_dir,'*.tif'))

