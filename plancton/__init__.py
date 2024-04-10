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
from pathlib import Path


try:
    import fontforge 
except ImportError:
    print('ImportError fontforge')

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
        

    def del_glyph(self, key):
        project_path = self.dir_projects+'/'+self.project
        outsvg = project_path+'/output-svg/'+str(key)+'.svg'
        mp = project_path+'/mpost/mpost-files/'+str(key)+'.mp'

        if os.path.isfile(outsvg):
            os.remove(outsvg)
        if os.path.isfile(mp):
            os.remove(mp)

        return str(key)+' has been deleted !'

    def add_glyph(self, key):
        project_path = self.dir_projects+'/'+self.project
        json_path = project_path+'/'+self.current_json
        inputsvg_path = project_path+'/input-svg/'
        
        if os.path.isfile(project_path+'/mpost/mpost-files/'+str(key)+'.mp'):
            return str(key)+' already exist ! Use ":delete '+str(key)+'" before.'
        else: 
            buildFig = self.mp_template.format(
                char       = chr(int(key)),
                keycode    = key,
                width      = '5',
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
        print(svg_dir)
        print(json)
        
        run_command = "fontforge -script plancton/font-baker.py \""+ str(svg_dir) + "\" \"" + str(json) + "\" \"" + str(ex_folder_svg) + "\" \"" + str(self.project) + "\""
        print(run_command)
        os.system(run_command)

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
        
        
    #########################
    #      ADD PROJECT      #
    #########################


    def newProject(self, new_project_name, new_author, new_author_email, new_license):
        json_info = '{\n"font_info":\n {\n"font-name": "' +new_project_name.replace(" ", "-")+'",\n "font-id": "' +new_project_name.replace(" ", "-")+'",\n"author-name": "' +new_author+'",\n"author-email": "' +new_author_email+'",\n"licence": "' +new_license+'",\n"height": "",\n"descent": "",\n"ascent": ""\n}\n}'
        
        mpost_def = "input ../global;\n\nheight := 13;\nbaseline := 0;\nxHeight := 5;\nascHeight := 11;\ndescHeight := -4;\ncapHeight := 11;\n\nstrokeX := 1u;\nstrokeY := 1u;\nrotation := 45;\n\ngrid = 1;\n\n\ndef beginchar(expr keycode, width)=\n\tbeginfig(keycode);\n\t\tpickup pencircle scaled .2;\n\n\t\tdraw (0 * ux, (descHeight - 2) * uy) -- \n\t\t\t(width * ux, (descHeight - 2) * uy) --\n\t\t\t(width * ux, (ascHeight + 2) * uy) -- \n\t\t\t(0 * ux, (ascHeight + 2) * uy) -- \n\t\t\tcycle scaled 0 withcolor red;\n\n\t\tif grid = 1:\n\t\t\tdefaultscale := .2;\n\t\t\tfor i=0 upto width:\n\t\t\t\tdraw (i*ux, height*uy) -- (i*ux, descHeight*uy) withcolor .3white;\n\t\t\tendfor;\n\t\t\tfor i=descHeight upto (height):\n\t\t\t\tdraw (width*ux, i*uy) -- (0*ux, i*uy) withcolor .3white;\n\t\t\tendfor;\n\t\tfi;\n\t\tpickup pencircle scaled 1;\n\n\t\tif hints = 1:\n\t\t\tdraw (0 * ux, capHeight * uy) -- (width * ux, capHeight * uy)  withcolor (green + blue);\n\t\t\tdraw (0 * ux, ascHeight * uy) -- (width * ux, ascHeight * uy)  withcolor (green + blue);\n\t\t\tdraw (0 * ux, descHeight * uy) -- (width * ux, descHeight * uy)  withcolor (green + blue);\n\t\t\tdraw (0 * ux, baseline * uy) -- (width * ux, baseline * uy)  withcolor green;\n\t\tfi;\n\t\t\n\t\tpickup pencircle xscaled strokeX yscaled strokeY rotated rotation;\n\nenddef;\n\n\ndef endchar(expr lenDots)=\n\tif dot_label = 1:\n\t\tdefaultscale := 3;\n\t\tfor i=1 upto lenDots:\n\t\t\tdotlabels.urt([i]) withcolor blue;\n\t\tendfor;\n\tfi;\nendfig;\nenddef;"
        mpost_global = 'outputformat := "svg";\noutputtemplate := "projects/'+new_project_name.replace(" ", "-")+'/output-svg/%c.svg";\n\n% grid\ngrid := 1;\n\n% dot label\ndot_label := 0;\n\n% hints\nhints := 0;\n\n% unity\nu = 40pt;\nux = 1u;\nuy = 1u;\n'
        
        project_path = self.dir_projects+'/'+new_project_name.replace(" ", "-")
        Path(project_path).mkdir(parents=True, exist_ok=True)
        Path(project_path+'/mpost/mpost-files').mkdir(parents=True, exist_ok=True)
        Path(project_path+'/mpost/def.mp').touch(exist_ok=True)
        Path(project_path+'/mpost/global.mp').touch(exist_ok=True)
        ex_folder = project_path+'/fonts/test'
        Path(ex_folder).mkdir(parents=True, exist_ok=True)
        ex_folder_svg = self.dir_projects+'/'+new_project_name.replace(" ", "-")+'/fonts/test/svg'
        Path(ex_folder_svg).mkdir(parents=True, exist_ok=True)
        json_path = project_path+'/'+self.current_json
        if not os.path.exists(json_path):
            Path(json_path).touch()
            with open(json_path, "w") as file:
                file.write(json_info)
                
        with open(Path(project_path+'/mpost/def.mp'), "w") as file:
            file.write(mpost_def)
            
        with open(Path(project_path+'/mpost/global.mp'), "w") as file:
            file.write(mpost_global)
                