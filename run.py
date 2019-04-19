from bottle import Bottle, run, template, route, static_file, get, request
import lib.svg2mpost as s2m
import subprocess
import os

app = Bottle()
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

print(ROOT_PATH)

@app.route("/static/<filepath:path>")
def asset(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))

@app.route("/files/<filepath:path>")
def files(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'files'))

@app.route('/')
@app.route('/index')
def index():
    return template('templates/index.tpl')

@app.route('/write', method='post')
def traitement():
    json = request.forms.json
    sett = request.forms.set

    if sett != '-all':
        file = open('files/global-1.json','w') 
        file.write(json)
        file.close()     
        s2m.buildGlobalMp('files/global-1.json') 
        for n in sett:
            s2m.buildSvg('files/mpost/mpost-files/', ord(n)) 
            print(ord(n))
    else:
        s2m.buildSvg('files/mpost/mpost-files/', '-all') 
        print('all')
    sett = ''
    return json

@app.route('/inkscape', method="post")
def inkscape():
    key = request.forms.key
    subprocess.Popen(["inkscape", "files/input-svg/" + key + ".svg"])
    
    return '<<<<<<< I N K S C A P E !' 

@app.route('/updateMp', method="post")
def editeSvg():
    key = request.forms.key
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ' + key)
    s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key)
    s2m.buildSvg('files/mpost/mpost-files/', key) 
    return '! ! ! ! ! ! !' 

run(app, host="localhost", port=8080, reloader=True, debug=True)


