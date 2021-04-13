
from flask import Flask, request
from flask_json import FlaskJSON,JsonError, json_response, as_json
import operationHandler as oph

app = Flask(__name__)
json = FlaskJSON(app)


@app.route('/')
def index():
    return json_response(msg = "test correct")

@app.route('/save-file',methods = ['POST'])
def save_file():
    
    '''
    accepts form data
    {
    root: test,
    path: '/',
    content: 'rohit is the hero',
    filename: 'text.txt'
    }
    '''
    root = request.form.get('root')
    path = request.form.get('path')
    content = request.form.get('content')
    filename = request.form.get('filename')
    # root, path,content,filename
    msg = oph.save_file(root=root, path=path,content=content,filename=filename)
    if msg == 'Done':
        return json_response(msg = "successful")
    else:
        return json_response(msg = "error")

@app.route('/save-commit',methods = ['POST'])
def save_commit():
    '''
    accepts json data
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
    payload = request.json
    print(payload)

    msg = oph.save_commit(payload = payload)
    print(msg)
    if msg[0:5] != 'error':
        return json_response(msg = "successful")
    else:
        return json_response(msg = msg)


@app.route('/pull-server',methods = ['POST'])
def pull_server():
    '''
    accepts form data
    {
    root: test,
    project_name: test_project,
    branch: username
    }
    '''
    #root,project_name,branch
    root = request.form.get('root')
    project_name = request.form.get('project_name')
    branch = request.form.get('branch')
    hiry = oph.pull_editor(root = root, project_name= project_name,branch=branch)
    return json_response(files = hiry)

@app.route('/get-file',methods = ['POST'])
def get_file():
    '''
    accepts form data
    {
    root: test,
    path: '/',
    filename: 'test.txt'
    }
    '''
    #root,path,filename
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    content = oph.get_file(root=root, path=path, filename = filename)
    return json_response(content = content)


@app.route('/delete-dir',methods = ['POST'])
def del_dir():
    '''
    accepts form data
    {
    root: test,
    path: '/',
    dirname: 'test1'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    dirname = request.form.get("dirname")
    hir = oph.delete_dir(root = root, path=path, dirname = dirname)
    return json_response(hir = hir)

@app.route('/delete-file',methods = ['POST'])
def del_file():
    '''
    accepts form data
    {
    root: test,
    path: '/',
    filename: 'test1.php'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    hir = oph.delete_file(root = root, path=path, filename = filename)
    return json_response(hir = hir)


@app.route('/make-dir',methods = ['POST'])
def make_dir():
    '''
    accepts form data
    {
    root: test,
    path: '/',
    dirname: 'test1'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    new_dir = request.form.get("dirname")
    hir,error = oph.delete_dir(root = root, path=path, new_dir = new_dir)
    return json_response(hir= hir,error = error)


@app.route('/make-file',methods = ['POST'])
def make_file():
    '''
    accepts form data
    {
    root: test,
    path: '/test1',
    filename: 'test1.txt'
    }
    '''
    #root,path,filename
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    file_hir,error = oph.make_file(root = root, path=path, filename = filename)
    return json_response(hir = file_hir,error= error)

@app.route('/make-repo',methods = ['POST'])
def make_repo():
    '''
    accepts form data
    {
    projectname: 'test_project'
    }
    '''
    projectname = request.form.get("projectname")
    msg = oph.make_repo(projectname)
    return json_response(msg = msg)

@app.route('/merge',methods = ['POST'])
def merge_repo():
    pass


if __name__ == "__main__":
    app.run(port = 5000)
