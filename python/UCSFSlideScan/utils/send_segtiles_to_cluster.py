import fnmatch
import os
import sys
import glob
import paramiko
import time
import select


#From StackOverflow (https://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python)
class SSH_Helper:
    def __init__(self, retry_time=0):
        self.retry_time = retry_time
        self.ssh = None
        self.sftp = None
        pass

    def connect(self, host_ip, user_name):
        i = 0
        while True:
        # print("Trying to connect to %s (%i/%i)" % (self.host, i, self.retry_time))
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(hostname=host_ip,username=user_name)
                self.sftp = self.ssh.open_sftp()
                break
            except paramiko.AuthenticationException:
                print("Authentication failed when connecting to %s" % host_ip)
                sys.exit(1)
            except:
                print("Could not SSH to %s, waiting for it to start" % host_ip)
                i += 1
                time.sleep(2)

    def disconnect(self):
        self.ssh.close()

    def run_cmd(self, cmd):
        print(cmd)
        # execute commands
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    tmp = stdout.channel.recv(1024)
                    output = tmp.decode()
                    print output

    def exists(self,remote_path):
        try:
            print(self.sftp.stat(remote_path))
            return True
        except IOError:
            return False

    def mkdir(self,remote_dir):
        self.sftp.mkdir(remote_dir)

    def send_file(self,remote_path,local_file):
        self.sftp.put(localpath=local_file,remotepath=remote_path,confirm=True)



def send_files(local_root,remote_root):

    #get list of local folders
    local_files = os.listdir(local_root)
    dir_list = []
    for fi in local_files:
        if os.path.isdir(os.path.join(local_root,fi)):
            dir_list.append(fi)


    #open ssh channel
    ssh_helper = SSH_Helper()
    ssh_helper.connect('wynlog1.compbio.ucsf.edu','malegro')

    #create folders on remoter server
    for direc in dir_list:

        if direc.find('magick_tmp') != -1:
            continue

        print('*** Folder {} ***'.format(direc))

        remote_path = os.path.join(remote_root,direc) #ex: /../../AT100_280
        remote_seg = os.path.join(remote_path,'heat_map')
        remote_TAU_seg = os.path.join(remote_seg,'TAU_seg_tiles')

        local_path = os.path.join(local_root,direc) #ex: /../../AT100_280
        local_seg = os.path.join(local_path,'heat_map')
        local_TAU_seg = os.path.join(local_seg,'TAU_seg_tiles')

        if ssh_helper.exists(remote_path):

            print('Folder {} exists. OK.'.format(remote_path))

            # create remote folders if necessary
            if ssh_helper.exists(remote_seg):
                print('Folder {} exists. OK.'.format(remote_seg))

                if not ssh_helper.exists(remote_TAU_seg):
                    print('Folder {} does not exists. Creating it...'.format(remote_TAU_seg))
                    ssh_helper.mkdir(remote_TAU_seg)
                else:
                    print('Folder {} exists. OK.'.format(remote_TAU_seg))
            else:

                print('Folder {} does not exists. Creating it...'.format(remote_seg))
                ssh_helper.mkdir(remote_seg)
                print('Folder {} does not exists. Creating it...'.format(remote_TAU_seg))
                ssh_helper.mkdir(remote_TAU_seg)

            #copy files
            tile_list = glob.glob(os.path.join(local_TAU_seg,'*.tif'))

            for tile in tile_list:

                print('Sending {}'.format(tile))

                tile_name = os.path.basename(tile)
                remote_tile = os.path.join(remote_TAU_seg, tile_name)
                ssh_helper.send_file(remote_tile,tile)

        else:
            #case is not in the cluster, skip it
            print('Folder {} does not exist. Skipping.'.format(remote_path))

    ssh_helper.disconnect()
    print('Finished sending files')


def main():
    if len(sys.argv) != 3:
        print('Usage: send_segtiles_to_cluster.py <local_root_dir> <cluster_root_dir>')
        exit()

    local_dir = str(sys.argv[1])  # abs path to where the images are
    remote_dir = str(sys.argv[2])

    #local_dir = '/home/maryana/storage/Posdoc/AVID/AV13/TEMP'
    #remote_dir = '/grinberg/scratch/AVID/TEMP'

    send_files(local_dir,remote_dir)


if __name__ == '__main__':
    main()