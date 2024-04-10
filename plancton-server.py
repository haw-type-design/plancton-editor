from bottle import Bottle, run, template, route, static_file, get, request, response
import plancton as plct
import plancton.gitManager as gm 
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
gitm = gm.gitManager()
gitm.project_path = ''

session = dict()

###########
# Session #
###########
session['zoom'] = '1' 
session['sentence'] = ''
session['current'] = 'none'
session['version'] = 'none'

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

    defFiles = []

    mpFiles= glob.glob('projects/' + pl.project + '/mpost/*.mp')
    for mpFile in mpFiles:
        defFile =  os.path.basename(mpFile)
        defFile =  defFile.replace('.mp', '')
        print("deffff"+defFile)
        if defFile != "global":
            defFiles.append(defFile )
        
    print(defFiles)
    gitm.project_path = 'projects/' + pl.project
    versions = gitm.branch_list()
    
    for v in versions:
        if v.startswith('*'):
            current_version = v
        else: 
            current_version = 'main'

    if keycode == 'free':
        pl.build_svg('-all') 
    SETFOLDER = glob.glob('projects/' + pl.project + '/mpost/mpost-files/*.mp')
    SET = []
    for CHAR in SETFOLDER:
        mpFile = os.path.basename(str(CHAR))
        key = os.path.splitext(mpFile)[0]
        SET.append(key)
    rand = random.randint(1, 300)
    if keycode == 'free':
        chartKey = [keycode, session['sentence']]
    else:
    	chartKey = [keycode, chr(int(keycode))]
    # print(pl.switchVersion('main', 'regular'))
    return template('templates/set-type.tpl', setchart=SET, rand=rand, mode='type', key=chartKey, PROJECT=pl.project, versions=versions, current_version=current_version, defFiles=defFiles)


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
    return "Glyph "+keycode+" has been removed!"



@app.route('/clean/<keycode>')
def clean(keycode=False):
    if keycode == False:
        return "The keycode is missing !"
    pl.clean_mp(keycode, True)
    return "Glyph " +keycode+" has been cleaned!"

@app.route('/clean/<keycode>')
def clean(keycode=False):
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

# @app.route('/editglobal', method='post')
# def edit_global(data):
#     json = request.forms.json
#     sett = request.forms.set
#     file = open('projects/' + pl.project + '/global.json','w')
#     file.write(data)
#     file.close()
      
    
    
    
##################
# CREATE PROJECT #
##################
@app.route('/create/<project>')
def createProject(project):
    pl.newProject(project, "null", "null", "null")
    projects = glob.glob('projects/*/current.json')
    projectsjson = []
    
    for p in projects:
        d = load_json(p)
        projectsjson.append(d['font_info'])
    return template('templates/index.tpl', projectsjson=projectsjson)



##################
# GIT COMMANDS   #
##################

@app.route('/git/<action>/<branch>/<message>')
def git_action(action=False, branch=False, message=False):
    if action == 'checkout':
        if branch.startswith('*'):
            return 'c\'est la branch courante' 
        else:
            rr = gitm.checkout_branch(branch)
            return rr 
    elif action == 'save':
        rr = gitm.save('.', branch, message)
        return rr 


##################
# WRITE FILE URL #
##################


@app.route('/write_mp', method='post')
def write_mp():
    PROJECT = request.forms.project
    mp = request.forms.mp
    key = request.forms.key
    file = request.forms.file
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
    write_file('projects/' + PROJECT + '/mpost/' + file + '.mp', mp)
    pl.build_svg(key)
    return mp

@app.route('/write_file', method='post')
def writefile():

    PROJECT = request.forms.project
    mp = request.forms.mp
    file = request.forms.file
    key = request.forms.key
    print('FILLLE'+ file)
    print('KEY'+ key)
    mp = mp.replace('#59', ';')
    mp = mp.replace('#45', '+')
   
    if file == str(key):
        print('mpost')
        chemin = '/mpost/mpost-files/' + file + '.mp'
        write_file('projects/' + PROJECT + chemin, mp)
        pl.build_svg(key)
    else:
        chemin = '/mpost/' + file + '.mp'
        write_file('projects/' + PROJECT + chemin, mp)
    
    return mp




@app.route('/write_global', method='post')
def write_global():
   
    data = request.forms.data
    sett = request.forms.set
    PROJECT = request.forms.project

    if sett != '-all':
        data = data.replace('#59', ';')
        data = data.replace('#45', '+')
        file = open('projects/'+pl.project+'/mpost/global.mp','w')
        file.write(data)
        file.close() 
        
        for n in sett:
            pl.build_svg(ord(n)) 
    else:
        pl.build_svg('-all') 
    
    return data

@app.route('/write_json', method='post')
def write_json():
    json = request.forms.json
    sett = request.forms.set

    if sett != '-all':
        file = open('projects/' + pl.project + '/current.json','w') 
        file.write(json)
        file.close()     
        #pl.build_global_mp() 
        for n in sett:
            pl.build_svg(ord(n)) 
    else:
        pl.build_svg('-all') 
    return json

@app.route('/write_css', method='post')
def write_css():
    css = request.forms.css
    file = open('static/css/' + pl.project + '.css','w') 
    file.write(css)
    file.close()     
    
    return css

# TEST FONT 

@app.route('/testing/<project>')
def test_font(project):
    pl.project = project 
    pl.svg_to_font()
    return template('templates/test.tpl', project=project)

#############
# EDIT FILE #
#############

@app.route('/updateMp', method='post')
def editeSvg():
    PROJECT = request.forms.project
    key = request.forms.key
    plct.buildMp('files/input-svg/', 'files/mpost/mpost-files/', key, origin)
    pl.build_svg(key) 
    return '! ! ! ! ! ! !' 

run(app, host="0.0.0.0", port=8088, reloader=True, debug=True)
