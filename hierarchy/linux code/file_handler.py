import os
import shutil
import subprocess

class FHandler():
    file_path = "/home/client/php-server/"
    dir_name = ""
    hierarchy = []
    def __init__(self,dir_name):
        for dir in dir_name.split("/"):
            self.file_path = os.path.join(self.file_path,dir)
        self.dir_name = dir_name
        self.hierarchy = []
        os.chdir(self.file_path)

    def set_default_path(self):
        '''
        This function is to set the dir to default
        '''
        for dir in self.dir_name.split("/"):
            self.file_path = os.path.join(self.file_path,dir)
        os.chdir(self.file_path)

    def change_dir(self,dir_name):
        '''
        This function is to change directory
        '''
        for dir in dir_name.split("/"):
            os.chdir(os.path.join(self.file_path,dir))

    def current_dir(self):
        '''
        This will retun the current directory
        '''
        return subprocess.run("pwd", capture_output = True, text = True, shell = True).stdout[:-1]

    def make_dir(self,dirname):
        '''
        This function will create directory
        '''
        return subprocess.run("mkdir "+dirname, capture_output = True, shell = True).returncode

    def make_file(self,fname):
        '''
        This will create files
        '''

        if subprocess.run("cat "+fname, capture_output = True, shell = True).returncode == 1:
            subprocess.run("touch "+fname, capture_output = True, shell = True)
            return "file created"
        else:
            return "file already exist"

    def delete_folder_final(self):
        '''
        This will be used to delete the file
        '''
        shutil.rmtree(file_path)
    def save_file(self,content,file_name,path=None):
        '''
        This will be used to save the file to the current directory
        '''
        if path != None:
            #self.set_default_path()
            self.change_dir(path)
        print(self.current_dir())
        p = os.path.join(self.current_dir(), file_name)
        print(p)
        ps = subprocess.run("cat > "+p , input = content, capture_output = True, shell = True)
        if ps.returncode == 0:
            return "Done"
        else:
            return "error"

    def recursive_copy(self,src,path='/',):
        for item in os.listdir(src):
            if item[0] ==".":
                continue
            file_path = os.path.join(src, item)
            if os.path.isfile(file_path):
                file = { "path": path,	"filename": item }
                self.hierarchy.append(file)
            elif os.path.isdir(file_path):
                item+="/"
                self.recursive_copy(file_path,path+item)

    def get_hierarchy(self):
        self.recursive_copy(self.current_dir())
        return self.hierarchy


    def get_file_content(self,filename):
        content = subprocess.run("cat "+filename , capture_output = True, shell = True).stdout
        return content
