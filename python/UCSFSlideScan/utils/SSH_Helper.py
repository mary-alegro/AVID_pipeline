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
            except paramiko.AuthenticationException as exc:
                print("Authentication failed when connecting to %s" % host_ip)
                print(exc)
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
            self.sftp.stat(remote_path)
            return True
        except IOError:
            return False

    def mkdir(self,remote_dir):
        self.sftp.mkdir(remote_dir)

    def send_file(self,remote_path,local_file):
        self.sftp.put(localpath=local_file,remotepath=remote_path,confirm=True)

    # def compare_files(self, remote_path, local_path):
    #     if not self.exists(remote_path):
    #         raise IOError('Remote file {} does not exist'. format(remote_path))
    #
    #     if not os.path.exists(local_path):
    #         raise IOError('Local file {} does not exist'. format(local_path))



