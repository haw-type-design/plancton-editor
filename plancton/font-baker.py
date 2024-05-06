#/usr/bin/python
# -*- coding: utf-8 -*-


import fontforge
import sys
import json
import os 
import lxml.etree as ET
import psMat

def removeCadra(root, pattern):
    for child in root:
        if child.tag == '{http://www.w3.org/2000/svg}path':
            if child.attrib['style'].startswith(pattern):
                b = child
                root.remove(b)
    ET.dump(root)
    return ET.tostring(root, encoding='utf8', method='xml').decode()

json = json.loads(sys.argv[2].replace("'", '"'))
svg_dir = eval(sys.argv[1])
ex_folder_svg = sys.argv[3]
project = sys.argv[4]



font = fontforge.font()

try: 
    height = 1000 / int(json['font_info']['height'])
except:
    print('no height define in json')

try: 
    font.descent = int(height * int(json['font_info']['descent']))
except:
    print('no descent define in json')

try:
    font.ascent = int(height * int(json['font_info']['ascent']))
except:
    print('no descent define in json')

font.fontname = json['font_info']['font-id']
font.familyname = json['font_info']['font-id']
font.copyright = json['font_info']['author-name']

for g in svg_dir:
    print(g)
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
        try: 
            char.width = int(gwidth * height)
        except:
            char.width = int(gwidth)
            
        try:
            char.importOutlines(out_svg, scale=False)
        except:
            print('glyph ' + str(char.glyphname) + ' failed')
            continue

font.addExtrema()
font.autoHint()
font.generate('static/fonts/exports/'+project+'.ttf')
font.generate('fonts/'+project+'.ttf')