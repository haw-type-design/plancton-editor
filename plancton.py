import json
from collections import OrderedDict
import glob
import os
import subprocess
import lxml.etree as ElementTree
from svg.path import parse_path

Template = '''
% {char}
input ../def;
beginchar({keycode}, {width});
    {cordonates} 
    {draws}
endchar({lenpoints});
end;
'''

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
    print('---------> BuildMp ')
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
        # print(setfig)
    else:
        SET = glob.glob(dirMP + '*.mp')

    for mp in SET:
        mpFile = os.path.basename(mp)
        key = os.path.splitext(mpFile)[0]
        subprocess.call(["mpost", "-interaction=batchmode", mp])
        subprocess.call(["rm", "-f", "*.log"])

def buildGlobalMp(dirFiles, dirMP) :
    out = []
    Tmp = '''{In} := {Out};'''

    with open(dirFiles) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    CATEGORIES = data['variables']
    # print(data)

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

