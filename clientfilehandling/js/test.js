hir = {}
file_content = {
}
str = '{"files": ["test11.txt", "git tst.txt", "b1_1", "r1", "git_merge.txt"], "test1": {"files": ["test11.txt"], "testapi1": {"files": ["readme.txt", "testapi3.txt"], "testapi3": {"files": ["readme.txt", "testapi4.txt"]}}}, "test11": {"files": ["readme.txt"]}, "testapi": {"files": ["readme.txt", "testapi1.txt"]}, "testapi1": {"files": ["readme.txt", "testapi2.txt"]}}';





function load_hir(hir_files,file_data){
    path = ""
    parent_div = document.getElementById("root")
    rec_helper(path,hir_files,parent_div,file_data)
}
function folder_collapse(_id){
    el = document.getElementById(_id).childNodes
    len = el.length
    togle = el[1].style.display == "none" ? "block" : "none"

    console.log(el)
    i = 1
    while(i!=len){
        ce = el[i]
        ce.style.display=togle
        i=i+1
    }
}