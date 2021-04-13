import os
import shutil
import subprocess
from file_handler import FHandler

class MHandler():
    cwd = ""
    def __init__(self,cwd):
        self.cwd = cwd
        
    def git_diff(self,branch):
        msg = self.execute(command="git diff {branch}".format(branch=branch),dir_output = 1)
        
        return msg
    def git_checkout_patch(self,branch,filename):
        msg = self.execute(command="git checkout {branch} {file}".format(branch=branch,file=filename),dir_output = 1)
        print(msg)

    def git_merge(self,branch):
        msg = self.execute(command = "git merge {branch}".format(branch=branch),output="CONFLICT (content)")
    
    def git_pull(self,branch):
        msg = self.execute(command = "git pull {branch}".format(branch=branch),output="CONFLICT (content)")

    def execute(self,command,output=None,dir_output=0):
        ps = subprocess.run(args = command, capture_output = True, text=True,shell = True,cwd=self.cwd)
        # print(ps.stdout)
        # print(ps.stderr)
        # print(ps) 
        if dir_output == 1:
            return ps.stdout

        if output == None:
            return 
        
        
        if output in ps.stdout or ps.returncode != 0 :
            if ps.stderr == "":
                return ("somthing went wrong",True)
            else:
                return (ps.stdout,True)
        else:
            return (ps.stdout,False)
    
    # def check_error(self,data):
    #     if "=======" in data:
    #         return 1
    #     else: 
    #         return 0

    # def find_error(self,paths):
    #     error = 0
    #     for path in paths:
    #         temp = self.cwd
    #         for d in path["path"].split("/"):
    #             temp = os.path.join(temp,d)
    #         #print(temp)
    #         f_p = os.path.join(temp,path["filename"])
    #         print(f_p)
    #         fs = open(f_p)
    #         data = fs.read()
    #         error+= self.check_error(data)
    #     return error

if __name__ == "__main__":
    fh = FHandler("test")
    base_path = fh.current_dir()
    print(base_path)
    all_files = fh.raw_file_structure()
    mh = MHandler(base_path)
    print(mh.find_error(all_files))
    


