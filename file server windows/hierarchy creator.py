import os
import pprint
import time
base = "D:\Dist Workspace\\test git files"
base = base.replace("\\","/")
root = "hierarchy"
# print(base)
# os.chdir(base)
# #print(os.listdir())
# for i in os.listdir():
#     file_path = os.path.join(base,i)
#     if os.path.isfile(file_path):
#         print(i,"File")
#     else:
#         print(i,"Dir")
# print(os.getcwd())
# f = open(os.path.join(os.getcwd(),"git_handler_backup.py"),"r")
# print(f.read())
hierarchy = []
def recursive_copy(src,path='/'):
    for item in os.listdir(src):
        if item[0] ==".":
            continue
        file_path = os.path.join(src, item)
        if os.path.isfile(file_path):
            file = { "path": path,	"filename": item }
            print(item,path)
            hierarchy.append(file)
        elif os.path.isdir(file_path):
            item+="/"
            recursive_copy(file_path,path+item)

def get_hierarchy():
    path1 = base
    path1 =os.path.join(path1,root)
    print(path1)
    recursive_copy(base)
    return hierarchy

def helper(hr,fol):
    #print(type(hr))
    #print(hr)
    if fol[0] in hr:
        if len(fol) == 0:
            return hr
        else:
            helper(hr[fol[0]],fol[1:])
    else:
        hr[fol[0]] = {"files":[]}
        if len(fol)-1 == 0:
            return hr
        else:
            helper(hr[fol[0]],fol[1:])

def sorter1(lis):
    hr = {"files":[]}
    se = set()
    print(len(lis))
    for i in lis:
        a = i['path']
        # while "" in a:
        #     a.remove("")
        se.add(a)
    
    folders = sorted(se)
    r = []
    for j in folders:
        a = j.split("/")
        while "" in a:
            a.remove("")
        if len(a) == 0:
            continue
        helper(hr,a)
    pp = pprint.PrettyPrinter(indent=2)
    #print(hr)
    print("Blue print")
    pp.pprint(hr)
    for i in lis:
        a = i['path'].split("/")
        while "" in a:
            a.remove("")
        if len(a) == 0:
            hr["files"].append(i["filename"])
        else:
            temp = hr

            for fol in a:
                temp = temp[fol]
            temp["files"].append(i["filename"])
    print("Final hierarchy")
    pp.pprint(hr)
    #return hr
    #print(se)
    
    # helper(hr,a)
    #    for j in a:
    #        if dict.has_key(j):
    #            continue
    #         else:
    #             hr[j] = {"files":[]}

t  = time.time()
print(sorter1(get_hierarchy()))
print(time.time()-t)
'''

{
    files:[],
    subfolder1:{
        files:[]
        sub-subfolder:{

        }
    },
    subfolder2:{
        files:[]
        sub-subfolder:{

        }
    }
}'''