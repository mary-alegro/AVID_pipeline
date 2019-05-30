
import os
import uuid
import glob
import shutil




def main():
    image_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/db_validation/images'
    mask_dir = '/home/maryana/storage2/Posdoc/AVID/AV23/AT100/db_validation/masks'

    file_list = glob.glob(os.path.join(image_dir,'*.tif'))
    for f in file_list:
        filename = os.path.basename(f)  # tile names are always 'tile_????.tif'
        idx1 = filename.find('_')
        idx2 = filename.find('.')
        snum = filename[idx1 + 1:idx2]
        snum = int(snum)

        maskname = 'patch_{}_mask.tif'.format(snum)
        mask_file_name = os.path.join(mask_dir,maskname)
        if not os.path.exists(mask_file_name):
            print('Error: mask {} not found'.format(mask_file_name))
            continue

        uu_id = str(uuid.uuid1())
        new_filename = 'patch_{}.tif'.format(uu_id)
        new_maskname = 'patch_{}_mask.tif'.format(uu_id)


        old_filename = os.path.join(image_dir,filename)
        old_maskname = os.path.join(mask_dir,maskname)
        new_filename = os.path.join(image_dir,new_filename)
        new_maskname = os.path.join(mask_dir,new_maskname)

        try:
            print('Copying {} to {}'.format(old_filename,new_filename))
            shutil.copy(old_filename,new_filename)
        except:
            os.remove(new_filename)

        try:
            print('Copying {} to {}'.format(old_maskname, new_maskname))
            shutil.copy(old_maskname,new_maskname)
        except:
            os.remove(new_filename)

        os.remove(old_filename)
        os.remove(old_maskname)









if __name__ == '__main__':
    main()