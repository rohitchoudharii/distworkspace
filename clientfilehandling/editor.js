
//////////////////// start-up script

function load_editor(){
    hir = await request_setup_hir(root,project_name,branch);
    root_element = document.getElementById("root");
    load_hir(hir,root_element,file_content);
}

////////////////////////////////////////Helper functions

function on_file_click(path){
    current_file = path;
    console.log(path);
    if(file_content[current_file].content == ""){
        file_content[current_file].content = await get_file(path);
    }else{
        document.getElementById("editor").value = file_data[current_file];
    }
}


function request_setup_hir(folder_root,projectname,branch_name){
    // call the api to setup the files
    //This function will return the hierarchy of the folder
    let formData = new FormData();
    formData.append("root",folder_root);
    formData.append("project_name",projectname);
    formData.append("branch",branch_name);
    const resp = await fetch(server+"/pull-server",{ body: formData, method: "post" });
    parse_resp = await resp.json();
    return parse_resp.files;
}


function folder_collapse(_id){
    el = document.getElementById(_id).childNodes;
    len = el.length;
    togle = el[1].style.display == "none" ? "block" : "none";
    i = 1;
    while(i!=len){
        ce = el[i];
        ce.style.display=togle;
        i=i+1;
    }
}

function load_hir(hir_files,parent_el,file_data){
    path = "";
    rec_helper(path,hir_files,parent_el,file_data);
}

function rec_helper(path,hir_files,parent_div,file_data){
    // This is an important function, if you would to add any sort of attribute in the element, it can be done from here
    for(i in hir_files){
        if(i=="files"){
            // attribute for the file can be fone from here
            for(j in hir_files.files){
                var para = document.createElement("div");        
                para.innerText = hir_files.files[j];           
                file_data[path+hir_files.files[j]] = {content:"",save:0};
                para.setAttribute("ondblclick","on_file_click('"+path+hir_files.files[j]+"')");
                parent_div.appendChild(para);  
            }
        }else{
            // attribute for the folder can be done from here
            var sub_folder = document.createElement("div");  
            var sub_folder_name = document.createElement("div");  
            var collapse_btn = document.createElement("button");  
            var create_file_btn = document.createElement("button");  
            var create_dir_btn = document.createElement("button");  
            var delete_dir_btn = document.createElement("button");  

            collapse_btn.innerHTML = i
            collapse_btn.setAttribute("onclick","folder_collapse('"+path+i+"')");

            create_file_btn.innerHTML = "CF";
            create_file_btn.setAttribute("onclick","create_file('"+path+i+"')");

            create_dir_btn.innerHTML = "CD";
            create_dir_btn.setAttribute("onclick","create_dir('"+path+i+"')");

            delete_dir_btn.innerHTML = "DD";
            delete_dir_btn.setAttribute("onclick","delete_dir('"+path+i+"')");
            sub_folder_name.appendChild(collapse_btn);
            sub_folder_name.appendChild(create_file_btn);
            sub_folder_name.appendChild(create_dir_btn);
            sub_folder_name.appendChild(delete_dir_btn);

            sub_folder.setAttribute("id",path+i);
            sub_folder.appendChild(sub_folder_name);
            parent_div.appendChild(sub_folder);
            rec_helper(path+i+"/", hir_files[i], sub_folder,file_data);
        }
    }
}
function loacl_file_saver(){
    if(current_file==""){
        console.log("Please select the file");
    }else{
        editor_content = document.getElementById("editor").value;
        file_content[current_file] = editor_content;
    }
}


////////////////// Main functions

function get_file(path){
// make a call to the api and get the file content 
    console.log("getting file for path: "+path);
    formData = new FormData();
    formData.append("root",root);
    formData.append("path","/");
    formData.append("filename",path);
    resp = await fetch(server + "/get-file",{
        body:formData,
        method: "post"
    });
    to_json = resp.json();
    return to_json.content;
}

function save_file(path){
    data = file_content[path];
    formData = new FormData();
    formData.append("root",root);
    formData.append("path","/");
    formData.append("filename",path);
    formData.append("content",data);
    resp = await fetch(server + "/get-file",{
        body:formData,
        method: "post"
    });
    to_json = resp.json();
    return to_json.msg;
}


/////////////Pending
// function commit_file(message){
//     // get the message 
//     // call save function
//     // make api call to commit 
// }

