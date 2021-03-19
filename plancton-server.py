from bottle import Bottle, run, template, route, static_file, get, request, response
import plancton as plct
# import svg2font as s2f
import subprocess
import os
from os import listdir
import glob
import random
import urllib
import json 

app = Bottle()

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
origin = [0, 18]

pl = plct.Plancton()

session = dict()

###########
# Session #
###########
session['zoom'] = '1' 
session['sentence'] = 'Abc'
session['current'] = 'none'
session['version'] = 'regular'

@app.route('/session_set/<key>/<value>')
def session_set(key, value):
    session[key] = value
    return session[key]

@app.route('/session_get/<key>')
def session_get(key):
    return session[key]

#######################
# Utilities Functions #
#######################
def write_file(loc, content):
    file = open(loc, 'w')
    file.write(str(content))
    file.close()

def load_json(dirFiles):
    with open(dirFiles, 'r') as f:
        data = json.load(f)
    return data

#################
# Statics Files #
#################
@app.route('/static/<filepath:path>')
def asset(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))

@app.route('/projects/<filepath:path>')
def files(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'projects'))

#################
# Templates URL #
#################
@app.route('/')
@app.route('/index')
def index():
    projects = glob.glob('projects/*/current.json')
    projectsjson = []
    
    for p in projects:
        d = load_json(p)
        projectsjson.append(d['font_info'])
    
    return template('templates/index.tpl', projectsjson=projectsjson)

@app.route('/type/<project>')
@app.route('/type/<project>/<keycode>')
def type(project, keycode='free'):
    pl.project = project
    # if keycode == 'free':
    #     pl.build_svg('-all') 
    SETFOLDER = glob.glob('projects/' + pl.project + '/mpost/mpost-files/*.mp')
    SET = []
    for CHAR in SETFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    rand = random.randint(1, 300)
    if keycode == 'free':
        chartKey = [keycode, session['sentence']]
    else:
    	chartKey = [keycode, chr(int(keycode))]
    print(pl.switchVersion('main', 'regular'))
    return template('templates/set-type.tpl', setchart=SET, rand=rand, mode='type', key=chartKey, PROJECT=pl.project, versions=pl.getVersions())


################
# COMMANDS URL #
################
@app.route('/add/<keycode>')
def add(keycode=False):
    if keycode == False:
        return "The keycode is missing !"
    pl.add_glyph(keycode)
    return "Glyph "+keycode+" has been created !"

@app.route('/delete/<keycode>')
def delete(keycode=False):
    if keycode == False:
        return "The keycode is missing !"
    pl.del_glyph(keycode)
    return "Glyph " +keycode+" has been removed!"

@app.route('/clean/<keycode>')
def delete(keycode=False):
    if keycode == False:
        return "The keycode is missing !"
    pl.clean_mp(keycode, True)
    return "Glyph " +keycode+" has been cleaned!"

@app.route('/generate_font/<project>/<keycode>')
def generate_font(project, keycode=False):
    if keycode == False:
        return "The keycode is missing !"
    return "Font has been generated!"

@app.route('/set/<PROJECT>')
def set(PROJECT):
    MPFOLDER = glob.glob('projects/' + pl.project + '/mpost/mpost-files/*.mp')
    out_path = 'projects/' + pl.project + '/output-svg/'
    SET = []
    for CHAR in MPFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(int(key))
    SET.sort()
    SET = list(map(str, SET))
    return '|'.join(SET)

##################
# WRITE FILE URL #
##################
@app.route('/write_json', method='post')
def write_json():
    json = request.forms.json
    sett = request.forms.set

    if sett != '-all':
        file = open('projects/' + pl.project + '/current.json','w') 
        file.write(json)
        file.close()     
        pl.build_global_mp() 
        for n in sett:
            pl.build_svg(ord(n)) 
    else:
        pl.build_svg('-all') 
    return json

@app.route('/write_mp', method='post')
def write_mp():
    PROJECT = request.forms.project
    mp = request.forms.mp
    key = request.forms.key
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write_file('projects/' + PROJECT + '/mpost/mpost-files/' + key + '.mp', mp)
    pl.build_svg(key)
    return mp

@app.route('/write_file', method='post')
def writefile():
    PROJECT = request.forms.project
    mp = request.forms.mp
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write_file('projects/' + PROJECT + '/mpost/def.mp', mp)
    return mp

#############
# EDIT FILE #
#############
@app.route('/inkscape', method='post')
def inkscape():
    PROJECT = request.forms.project
    key = request.forms.key
    subprocess.Popen(['inkscape', 'projects/' + PROJECT + '/input-svg/' + key + '.svg']) 
    return '<<<<<<< I N K S C A P E !' 

@app.route('/updateMp', method='post')
def editeSvg():
    PROJECT = request.forms.project
    key = request.forms.key
    plct.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key, origin)
    pl.build_svg(key) 
    return '! ! ! ! ! ! !' 

run(app, host="0.0.0.0", port=8088, reloader=True, debug=True)
