import os
import shutil
import subprocess
import pprint

class FHandler():
    base = "/home/rohit/php/"
    folder_path = "/home/rohit/php/"
    root=""
    dir_name = ""
    hierarchy = {"files":[]}
    hir_ar = []
    def __init__(self,dir_name,make_dir=False):
        self.root=dir_name
        self.dir_name = dir_name  
        if make_dir:
            a =  self.make_dir(dirname = dir_name,create_file=False)

        for d in dir_name.split("/"):
            self.folder_path = os.path.join(self.base,d)
        #print(self.folder_path)

    def set_default_path(self):
        '''
        This function is to set the dir to default
        '''
        # for dir in self.root.split("/"):
        #     self.folder_path = os.path.join(self.folder_path,dir)
        os.chdir(self.folder_path)

    def change_dir(self,dir_name):
        '''
        This function is to change directory
        '''
        p = self.folder_path
        for d in dir_name.split("/"):
            p = os.path.join(p,d)
        os.chdir(p)

    def current_dir(self):
        '''
        This will retun the current directory
        '''
        #path = os.getcwd()
        #path=path.replace("\\","/")
        return self.folder_path

    def make_dir(self,dirname,path="/",create_file=True):
        '''
        This function will create directory
        '''
        #return subprocess.run("mkdir "+dirname, capture_output = True, shell = True).returncode (This code is for linux)
        file_path = self.folder_path
        for p in path.split("/"):
            file_path = os.path.join(file_path,p)
        try:
            file_path = os.path.join(file_path,dirname)
            os.mkdir(file_path)
            if(create_file):
                file_path = os.path.join(file_path,"readme.txt")
                with open(file_path,"w") as f1:
                    f1.write("\n")
            return 1
        except FileExistsError:
            return 0
        


    def make_file(self,fname,path):
        '''
        This will create files
        '''
        file_path = self.folder_path
        for p in path.split("/"):
            file_path =os.path.join(file_path,p)
        file_path =os.path.join(file_path,fname)
        print(file_path)
        #if os.path
        try:
            f = open(file_path,"x")
            f.close()
            with open(file_path,"w") as f1:
                f1.write("#write your code here")
            return 1
        except FileExistsError:
            return 0


    def delete_folder_final(self):
        '''
        This will be used to delete the file
        '''
        shutil.rmtree(folder_path)
    def save_file(self,content,file_name,path='/'):
        '''
        This will be used to save the file to the current directory
        '''
        p=self.folder_path
        for i in path.split("/") :
            p = os.path.join(p,i)
        print(p)
        p = os.path.join(p, file_name)
        print(p)
        
        
        try: 
            with open(p,"wb") as f:
                f.write(content)
            return 1
        except:
            return 0

    def recursive_copy(self,src,path='/'):
        for item in os.listdir(src):
            if item[0] ==".":
                continue
            file_path = os.path.join(src, item)
            if os.path.isfile(file_path):
                file = { "path": path,	"filename": item }
                #print(item,path)
                self.hir_ar.append(file)
            elif os.path.isdir(file_path):
                item+="/"
                self.recursive_copy(file_path,path+item)

    def helper(self,hr,fol):
        if fol[0] in hr:
            if len(fol) == 0:
                return hr
            else:
                self.helper(hr[fol[0]],fol[1:])
        else:
            hr[fol[0]] = {"files":[],"conflict":[]}
            if len(fol)-1 == 0:
                return hr
            else:
                self.helper(hr[fol[0]],fol[1:])

    def sorter_hir(self,lis):
        hr = {"files":[],"conflict":[]}
        se = set()
        #print(len(lis))
        for i in lis:
            a = i['path']
            se.add(a)
        
        folders = sorted(se)
        r = []
        for j in folders:
            a = j.split("/")
            while "" in a:
                a.remove("")
            if len(a) == 0:
                continue
            self.helper(hr,a)
        pp = pprint.PrettyPrinter(indent=2)
        #print(hr)
        #print("Blue print")
        #pp.pprint(hr)
        for i in lis:
            conflict = self.check_conflict(path = i["path"],filename = i["filename"])
            a = i['path'].split("/")
            while "" in a:
                a.remove("")
            if len(a) == 0:
                hr["files"].append(i["filename"])
                if conflict:
                    hr["conflict"].append(i["filename"])
            else:
                temp = hr

                for fol in a:
                    temp = temp[fol]
                temp["files"].append(i["filename"])
                if conflict:
                    temp["conflict"].append(i["filename"])
        #print("Final hierarchy")
        #pp.pprint(hr)
        return hr
    def raw_file_structure(self):
        path = self.folder_path
        self.recursive_copy(path)
        return self.hir_ar

    def get_hierarchy(self):
        
        path = self.folder_path
        self.recursive_copy(path)
        return self.sorter_hir(lis = self.hir_ar)

        #return self.hierarchy

    def check_conflict(self,path,filename):
        data = self.get_file_content(path = path,filename = filename)
        if "=======" in data:
            return 1
        else: 
            return 0

    def get_file_content(self,filename,path="/"):
        
        p = self.folder_path
        for d in path.split("/"):
            p = os.path.join(p,d)
        content = ""
        final_p=os.path.join(p,filename)
        try:
            with open(final_p) as f:
                content = f.read()
        except FileExistsError:
            print("File does not exist")

        return content


if __name__=="__main__":
    fh = FHandler(dir_name = "test1")
    pprint.pprint(fh.get_hierarchy())