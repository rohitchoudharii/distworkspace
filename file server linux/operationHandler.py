
from file_handler import FHandler
from git_handler import GHandler
#from paramiko import SSHClient
import subprocess
import time
import json
import os



def commit(msg,branch,root):
    fh = FHandler(dir_name = root)
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

def pull_editor(root,project_name,branch):
    '''
    Pull the data to php folder
    send the directory structure to the user
    '''
    print(branch)
    #Set the path and make the directory
    fh = FHandler(root,make_dir=True)
    print(fh.current_dir())
    gh = GHandler(cwd = fh.current_dir())
    #perform gti fetch
    gh.git_init()
    gh.git_remote_add(project_name = project_name)
    #gh.add_ssh()
    print(fh.current_dir())
    gh.git_pull_server(branch = branch)
    #msg, flag = gh.execute()
    del gh
    del fh
    #Fetch the file structure
    fh  = FHandler(root)

    hierarchy = fh.get_hierarchy()
    return hierarchy

def save_commit(payload):
    '''
    {
        branch: branch_name,
        root: "root name",
        commit_msg: "first commit"
        files: [{
                    filename: "test.txt",
                    content:"test"
                },
                {
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
        #path = file['path']
        path = "/"
        filename = file["filename"]
        content = file["content"]
        res = save_file(root=root,path = path,content = content, filename = filename)
        if res == 0:
            return "error saving"

    # commiting the code
    commit_res = commit(msg = commit_msg, branch = branch,parent_path = root)
    if commit_res == "error":
        return "error commiting"

    return "done"


def save_file(root, path,content,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    #fh.set_default_path()
    msg = fh.save_file(content = bytes(content,'utf-8'), file_name = filename,path = "/")
    return msg

def get_file(root,path,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    # if path!="/":
    #     fh.change_dir(path)
    #     print(fh.current_dir())
    content = fh.get_file_content(filename=filename,path="/")
    return content

def make_dir(root,path,dir_name):
    fh = FHandler(root)
    # if path != '/':
    #     fh.change_dir(path)
    # print(fh.current_dir())
    if fh.make_dir(dir_name) == 1:
        return fh.get_hierarchy(),0
    else:
        return 0,1

def make_file(root,path,filename):
    fh = FHandler(root)
    if fh.make_file(fname = filename,path=path) == 1:
        return fh.get_hierarchy(),0
    else:
        return 0,1
def make_repo(projectname):
    # send request to the git server using API
    pass
    # ps = subprocess.Popen("ssh git@192.168.100.4 git init --bare {projectname}.git".format(projectname = projectname),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True).communicate()
    # if ps[0][0].lower() == 'i':
    #     return "created"
    # else:
    #     return "name exist"

def delete_dir(root,path,dirname){
    fh = FHandler(root)
    fh.delete_dir(dirname = dirname)
    return fh.get_hierarchy()
}

def delete_file(root,path,filename){
    fh = FHandler(root)
    fh.delete_file(filename = filename)
    return fh.get_hierarchy()
}

def tester(root):
    t = time.time()
    # fh = FHandler(dir_name= root)
    # fh.get_hierarchy()
    # fh.set_default_path()
    # gh = GHandler()
    # print(gh.git_init())
    # gh.git_add()
    # print(gh.git_commit(msg = "1234"))
    pull_editor(root,project_name="git123",branch="master")
    print(time.time() - t)

if __name__ == "__main__":
    # hir = pull_editor(str(time.time()),"project","master")
    # for files in hir:
    #     print(files)
    #ommit(msg,branch,parent_path)
    #print(save_file(content = "Test file",root="dist", path='/',filename="test.txt"))
    print(tester(root="test1"))