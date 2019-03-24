import glob
import sys
import lxml.etree as ElementTree
from svg.path import parse_path

Template = '''
outputtemplate := "%j%c.svg";
ux = 20;
uy = 20;
beginfig({keycode});
    pickup pencircle xscaled 50pt yscaled 50pt rotated 45;
    {cordonates} 
    {draws}
endfig;
end;
'''

def parsePath(path):
    dparse = parse_path(path)
    cordonates = []
    draws = []
    inc = 1
    incD = 0 
    y = 20
    j = ' --'
    for point in dparse:
        if str(point)[0:4] == 'Move':
            if incD > 0:
                cordonates.append('x' + str(inc) + ' = ' + str(dparse[inc - 1].end.real) + 'ux;')
                cordonates.append('y' + str(inc) + ' = ' + str(y - dparse[inc - 1].end.imag + y) + 'uy;')
                draws.append(j)
                draws.append(' z' + str(inc))
                draws.append('; \n')
                inc = inc + 1

            draws.append('draw')
            incD = 1
            ii = 0

        elif str(point)[0:4] == 'Line': 

            cordonates.append('x' + str(inc) + ' = ' + str(point.start.real) + 'ux;')
            cordonates.append('y' + str(inc)+ ' = ' + str(y - point.start.imag + y) + 'uy;')
 
            if ii > 0:
                draws.append(j)

            draws.append(' z' + str(inc))
            inc = inc + 1
            ii = 1

        elif str(point)[0:4] == 'Close': 
            draws.append(';')

    cordonates.append('x' + str(inc) + ' = ' + str(dparse[inc - 1].end.real) + 'ux;')
    cordonates.append('y' + str(inc) + ' = ' + str(y - dparse[inc - 1].end.imag + y) + 'uy;')
    draws.append(j)
    draws.append(' z' + str(inc))
    draws.append('; \n')

    return [cordonates, draws]

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
                buildFig = Template.format(keycode= lDec, cordonates='\n    '.join(valueP[0]), draws=''.join(valueP[1]) )

                f = open('mpost-files/' + lDec + '.mp', 'w')
                f.write(buildFig)  # python will convert \n to os.linesep
                f.close()
                print(buildFig)


def mp2svg():
    print('ss')

if sys.argv[1] == '-mp':
    svg2mpost()
elif sys.argv[1] == '-mp2svg':
    mp2svg()
else:
    print('no arguments')

