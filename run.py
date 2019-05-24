from bottle import Bottle, run, template, route, static_file, get, request
import lib.svg2mpost as s2m
import lib.svg2font as s2f
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

@app.route('/files/<filepath:path>')
def files(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'files'))

@app.route('/')
@app.route('/index')
def index():
    INFOLDER = glob.glob('files/input-svg/*.svg')
    MPFOLDER = glob.glob('files/mpost/mpost-files/*.mp')
    OUTFOLDER = glob.glob('files/output-svg/*.svg')
    if not INFOLDER:
        return 'Il n\'y pas de fichiers'
    else:
        if not MPFOLDER: 
            s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', '-all', origin)
            s2m.buildSvg('files/mpost/mpost-files/', '-all') 
            MPFOLDER = glob.glob('files/mpost/mpost-files/*.mp')
        if not OUTFOLDER: 
            s2m.buildSvg('files/mpost/mpost-files/', '-all') 
    SET = []
    for CHAR in MPFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    SET.sort()
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
    return template('templates/index.tpl', setchart=SET, rand=rand, mode='type', key=chartKey)

@app.route('/write', method='post')
def traitementJson():
    json = request.forms.json
    sett = request.forms.set
    if sett != '-all':
        file = open('files/global.json','w') 
        file.write(json)
        file.close()     
        s2m.buildGlobalMp('files/global.json') 
        for n in sett:
            s2m.buildSvg('files/mpost/mpost-files/', ord(n)) 
    else:
        s2m.buildSvg('files/mpost/mpost-files/', '-all') 
    sett = ''
    subprocess.popen('rm -f *.log')
    return json

@app.route('/write-mp', method='post')
def writeMp():
    mp = request.forms.mp
    key = request.forms.key
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write('files/mpost/mpost-files/' + key + '.mp', mp)
    s2m.buildSvg('files/mpost/mpost-files/', key) 
    return mp

@app.route('/write-file', method='post')
def writeF():
    mp = request.forms.mp
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    print(mp)
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
@app.route('/specimen/<elem>')
def specimen(elem='temp'):
    archiveList = [f for f in listdir('files/fonts/archive/') if isdir('files/fonts/archive/' + f)]
    return template('templates/specimen.tpl', archiveList=archiveList, elem=elem)

@app.route('/manager')
@app.route('/manager/<action>/<subaction>')
@app.route('/manager/<action>/<subaction>/<elem>')
def manager(action='none', subaction='false', elem='false'): 
    if action == 'generate':
        s2f.buildFont(subaction)
        print('salut')
    if action == 'versions':
        if subaction == 'save':
            s2f.saveVersion()
        elif subaction == 'delete':
            s2f.deleteVersion(elem)
        else:
            return 'Il y a une erreur...'

    return 'yes'

run(app, host="localhost", port=8088, reloader=True, debug=True)
