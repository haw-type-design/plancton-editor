from bottle import Bottle, run, template, route, static_file, get 
import lib.svg2mpost as s2m
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

@app.route('/writejson', method='POST')
def writeJson():
    s2m.buildGlobalMp('files/global.json') 
    s2m.buildSvg('files/mpost/mpost-files/') 
    return 'yess';


run(app, host="localhost", port=8080, reloader=True, debug=True)


