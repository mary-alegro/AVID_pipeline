import fnmatch
import os
import sys
import glob
# import paramiko
# import time
# import select
from SSH_Helper import SSH_Helper


def check_hm_files(local_root,remote_root, report_path):

    #get list of local folders
    local_files = os.listdir(local_root)
    dir_list = []
    for fi in local_files:
        if os.path.isdir(os.path.join(local_root,fi)):
            dir_list.append(fi)


    #open ssh channel
    ssh_helper = SSH_Helper()
    ssh_helper.connect('wynlog1.compbio.ucsf.edu','malegro')

    report_f = None
    nDirs = len(dir_list)
    if nDirs > 0: #if list is not empty
        report_f = open(report_path,"w")


    nInc = 0

    #find folders on remoter server
    for direc in dir_list:

        if direc.find('magick_tmp') != -1:
            continue

        print('*** Folder {} ***'.format(direc))

        #get slice number
        slice_id = direc[direc.find('_')+1:]

        remote_path = os.path.join(remote_root,'s'+slice_id,direc) #ex: /../../s280/AT100_280
        remote_hm = os.path.join(remote_path,'heat_map','hm_map_0.1')
        remote_hm_file = os.path.join(remote_hm,'heat_map_0.1_res10.nii')

        local_path = os.path.join(local_root,direc) #ex: /../../AT100_280
        local_hm = os.path.join(local_path,'heat_map','hm_map_0.1')
        local_hm_file = os.path.join(local_hm,'heat_map_0.1_res10.nii')

        if ssh_helper.exists(remote_hm): #check if remote folder exists
            if ssh_helper.exists(remote_hm_file):
                if os.path.exists(local_hm_file):
                    cmd = 'ssh malegro@wynlog1.compbio.ucsf.edu "cat {}" | cmp - {}'.format(remote_hm_file,local_hm_file)
                    result = os.popen(cmd).read()
                    if result: #if string is not empty, files are not the same so add t o the report
                        line = '*** {} <> {}\n'.format(remote_hm_file,local_hm_file)
                        print(line)
                        report_f.write(line)
                        #report_f.write(result)
                        nInc += 1

                else:
                    line = 'Local file {} does not exist.\n'.format(local_hm_file)
                    report_f.write(line)
                    print(line)
            else:
                line = 'Remote file {} does not exist.\n'.format(remote_hm_file)
                report_f.write(line)
                print(line)

        else:
            #case is not in the cluster, skip it
            line = 'Remote folder {} does not exist. Skipping.\n'.format(remote_path)
            report_f.write(line)
            print(line)

    report_f.write('{} inconsistent file(s)\n'.format(nInc))

    ssh_helper.disconnect()
    report_f.close()
    print('Finished sending files')



def main():
    if len(sys.argv) != 4:
        print('Usage: send_segtiles_to_cluster.py <local_root_dir> <cluster_root_dir> <report_file>')
        exit()

    local_dir = str(sys.argv[1])  # abs path to where the images are
    remote_dir = str(sys.argv[2])
    report_file = str(sys.argv[3])

    check_hm_files(local_dir,remote_dir,report_file)


if __name__ == '__main__':
    main()