import subprocess
from time import sleep

class GHandler():
    cmd = []
    def __init__(self):
        pass
    def git_add(self):
        self.cmd.append("git add .")
    def git_commit(self,msg):
        self.cmd.append('git commit -m "{ms}"'.format(ms=msg))
    def git_push(self,branch):
        self.cmd.append('git push origin {brch}'.format(brch=branch))

    def git_clone(self,server,project_name,branch):
        self.cmd.append('git clone -b {brch} {server}:{project}.git'.format(brch=branch,server=server,project=project_name))

    def git_init(self):
        self.cmd.append("git init")
    def git_remote_add(self,project_name):
        self.cmd.append("git remote add origin git@192.168.100.4:{projectname}.git".format(projectname = project_name))
    def git_pull_server(self, branch):
        self.cmd.append("git pull origin {branch}".format(branch=branch))

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
