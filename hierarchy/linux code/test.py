# from paramiko import SSHClient
# ssh = SSHClient()
# ssh.connect('192.168.100.4',username = 'git',password = 'Rohit0987')
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('git init --bare tst.git')
# print(ssh_stdout) #print the output of ls command
import subprocess

ps = subprocess.Popen("ssh {user}@{host} {cmd}".format(user='git', host='192.168.100.4', cmd='git init --bare test1.git'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True).communicate()
print(ps[0][0])
