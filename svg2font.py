import fontforge
import lxml.etree as et
import glob
import os
from svg.path import parse_path
import psMat
import json
import urllib
import subprocess
from datetime import datetime

def getInfoPath(f, pattern):
    file = open(f, "r")
    elem = et.parse(file)
    root = elem.getroot()
    for child in root:
        for child in root:
            if child.tag == '{http://www.w3.org/2000/svg}path':
                if child.attrib['style'].startswith(pattern):
                    dparse = parse_path(child.attrib['d'])
                    for point in dparse:
                        type = str(point)[0:4]
                        x = dparse[1].start.real
                        y = dparse[2].end.imag * -1
                        h = dparse[1].start.imag 
                        w = dparse[1].end.real
    return [x, y, w, h]

def removeCadra(g, pattern):
    file = open(g, "r")
    elem = et.parse(file)
    root = elem.getroot()
    for child in root:
        if child.tag == '{http://www.w3.org/2000/svg}path':
            if child.attrib['style'].startswith(pattern):
                b = child
                root.remove(b)
    et.dump(root)
    return et.tostring(root, encoding='utf8', method='xml').decode()
    
def saveVersion():
    now = datetime.now()
    now = now.strftime("%y-%m-%d_%H-%M-%S")
    os.popen('cp -rf files/fonts/archive/temp/ files/fonts/archive/' + now)
    # A finir !!
    # os.popen('mv files/fonts/archive/' + now + '/temp.{u}')

def deleteVersion(elem):
    os.popen('rm -rf files/fonts/archive/' + elem + '/')

def buildFont(PATH_,outline):
    # compositeChar = [192, 193, 194, 195, 196, 199, 200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 217, 218, 219, 220, 224, 225, 226, 227, 231, 232, 233, 234, 235, 236, 237, 238, 239, 242, 243, 244, 249, 250, 251, 252, 350, 351]
    SVG_DIR = glob.glob(PATH_+'/output-svg/*.svg')

    # os.popen('cp -rf files/output-svg/ files/fonts/archive/temp/')
    # with open('files/global.json') as json_data:
    #     d = json.load(json_data)
    #     height = 1000 / int(d['font_info']['height']) 
    #     descent = height * int(d['font_info']['descent'])
    #     ascent = height * int(d['font_info']['ascent'])
    # font = fontforge.open('.tmp/empty.sfd')
    font = fontforge.font()

    for g in SVG_DIR:

        gkey = g.split("/")[-1].replace(".svg", "")
        if gkey.isdigit() == True:
            with open(g, 'rt') as gp:
                treeLet = et.parse(gp)

            rootLet = treeLet.getroot()
            gwidth = rootLet.get('width')
            gheight = rootLet.get('height')
            gwidth = round(float(gwidth))
            # gclean = removeCadra(g, 'stroke:rgb(100.000000%,0.000000%,0.000000%);')
            # pos = getInfoPath(g, 'stroke:rgb(100.000000%,0.000000%,0.000000%);')
            # scaleValue = 1000 / pos[3]
            # f = open(g, 'w')
            # f.write(str(gclean)) 
            # f.close()

            if outline == True:
                subprocess.call(['bash', 'lib/outline.sh', 'files/fonts/archive/temp/output-svg/' + gkey + '.svg']) 

            letter_char = font.createChar(int(gkey))
            letter_char.importOutlines(PATH_ + gkey + '.svg')
            letter_char.left_side_bearing = letter_char.right_side_bearing = 10
            print(gkey, '->>>', svg)
            # letter_char.removeOverlap()
            # letter_char.width = (gwidth * scaleValue)

    # for letter_comp in compositeChar:
    #     glyphAcc = font.createChar(letter_comp)
    #     glyphAcc.build()

    # trs = psMat.translate(0, -70) 
    # font.selection.all()
    # font.transform(trs)
    # font.correctDirection()
    # font.removeOverlap()
    # font.simplify()
    # font.round()
    # font.ascent = ascent
    # font.descent = descent 
    font.generate('temp.otf')
    font.generate('temp.ufo')
    font.close()
    # subprocess.call(['fontforge', 'temp.otf'])


    
buildFont('bac-a-sable/output-svg', False)
