
from flask import Flask, request
from flask_json import FlaskJSON,JsonError, json_response, as_json
import subprocess

app = Flask(__name__)
json = FlaskJSON(app)


@app.route('/')
def index():
    return json_response(msg = 'test correct')

@app.route('/create-repo',methods = ['GET'])
def create_repo():
    '''
    {
    'projectname':'ABCD'
    }
    '''
    projectname = request.args.get('projectname')
    ps = subprocess.Popen('git init --bare {projectname}.git'.format(projectname = projectname),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True).communicate()
    
    if ps[0][0].lower() == 'i':
        return json_response(msg = 'file created',error=0)
    else:
        return json_response(msg = 'Project already exist',error=1)

if __name__ == '__main__':
    app.run(port = 8080,host="0.0.0.0")
