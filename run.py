from bottle import Bottle, run, template, route, static_file, get, request
import plancton as plct
import svg2font as s2f
import subprocess
import os
from os import listdir
from os.path import isfile, isdir, join
import glob
import random
import urllib
import json 

app = Bottle()
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

origin = [0, 18]

def write(loc, content):
    file = open(loc, 'w')
    file.write(str(content))
    file.close()

def loadJson(dirFiles):
    with open(dirFiles, 'r') as f:
        data = json.load(f)
    return data

@app.route('/static/<filepath:path>')
def asset(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))

@app.route('/projects/<filepath:path>')
def files(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'projects'))

@app.route('/')
@app.route('/index')
def index():
    globals = glob.glob('projects/*/global.json')
    projectsjson = []
    
    for p in globals:
        d = loadJson(p)
        projectsjson.append(d['font_info'])
    
    return template('templates/index.tpl', projectsjson=projectsjson)


@app.route('/setOff/<PROJECT>')
def setOff(PROJECT):
    INFOLDER = glob.glob('projects/' + PROJECT + '/input-svg/*.svg')
    MPFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')
    OUTFOLDER = glob.glob('projects/' + PROJECT + '/output-svg/*.svg')

    if not INFOLDER:
        return 'Il n\'y pas de fichiers'
    else:
        if not MPFOLDER: 
            plct.buildMp('projects/' + PROJECT + '/input-svg/', 'projects/' + PROJECT +  '/mpost/mpost-files/', '-all', origin)
            plct.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', '-all') 
            MPFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')
        if not OUTFOLDER: 

            plct.buildGlobalMp('projects/' + PROJECT + '/global.json','projects/' + PROJECT + '/mpost/global.mp' ) 
            plct.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/', 'projects/' + PROJECT + '/output-svg/', '-all') 
    SET = []
    for CHAR in MPFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    SET.sort()
    print(SET)
    SET = list(map(str, SET))
    return '|'.join(SET)
    # return template('templates/set-type.tpl', setchart=SET, rand=rand, mode="set", key="none", PROJECT=PROJECT)

@app.route('/set/<PROJECT>')
def set(PROJECT):
    MPFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')

    out_path = 'projects/' + PROJECT + '/output-svg/'
    SET = []
    for CHAR in MPFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        # if os.path.isfile(out_path+key+'.svg'):
        #     pass
        # else:
        #     plct.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', key) 

        SET.append(int(key))
    SET.sort()
    # print(SET)
    SET = list(map(str, SET))
    return '|'.join(SET)

@app.route('/type/<PROJECT>')
@app.route('/type/<PROJECT>/<keycode>')
def type(PROJECT, keycode='free'):
    SETFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')
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
    return template('templates/set-type.tpl', setchart=SET, rand=rand, mode='type', key=chartKey, PROJECT=PROJECT)

@app.route('/write-json', method='post')
def traitementJson():
    PROJECT = request.forms.project
    json = request.forms.json
    sett = request.forms.set
    if sett != '-all':
        file = open('projects/' + PROJECT + '/global.json','w') 
        file.write(json)
        file.close()     
        plct.buildGlobalMp('projects/' + PROJECT + '/global.json','projects/' + PROJECT + '/mpost/global.mp' ) 
        for n in sett:
            plct.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/',  'projects/' +PROJECT + '/output-svg/', ord(n)) 
    else:
        plct.buildSvg('projects/' + PROJECT +'/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', '-all') 
    sett = ''
    return json

@app.route('/write-mp', method='post')
def writeMp():

    PROJECT = request.forms.project
    mp = request.forms.mp
    key = request.forms.key
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write('projects/' + PROJECT + '/mpost/mpost-files/' + key + '.mp', mp)
    plct.buildSvg('projects/' + PROJECT +'/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', key) 
    return mp

@app.route('/write-file', method='post')
def writeF():
    PROJECT = request.forms.project
    mp = request.forms.mp
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write('projects/' + PROJECT + '/mpost/def.mp', mp)
    return mp

@app.route('/inkscape', method='post')
def inkscape():
    PROJECT = request.forms.project
    print('------------')
    print('------------')
    print(PROJECT)
    print('------------')
    print('------------')
    key = request.forms.key
    subprocess.Popen(['inkscape', 'projects/' + PROJECT + '/input-svg/' + key + '.svg']) 
    return '<<<<<<< I N K S C A P E !' 

@app.route('/updateMp', method='post')
def editeSvg():
    PROJECT = request.forms.project
    key = request.forms.key
    plct.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key, origin)
    plct.buildSvg('files/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', key) 
    return '! ! ! ! ! ! !' 

@app.route('/specimen')
@app.route('/specimen/<name>')
def specimen(name='temp'):
    archiveList = [f for f in listdir('files/fonts/archive/') if isdir('files/fonts/archive/' + f)]
    tt = name 
    return template('templates/specimen.tpl', archiveList=archiveList, elem=tt)

@app.route('/manager')
@app.route('/manager/<action>/<subaction>')
@app.route('/manager/<action>/<subaction>/<elem>')
def manager(action='none', subaction='false', elem='false'): 
    if action == 'generate':
        s2f.buildFont(subaction)
    if action == 'versions':
        if subaction == 'save':
            s2f.saveVersion()
        elif subaction == 'delete':
            s2f.deleteVersion(elem)
        else:
            return 'Il y a une erreur...'

    return 'yes'

run(app, host="0.0.0.0", port=8088, reloader=True, debug=True)
