import sys


TAG_STR = 'InitialTransformParametersFileName'
NEW_TAG_STR = '(InitialTransformParametersFileName "{}/TransformParameters.{}.txt")'

#(InitialTransformParametersFileName "/home/ssatrawada/Desktop/AV2AT100Registrations/276/1stStep:Automatic/TransformParameters.0.txt")

def edit_txt(file_arr,new_path):




def main():
    if len(sys.argv) != 5:
        print('Usage: apply_combined_registrations.py <slice_dir> <mov_file> <ref_file> <reg_file>')
        exit()

    slice_dir = sys.argv[1]
    mov_file = sys.argv[2] #histology or heatmap
    ref_file = sys.argv[3] #blockface
    reg_file = sys.argv[4] #output: registered heatmap/histology

    # slice_dir = '/home/maryana/storage/Posdoc/AVID/AV23/AT100/full_res/AT100_164'
    # mov_file = '/home/maryana/storage/Posdoc/AVID/AV23/AT100/full_res/AT100_164/reg/AT100_164_res10.nii'
    # ref_file = '/home/maryana/storage/Posdoc/AVID/AV23/AT100/full_res/AT100_164/reg/AV13-002_0164.png.nii'
    # reg_file = '/home/maryana/storage/Posdoc/AVID/AV23/AT100/full_res/AT100_164/reg/reg.nii'


if __name__ == '__main__':
    main()