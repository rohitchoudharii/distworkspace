
from file_handler import FHandler
from git_handler import GHandler
from paramiko import SSHClient
import subprocess
import time
import json
import os

def save_file(root, path,content,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    #fh.set_default_path()
    msg = fh.save_file(content = bytes(content,'utf-8'), file_name = filename,path = path)
    return msg

def commit(msg,branch,parent_path):
    fh = FHandler(parent_path)
    fh.set_default_path()
    gh = GHandler()
    gh.git_add()
    gh.git_commit(msg)
    gh.git_push(branch)
    res , flag = gh.execute()
    if flag:
        return "error"
    else:

        return "All good"

def save_commit(payload):
    '''
    {
        branch: branch_name,
        root: "root name",
        commit_msg: "first commit"
        files: [{
                    path: "/",
                    filename: "test.txt",
                    content:"test"
                },
                {
                    path: "/test",
                    filename: "test.txt",
                    content:"test"
                }]
    }
    '''
    #payload = json.loads(payload1)
    branch = payload["branch"]
    commit_msg = payload["commit_msg"]
    root = payload["root"]
    files = payload["files"]
    #Saving all the files
    for file in files:
        path = file['path']
        filename = file["filename"]
        content = file["content"]
        res = save_file(root=root,path = path,content = content, filename = filename)
        if res == "error":
            return "error saving"

    # commiting the code
    commit_res = commit(msg = commit_msg, branch = branch,parent_path = root)
    if commit_res == "error":
        return "error commiting"


    return "done"


def pull_editor(root,project_name,branch):
    '''
    Pull the data to php folder
    send the directory structure to the user
    '''
    print(branch)
    #Set the path and make the directory
    fh = FHandler("")
    print(fh.current_dir)
    fh.make_dir(root)
    print(fh.current_dir)
    fh.change_dir(root)
    print(fh.current_dir)
    gh = GHandler()
    #perform gti fetch
    gh.git_init()
    gh.git_remote_add(project_name = project_name)
    gh.git_pull_server(branch = branch)
    #msg, flag = gh.execute()
    del gh
    del fh
    #Fetch the file structure
    fh  = FHandler(root)

    hierarchy = fh.get_hierarchy()
    return hierarchy

def get_file(root,path,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    if path!="/":
        fh.change_dir(path)
        print(fh.current_dir())
    content = fh.get_file_content(filename)
    return content

def make_dir(root,path,new_dir):
    fh = FHandler(root)
    print(fh.current_dir())
    if path != '/':
        fh.change_dir(path)
    print(fh.current_dir())
    if fh.make_dir(new_dir) == 0:
        return "folder created"
    else:
        return "Folder already exist"

def make_file(root,path,filename):
    fh = FHandler(root)
    if path != '/':
        fh.change_dir(path)
    msg = fh.make_file(fname = filename)
    print(fh.current_dir())
    return msg
def make_repo(projectname):
    # send request to the git server using API
    pass
    # ps = subprocess.Popen("ssh git@192.168.100.4 git init --bare {projectname}.git".format(projectname = projectname),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True).communicate()
    # if ps[0][0].lower() == 'i':
    #     return "created"
    # else:
    #     return "name exist"

def merge_branch():
    pass


if __name__ == "__main__":
    # hir = pull_editor(str(time.time()),"project","master")
    # for files in hir:
    #     print(files)
    #ommit(msg,branch,parent_path)
    print(commit(msg = "Testing commit", branch = "branch1",parent_path="1603452897"))
