import subprocess
from time import sleep

class GHandler():
    cmd = []
    def __init__(self):
        pass
    def print_ps(self,ps):
        if ps.returncode == 0:
            print(ps.stdout)
        else:
            print(ps.stderr)

    def git_add(self):
        command = "git add ."
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)
    def git_commit(self,msg):
        command = 'git commit -m "{ms}"'.format(ms=msg)
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)
    def git_push(self,branch):
        command = 'git push origin {brch}'.format(brch=branch)
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)

    def git_clone(self,server,project_name,branch):
        command = 'git clone -b {brch} {server}:{project}.git'.format(brch=branch,server=server,project=project_name)
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)

    def git_init(self,ipAdr):
        command = "git init"
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)
    def git_remote_add(self,project_name):
        command = "git remote add origin ubuntu@{ipAdr}:{projectname}.git".format(projectname = project_name,ipAdr=ipAdr)
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)
    def git_pull_server(self, branch):
        command = "git pull origin {branch}".format(branch=branch)
        ps = subprocess.run(command, capture_output = True, text=True,shell = True)
        self.print_ps(ps)

    def execute(self):
        for command in self.cmd:
            print(command)
            ps = subprocess.run(command, capture_output = True, text=True,shell = True)
            print(ps.stdout)
            print(ps.stderr)
            if ps.returncode!=0:
                return (ps.stderr,True)
            else:
                continue
        return ("Done",False)
