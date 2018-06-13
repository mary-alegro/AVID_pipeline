import fnmatch
import os
import sys
import glob
from SSH_Helper import SSH_Helper
import re


def get_sliceid_from_str(arr):

    sliceid_str = ''
    sliceid = re.search(r'\/AT\d{1,3}[\#_]\d{1,3}\/', arr, re.M | re.I)
    if not sliceid:
        sliceid = re.search(r'\/MC1\d{1,3}[\#_]\d{1,3}\/', arr, re.M | re.I)

    if sliceid:
        sliceid_str = sliceid.group()
        sliceid_str = sliceid_str.replace('/','').replace('#', '_')

    if sliceid_str == '':
        print('Warning: String does not contain valid slice id.')

    return sliceid_str

def get_subdirs(root_dir):
    dirs_list = glob.glob(os.path.join(root_dir,'*/'))
    return dirs_list


def get_fullres_files(root_dir):
    fullres_files = {}
    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root, '*/RES(*'):  # it's inside /RES*
            for fn in fnmatch.filter(files, '*_*_*.tif'):  # get only full resolution images
                if fn.find('res10') > -1:  # skip res10 images
                    continue
                else:
                    sliceid = get_sliceid_from_str(root)
                    fullres_files[sliceid] = {'full_res':os.path.join(root,fn)}
    return fullres_files


def get_res10_files(root_dir):
    res10_files = {}
    for root, dir, files in os.walk(root_dir):
        if fnmatch.fnmatch(root, '*/RES(*'):  # it's inside /RES*
            for fn in fnmatch.filter(files, '*res10*.tif'):  # get only full resolution images
                if fn.find('res10') > -1:  # get res10 images
                    sliceid = get_sliceid_from_str(root)
                    res10_files[sliceid] = {'res10':os.path.join(root,fn)}
                    break

    return res10_files

def send_files(local_root,remote_root):

    fullres_files = {}
    res10_files = {}

    nfull_not_found = 0
    nres10_not_found = 0

    #get slice folders and look for files
    list_dirs = get_subdirs(local_root)

    print('{} folders found.'.format(len(list_dirs)))

    for sdir in list_dirs:
        fullres_info = get_fullres_files(sdir)
        res10_info = get_res10_files(sdir)

        if not fullres_info:
            print('Fullres not found ({})'.format(sdir))
            nfull_not_found += 1
        else:
            keyid = fullres_info.keys()[0]
            tmpdic = fullres_info[keyid]
            fileinfo = tmpdic['full_res']
            fullres_files[keyid] = {'full_res':fileinfo}


        if not res10_info:
            print('Res10 not found ({})'.format(sdir))
            nres10_not_found += 1
        else:
            keyid = res10_info.keys()[0]
            tmpdic = res10_info[keyid]
            fileinfo = tmpdic['res10']
            res10_files[keyid] = {'res10':fileinfo}

    print('{} full res files not found.'.format(nfull_not_found))
    print('{} res 10 fies not found.'.format(nres10_not_found))


    #open ssh channel
    ssh_helper = SSH_Helper()
    ssh_helper.connect('wynlog1.compbio.ucsf.edu','malegro')

    # send full res files
    print('Transfering full res images.')
    for sliceid in fullres_files.keys():
        file_info = fullres_files[sliceid]

        remote_path = os.path.join(remote_root,sliceid,'output/RES(0x0)')
        if ssh_helper.exists(remote_path): #it should exist but we are checking just in case
            print('Folder {} exists. OK.'.format(remote_path))
        else:
            print('Folder {} does not exists. Creating it...'.format(remote_path))
            ssh_helper.mkdir(remote_path)

        #send file
        local_img_path = file_info['full_res']
        img_name = os.path.basename(local_img_path)
        remote_img_path = os.path.join(remote_path,img_name)

        print('Sending {}'.format(local_img_path))
        ssh_helper.send_file(remote_img_path,local_img_path)

    #send res10 files
    print('Transfering 10% res images.')
    for sliceid in res10_files.keys():
        file_info = res10_files[sliceid]

        remote_path = os.path.join(remote_root, sliceid, 'output/RES(0x0)')
        if ssh_helper.exists(remote_path):  # it should exist but we are checking just in case
            print('Folder {} exists. OK.'.format(remote_path))
        else:
            print('Folder {} does not exists. Creating it...'.format(remote_path))
            ssh_helper.mkdir(remote_path)

        # send file
        local_img_path = file_info['res10']
        img_name = os.path.basename(local_img_path)
        remote_img_path = os.path.join(remote_path, img_name)

        print('Sending {}'.format(local_img_path))
        ssh_helper.send_file(remote_img_path, local_img_path)



    ssh_helper.disconnect()
    print('Finished sending files')






def main():
    #if len(sys.argv) != 3:
    #    print('Usage: send_files_to_cluster.py <local_root_dir> <remote_root_dir>')
    #    exit()

    #local_root_dir = str(sys.argv[1])  # abs path to where the images are
    #rem_root_dir = str(sys.argv[2])

    # local_root_dir = '/Volumes/macdata/groups/grinberg/Experiments/AVID/Cases/1181-002/Master Package 1181-002/Images/Stitched/AT100'
    local_root_dir = '/home/maryana/R_DRIVE/Experiments/AVID/Cases/1181-002/Master Package 1181-002/Images/Stitched/AT100'
    rem_root_dir = '/grinberg/scratch/AVID/AV2_AT100'

    send_files(local_root_dir,rem_root_dir)


if __name__ == '__main__':
    main()
