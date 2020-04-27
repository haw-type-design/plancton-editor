#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
import glob
import os
import subprocess
import lxml.etree as ElementTree
# from svg.path import parse_path
# from svgpathtools import svg2paths
from svgpathtools import svg2paths, parse_path
import svgwrite
import re 

Template = '''
% {char}
input ../def;
beginchar({keycode}, {width});
    {cordonates} 
    {draws}
endchar({lenpoints});
end;
'''

class Plancton:
    def __init__(self):
        self.mp_template = '''
        % {char}
        input ../def;
        beginchar({keycode}, {width});
            {cordonates} 
            {draws}
        endchar({lenpoints});
        end;
        '''
        self.dir_projects = 'projects'
        self.project = 'meta-old-french'
        self.global_json = 'global.json'


    def read_json(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def adjust_viewbox(f_svg):
        tree = ElementTree.parse(f_svg)
        root = tree.getroot()
        p = root.find(".//{http://www.w3.org/2000/svg}path")
        d_string = p.get('d')
        pp = parse_path(d_string)
        xmin, xmax, ymin, ymax = pp.bbox()
        width = xmax - xmin
        height = ymax - ymin
        root.set('width', str(width))
        root.set('height', str(height))
        root.set('viewBox', "{0} {1} {2} {3}".format(int(xmin), int(ymin), int(width), int(height)))
        tree.write(open(f_svg, 'wb'), encoding='unicode')

    def build_svg(self, key):
        project_path = self.dir_projects+'/'+self.project
        mp_path = project_path+'/mpost/mpost-files/'
        svg_path = project_path+'/output-svg/'
        print(svg_path)

        if key != '-all':
            SET = glob.glob(mp_path + str(key) + '.mp')
            SET_svg = glob.glob( svg_path + str(key) + '.svg')
        else:
            SET = glob.glob(mp_path + '*.mp')
            SET_svg = glob.glob(svg_path + '*.svg')

        for mp in SET:
            mpFile = os.path.basename(mp)
            subprocess.call(["mpost", "-interaction=batchmode", mp])
            for LOG in glob.glob('*.log'):
                os.remove(LOG)
        for svg in SET_svg:
            print('HEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEE')
            Plancton.adjust_viewbox(svg)

    def del_glyph(self, key):
        project_path = self.dir_projects+'/'+self.project
        insvg = project_path+'/input-svg/'+str(key)+'.svg'
        outsvg = project_path+'/output-svg/'+str(key)+'.svg'
        mp = project_path+'/mpost/mpost-files/'+str(key)+'.mp'

        if os.path.isfile(insvg):
            os.remove(insvg)
        if os.path.isfile(outsvg):
            os.remove(outsvg)
        if os.path.isfile(mp):
            os.remove(mp)

        return str(key)+' has been deleted !'

    def add_glyph(self, key):
        project_path = self.dir_projects+'/'+self.project
        json_path = project_path+'/'+self.global_json
        inputsvg_path = project_path+'/input-svg/'
        json_path = project_path+'/'+self.global_json
        
        if os.path.isfile(inputsvg_path + str(key) + '.svg'):
            return str(key)+' already exist ! Use del_glyph('+str(key)+') before.'
        else: 
            json = Plancton.read_json(json_path)
            height = json['font_info']['height']
            width = int(int(height)/2) 

            svg = svgwrite.Drawing(str(key) + '.svg', size=(width, height))
            svg.viewbox(0, 0, width, height)
            svg.saveas(project_path+'/input-svg/'+str(key)+'.svg')
            
            buildFig = Template.format(
                char       = chr(int(key)),
                keycode    = key,
                width      = width,
                cordonates = '',
                draws      = '',
                lenpoints  = '0' 
            )
            f = open(project_path+'/mpost/mpost-files/'+str(key)+'.mp', 'w')
            f.write(buildFig) 
            f.close()
            # os.chmod(project_path+'/mpost/mpost-files/'+str(key)+'.mp', 755)

            self.build_svg(key)

            return str(key)+' has been create !'


    def clean_mp(self, key, write=False):

        def Sort(sub_li):
            l = len(sub_li)
            for i in range(0, l):
                for j in range(0, l-i-1):
                    if (int(sub_li[j][2]) > int(sub_li[j + 1][2])):
                        tempo = sub_li[j]
                        sub_li[j]= sub_li[j + 1]
                        sub_li[j + 1]= tempo
            return sub_li

        project_path = self.dir_projects+'/'+self.project
        mp = project_path+'/mpost/mpost-files/'+str(key)+'.mp'
        
        with open(mp) as fl: 
            data = fl.read()
        pattern = '(([x|y|z])([0-9]+))'
        result = re.findall(pattern, data)
        o = []
        for v in result: o.append(int(v[2]))
        o = list(set(o))
        o.sort()
        i = 1
        fin = dict()
        for k in o:
            fin[k] = i 
            i = i + 1
        result = Sort(result)

        for r in result:
            v = int(r[2])
            data = re.sub(r'('+r[0]+')([^0-9])', r[1]+str(fin[v])+'\g<2>', data)
        data = re.sub(r'(endchar\()(.*)\);?', '\g<1>'+str(len(fin))+');', data)

        if write == True:
            file = open(mp, 'w')
            file.write(data)
            file.close()

        return data

def parsePath(path, OX, OY):
    dparse = parse_path(path)
    cordonates = []
    draws = []
    inc = 1
    incD = 0 
    y = 20
    line = ' --'
    curve = ' ..'
    for point in dparse:
        type = str(point)[0:4]
        if type == 'Move':
            if incD > 0:
                cordonates.append('x' + str(inc) + ' := ' + str(dparse[inc - 1].end.real - OX) + ' * ox;')
                cordonates.append('y' + str(inc) + ' := ' + str(y - dparse[inc - 1].end.imag + y - OY) + ' * oy;')
                draws.append(' z' + str(inc))
                draws.append('; \n')
                inc = inc + 1

            draws.append('draw')
            incD = 1
            ii = 0

        elif type == 'Line' or type == 'Cubi': 

            cordonates.append('x' + str(inc) + ' := ' + str(point.start.real - OX) + ' * ox;')
            cordonates.append('y' + str(inc)+ ' := ' + str(y - point.start.imag + y - OY) + ' * oy;')
 
            draws.append(' z' + str(inc))
            if type == 'Line':
                draws.append(line)
            elif type == 'Cubi':
                draws.append(curve)
            inc = inc + 1
            ii = 1

        elif type == 'Close': 
            draws.append(';')

    cordonates.append('x' + str(inc) + ' := ' + str(dparse[inc - 1].end.real - OX) + ' * ox;')
    cordonates.append('y' + str(inc) + ' := ' + str(y - dparse[inc - 1].end.imag + y - OY) + ' * oy;')
    draws.append(' z' + str(inc))
    draws.append('; \n')

    return [cordonates, draws, inc]

def buildMp(dirFiles_svg, dirFiles_mp, setfig, origin=None):
    if origin == None:
        OX = 0
        OY = 0
    else: 
        OX = origin[0]
        OY = origin[1]

    if setfig != '-all':
        SET = glob.glob(dirFiles_svg + str(setfig) + '.svg')
    else:
        SET = glob.glob(dirFiles_svg + '*.svg')

    for files in SET:
        with open(files, 'rt') as f:
            tree = ElementTree.parse(f)

        root = tree.getroot()

        lDec = root.attrib['data-dec']
        lWidth = root.attrib['width']
        lHeight = root.attrib['height']

        for path in root.iter():
            d = path.attrib.get('d')
            print(d)
            print('---')
            if d:
                letterD = d
                valueP = parsePath(d, OX, OY)  

                buildFig = Template.format(
                    char       = chr(int(lDec)),
                    keycode    = lDec,
                    width      = lWidth,
                    cordonates = '\n    '.join(valueP[0]),
                    draws      = ''.join(valueP[1]),
                    lenpoints  = valueP[2]
                )
                f = open( dirFiles_mp + lDec + '.mp', 'w')
                f.write(buildFig) 
                f.close()
 
def buildSvg(dirMP, dirOut, setfig):
    if setfig != '-all':
        SET = glob.glob(dirMP + str(setfig) + '.mp')
    else:
        SET = glob.glob(dirMP + '*.mp')

    for mp in SET:
        mpFile = os.path.basename(mp)
        key = os.path.splitext(mpFile)[0]
        subprocess.call(["mpost", "-interaction=batchmode", mp])
        for LOG in glob.glob('*.log'):
            os.remove(LOG)

def buildGlobalMp(dirFiles, dirMP) :
    out = []
    Tmp = '''{In} := {Out};'''

    with open(dirFiles) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    CATEGORIES = data['variables']

    for gvs in CATEGORIES:

        for gv in CATEGORIES[gvs]:
            item = CATEGORIES[gvs][gv]
            if type(item) == OrderedDict:
                IN = '\n% ' +item['description']+ '\n' +item['name']
                OUT = item['value'] + item['unity']
            else:
                IN = gv
                OUT = item 

            Line = Tmp.format(
                       In = IN,
                       Out = OUT,
                    )
            out.append(Line)
        f = open(dirMP, 'w')
        f.write('\n'.join(out)) 
        f.close()

        print('\n'.join(out))

