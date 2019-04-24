from bottle import Bottle, run, template, route, static_file, get, request
import lib.svg2mpost as s2m
import subprocess
import os
import glob
import random
import urllib

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
    # s2m.buildSvg('files/mpost/mpost-files/', '-all') 
    SETFOLDER = glob.glob('files/mpost/mpost-files/*.mp')
    SET = []
    for CHAR in SETFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    print(SET.sort())
    return template('templates/index.tpl', setchart=SET, rand=rand, mode="set", key="none")

@app.route('/type')
@app.route('/type/<keycode>')
def type(keycode='free'):
    SETFOLDER = glob.glob('files/mpost/mpost-files/*.mp')
    SET = []
    for CHAR in SETFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    if keycode == 'free':
    	chartKey = [keycode, 'Ab']
    else:
    	chartKey = [keycode, chr(int(keycode))]
    print(SET.sort())
    return template('templates/index.tpl', setchart=SET, rand=rand, mode="type", key=chartKey)



@app.route('/write', method='post')
def traitementJson():
    json = request.forms.json
    sett = request.forms.set
    if sett != '-all':
        file = open('files/global-1.json','w') 
        file.write(json)
        file.close()     
        s2m.buildGlobalMp('files/global-1.json') 
        for n in sett:
            s2m.buildSvg('files/mpost/mpost-files/', ord(n)) 
    else:
        s2m.buildSvg('files/mpost/mpost-files/', '-all') 
    sett = ''
    print(json)
    return json

@app.route('/writeMp', method='post')
def writeMp():
    mp = request.forms.mp
    key = request.forms.key
    mp = mp.replace('#59', ';')
    file = open('files/mpost/mpost-files/' + key + '.mp','w') 
    file.write(str(mp))
    file.close()     
    print(mp)
    s2m.buildSvg('files/mpost/mpost-files/', key) 
    return mp

@app.route('/inkscape', method="post")
def inkscape():
    key = request.forms.key
    subprocess.Popen(["inkscape", "files/input-svg/" + key + ".svg"])
    
    return '<<<<<<< I N K S C A P E !' 

@app.route('/updateMp', method="post")
def editeSvg():
    key = request.forms.key
    s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key)
    s2m.buildSvg('files/mpost/mpost-files/', key) 
    return '! ! ! ! ! ! !' 

run(app, host="localhost", port=8080, reloader=True, debug=True)