function save_commit_files(message){
    // pile up all the data and create one json and then call the api
    data = new Object();
    data.branch = branch;
    data.root = root;
    data.commit_msg = message;
    files_list = [];
    for(f in file_content){
        if(file_content[f] != "" && file_content[f]!=1){
            files_list.push({
                filename:f,
                content: file_content[f]
            });
        } 
    }
    data.files = files_list;
    resp = await fetch(server+"/save-commit",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    json_data = resp.json();
}


function create_file(path){
    // get the file name from prompt
    file_name = "test.php";

    // call the create file api and re-render the file hir 
    // create set of the current file set and the new file hir 

    // (perform)new_set.difference(old set)
    // append the result to the file_content with null value
    formData = new FormData();
    formData.append("root",root);
    formData.append("path","/");
    formData.append("filename",path);
    resp = await fetch(server + "/make-file",{
        body:formData,
        method: "POST"
    });
    to_json = resp.json();
    if(to_json.error == 0){
        new_file_hir = {};
        hir = to_json.hir;
        load_hir(hir,root_element,new_file_hir);
        setA = new set();
        for(el of Object.keys(new_file_hir)) setA.add(el);
        setB = new set();
        for(el of Object.keys(file_content)) setB.add(el);
        add_file_content( [...setA].filter(x=>setB.has(x)));

    }else{
        console.log("Somthing went wrong please go to dashboard and reload the editor");
    }

}

function delete_file(path){

    // call the delete api and re render the file hir 
    // create set of the current file set and new file hir

    // (perform) old_set.difference(new_set)
    // delete the result from the file content var
    formData = new FormData();
    formData.append("root",root);
    formData.append("path","/");
    formData.append("filename",path);
    resp = await fetch(server + "/delete-file",{
        body:formData,
        method: "POST"
    });
    to_json = resp.json();
    if(to_json.error == 0){
        new_file_hir = {};
        hir = to_json.hir;
        load_hir(hir,root_element,new_file_hir);
        setA = new set();
        for(el of Object.keys(new_file_hir)) setA.add(el);
        setB = new set();
        for(el of Object.keys(file_content)) setB.add(el);
        remove_file_content( [...setB].filter(x=>setA.has(x)));

    }else{
        console.log("Somthing went wrong please go to dashboard and reload the editor");
    }
}

function create_dir(path){
    // get the dirname from the prompt
    dirname = "test";
    // call the create file api and re-render the file hir 
    // create set of the current file set and the new file hir 

    // (perform)new_set.difference(old set)
    // append the result to the file_content with null value
    formData = new FormData();
    formData.append("root",root);
    formData.append("path",path);
    formData.append("dirname",dirname);
    resp = await fetch(server + "/make-dir",{
        body:formData,
        method: "POST"
    });
    to_json = resp.json();
    if(to_json.error == 0){
        new_file_hir = {};
        hir = to_json.hir;
        load_hir(hir,root_element,new_file_hir);
        setA = new set();
        for(el of Object.keys(new_file_hir)) setA.add(el);
        setB = new set();
        for(el of Object.keys(file_content)) setB.add(el);
        add_file_content( [...setA].filter(x=>setB.has(x)));
    }else{
        console.log("Somthing went wrong please go to dashboard and reload the editor");
    }
}

function delete_dir(path){
    // call the delete api and re render the file hir 
    // create set of the current file set and new file hir

    // (perform) old_set.difference(new_set)
    // delete the result from the file content var
    formData = new FormData();
    formData.append("root",root);
    formData.append("path","/");
    formData.append("dirname",path);
    resp = await fetch(server + "/delete-dir",{
        body:formData,
        method: "POST"
    });
    to_json = resp.json();
    if(to_json.error == 0){
        new_file_hir = {};
        hir = to_json.hir;
        load_hir(hir,root_element,new_file_hir);
        setA = new set();
        for(el of Object.keys(new_file_hir)) setA.add(el);
        setB = new set();
        for(el of Object.keys(file_content)) setB.add(el);
        remove_file_content( [...setB].filter(x=>setA.has(x)));

    }else{
        console.log("Somthing went wrong please go to dashboard and reload the editor")
    }
}

///////////// Client function Helper

function remove_file_content(files_ar){
    for(el of files_ar){
        delete file_content[el];
    }
}
function add_file_content(files_ar){
    for(el of files_ar){
        file_content[el] = {content:"",save:0};
    }
}
