#/usr/bin/python
# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
import glob
import os
import subprocess
import lxml.etree as ET
from svgpathtools import svg2paths, parse_path
import svgwrite
import re 
import fontforge 
import math       

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
        self.project = ''
        self.current_json = 'current.json'

    def read_json(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    # C O N V E R T - M P -> S V G
    def adjust_viewbox(f_svg):
        tree = ET.parse(f_svg)
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
        tree.write(open(f_svg, 'wb'))

    def build_svg(self, key):
        project_path = self.dir_projects+'/'+self.project
        mp_path = project_path+'/mpost/mpost-files/'
        svg_path = project_path+'/output-svg/'
        if not os.path.exists(svg_path):
            os.makedirs(svg_path)

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
            Plancton.adjust_viewbox(svg)
        
        print('--------------------------------------')
        print('--------------------------------------')
        print(mp_path)
        print('--------------------------------------')
        print('--------------------------------------')

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
        json_path = project_path+'/'+self.current_json
        inputsvg_path = project_path+'/input-svg/'
        
        if os.path.isfile(inputsvg_path + str(key) + '.svg'):
            return str(key)+' already exist ! Use ":delete '+str(key)+'" before.'
        else: 
            json = Plancton.read_json(json_path)
            height = json['font_info']['height']
            width = int(int(height)/2) 

            svg = svgwrite.Drawing(str(key) + '.svg', size=(width, height))
            svg.viewbox(0, 0, width, height)
            svg.saveas(project_path+'/input-svg/'+str(key)+'.svg')
            
            buildFig = self.mp_template.format(
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

    #########################
    # S V G   T O   F O N T #
    #########################
    def svg_to_font(self):

        def removeCadra(root, pattern):
            for child in root:
                if child.tag == '{http://www.w3.org/2000/svg}path':
                    if child.attrib['style'].startswith(pattern):
                        b = child
                        root.remove(b)
            ET.dump(root)
            return ET.tostring(root, encoding='utf8', method='xml').decode()

        # Build new directory
        project_path = self.dir_projects+'/'+self.project
        json_path = project_path+'/'+self.current_json
        json = Plancton.read_json(json_path)
        ex_folder = project_path+'/fonts/test/'
        ex_folder_svg = project_path+'/fonts/test/svg/'

        if not os.path.exists(ex_folder):
            os.mkdir(ex_folder)
        if not os.path.exists(ex_folder_svg):
            os.mkdir(ex_folder_svg)

        svg_dir = glob.glob(project_path+'/output-svg/*.svg')
        # svg_dir = glob.glob(ex_folder_svg+'*.svg')

        font = fontforge.font()
        height = 1000 / int(json['font_info']['height'])
        font.descent = height * int(json['font_info']['descent'])
        font.ascent = height * int(json['font_info']['ascent'])
        font.fontname = json['font_info']['font-id']
        font.familyname = json['font_info']['font-id']
        font.copyright = json['font_info']['author-name']

        for g in svg_dir:
            gkey = os.path.basename(g).replace('.svg', '')
            if gkey.isdigit() == True:
                with open(g, 'rb') as gp:
                    treeLet = ET.parse(gp)
                rootLet = treeLet.getroot()
                gclean = removeCadra(rootLet, 'stroke:rgb(100.000000%,0.000000%,0.000000%);')
                out_svg = ex_folder_svg+gkey+'.svg' 
                f = open(ex_folder_svg+gkey+'.svg', 'w')
                f.write(gclean) 
                f.close()
                gwidth = float(rootLet.get('width'))
                gheight = rootLet.get('height')
                print(int(gwidth), '\n', gheight)
                print('\n----------------------\n', gkey, '\n----------------------\n' )

                char = font.createChar(int(gkey))
                char.width = int(gwidth * 1.9)

                try:
                    char.importOutlines(out_svg).simplify().handle_eraser()
                except:
                    print('glyph failed')
                    continue

        font.generate('static/fonts/exports/'+self.project+'.otf')

    def build_global_mp(self):
        dirMP = self.dir_projects+'/'+self.project+'/mpost/global.mp' 
        dirFiles = self.dir_projects+'/'+self.project+'/'+self.current_json
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


    def searchKeysByVal(self,dict, byVal):
        keysList = []
        itemsList = dict.items()
        for item in itemsList:
            print(item)
        #     if item[1] == byVal:
        #         keysList.append(item[0])
        # return keysList

    def getVersions(self):

        def getInfo(v):
            with open(v) as f:
                data = json.load(f, object_pairs_hook=OrderedDict)
            return  data



        versions = glob.glob(self.dir_projects+'/'+self.project+'/versions/*.json')

        out = {}

        # for v in versions: out.append(getInfo(v))
        for v in versions:
            name = getInfo(v)['font_info']['version']
            out[name] = {'name': name, 'path': v} 
        
        print(out)
        return out

    def switchVersion(self, current_version, select_version):

        versions = self.getVersions()
        




