import glob
import sys
import os
import subprocess
import lxml.etree as ElementTree
from svg.path import parse_path

Template = '''
% {char}
input ../global;
beginchar({keycode}, {width});
    {cordonates} 
    {draws}
endchar({lenpoints});
end;
'''

def parsePath(path):
    dparse = parse_path(path)
    print(dparse)
    print('----------------------------------------------')
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
                cordonates.append('x' + str(inc) + ' := ' + str(dparse[inc - 1].end.real) + ' * ux;')
                cordonates.append('y' + str(inc) + ' := ' + str(y - dparse[inc - 1].end.imag + y) + ' * uy;')
                # draws.append(line)
                draws.append(' z' + str(inc))
                draws.append('; \n')
                inc = inc + 1

            draws.append('draw')
            incD = 1
            ii = 0

        elif type == 'Line' or type == 'Cubi': 

            cordonates.append('x' + str(inc) + ' := ' + str(point.start.real) + ' * ux;')
            cordonates.append('y' + str(inc)+ ' := ' + str(y - point.start.imag + y) + ' * uy;')
 


            draws.append(' z' + str(inc))
            if type == 'Line':
                draws.append(line)
            elif type == 'Cubi':
                draws.append(curve)
            inc = inc + 1
            ii = 1

        elif type == 'Close': 
            draws.append(';')

    cordonates.append('x' + str(inc) + ' := ' + str(dparse[inc - 1].end.real) + ' * ux;')
    cordonates.append('y' + str(inc) + ' := ' + str(y - dparse[inc - 1].end.imag + y) + ' * uy;')
    # draws.append(line)
    draws.append(' z' + str(inc))
    draws.append('; \n')

    return [cordonates, draws, inc]

def svg2mpost():
    dirFiles = 'input-svg/*.svg'

    for files in glob.glob(dirFiles):
        with open(files, 'rt') as f:
            tree = ElementTree.parse(f)

        root = tree.getroot()

        lDec = root.attrib['data-dec']
        lWidth = root.attrib['width']
        lHeight = root.attrib['height']

        for path in root.iter():
            d = path.attrib.get('d')
            if d:
                letterD = d
                valueP = parsePath(d)  # [0] ) cordonates; [1] draws

                buildFig = Template.format(
                char       = chr(int(lDec)),
                keycode    = lDec,
                width      = lWidth,
                cordonates = '\n    '.join(valueP[0]),
                draws      = ''.join(valueP[1]),
                lenpoints  = valueP[2]
                )

                f = open('mpost/mpost-files/' + lDec + '.mp', 'w')
                f.write(buildFig) 
                f.close()
                print(buildFig)
            
def mp2svg():
    dirMP = 'mpost/mpost-files/*.mp'
    for mp in glob.glob(dirMP):
        mpFile = os.path.basename(mp)
        key = os.path.splitext(mpFile)[0]
        subprocess.call(["mpost", "-interaction=batchmode", mp])
    subprocess.call(["rm", "-rf", "*.log"])

if sys.argv[1] == '-mp':
    svg2mpost()
elif sys.argv[1] == '-mp2svg':
    mp2svg()
elif sys.argv[1] == '-all':
    svg2mpost()
    mp2svg()

