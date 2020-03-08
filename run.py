from bottle import Bottle, run, template, route, static_file, get, request
import svg2mpost as s2m
import svg2font as s2f
import subprocess
import os
from os import listdir
from os.path import isfile, isdir, join
import glob
import random
import urllib

app = Bottle()
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

origin = [0, 18]

def write(loc, content):
    file = open(loc, 'w')
    file.write(str(content))
    file.close()

@app.route('/static/<filepath:path>')
def asset(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))

@app.route('/projects/<filepath:path>')
def files(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'projects'))

@app.route('/')
@app.route('/index')
def set(PROJECT):
    return 'no project'


@app.route('/set/<PROJECT>')
def set(PROJECT):
    INFOLDER = glob.glob('projects/' + PROJECT + '/input-svg/*.svg')
    MPFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')
    OUTFOLDER = glob.glob('projects/' + PROJECT + 'files/output-svg/*.svg')
    
    if not INFOLDER:
        return 'Il n\'y pas de fichiers'
    else:
        if not MPFOLDER: 
            s2m.buildMp('projects/' + PROJECT + '/input-svg/', 'files/mpost/mpost-files/', '-all', origin)
            s2m.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/', '-all') 
            MPFOLDER = glob.glob('projects/' + PROJECT + '/mpost/mpost-files/*.mp')
        if not OUTFOLDER: 
            s2m.buildSvg('files/mpost/mpost-files/', '-all') 
    SET = []
    for CHAR in MPFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    SET.sort()
    return template('templates/set-type.tpl', setchart=SET, rand=rand, mode="set", key="none", PROJECT=PROJECT)

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
    print(SET.sort())
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
        s2m.buildGlobalMp('projects/' + PROJECT + '/global.json') 
        for n in sett:
            s2m.buildSvg('projects/' + PROJECT + '/mpost/mpost-files/', ord(n), 'projects/' +PROJECT + '/output-svg/') 
    else:
        s2m.buildSvg('projects/' + PROJECT +'/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', '-all') 
    sett = ''
    return json

@app.route('/write-mp', method='post')
def writeMp():
    PROJECT = request.forms.project
    mp = request.forms.mp
    key = request.forms.key
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write('/mpost/mpost-files/' + key + '.mp', mp)
    s2m.buildSvg('files/mpost/mpost-files/', 'projects/' +PROJECT + '/output-svg/', key) 
    return mp

@app.route('/write-file', method='post')
def writeF():
    mp = request.forms.mp
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write('files/mpost/def.mp', mp)
    return mp

@app.route('/inkscape', method='post')
def inkscape():
    key = request.forms.key
    subprocess.Popen(['inkscape', 'files/input-svg/' + key + '.svg']) 
    return '<<<<<<< I N K S C A P E !' 

@app.route('/updateMp', method='post')
def editeSvg():
    key = request.forms.key
    s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key, origin)
    s2m.buildSvg('files/mpost/mpost-files/', key) 
    return '! ! ! ! ! ! !' 

@app.route('/specimen')
@app.route('/specimen/<name>')
def specimen(name='temp'):
    archiveList = [f for f in listdir('files/fonts/archive/') if isdir('files/fonts/archive/' + f)]
    tt = name 
    return template('templates/specimen.tpl', archiveList=archiveList, elem=tt)

# /manager/generate/
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
