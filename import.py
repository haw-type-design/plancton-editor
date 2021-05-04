#/usr/bin/env python2

import fontforge
import glob
import sys
import lxml.etree as et 
import psMat

# FontName = sys.argv[1]
# yTranslate = sys.argv[2]
PATH_ = 'bac-a-sable/output-svg/'
SVG_DIR = glob.glob(PATH_+'*.svg')
# font = fontforge.open('temp/empty.sfd')
font = fontforge.font()
compositeChar = [192, 193, 194, 195, 196, 199, 200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 217, 218, 219, 220, 224, 225, 226, 227, 231, 232, 233, 234, 235, 236, 237, 238, 239, 242, 243, 244, 249, 250, 251, 252, 350, 351]

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

for glyph in SVG_DIR:
    print(glyph)
    with open(glyph, 'rt') as f:
        treeLet = et.parse(f)
    rootLet = treeLet.getroot()
    chasse = float(rootLet.get('width'))

    letter = glyph.split("/")[-1].replace(".svg", "")
    print('dec : ' + letter + '| width : ' + str(chasse))

    gclean = removeCadra(glyph, 'stroke:rgb(100.000000%,0.000000%,0.000000%);')
    svg_clean = PATH_+'clean/'+letter+'.svg' 
    f = open(svg_clean, 'w')
    f.write(str(gclean)) 
    f.close()
    print('STARTTT')
    letter_char = font.createChar(int(letter))
    try:
        test = letter_char.importOutlines(svg_clean)
    except:
        print('noooooo')

    print('ENDDDD')
    # letter_char.width = int(chasse)

# for letter_comp in compositeChar:
#     glyphAcc = font.createChar(letter_comp)
#     glyphAcc.build()
#     print('-----')
#     print(letter_comp)
#     print('-----')
#     glyphAcc.left_side_bearing = glyphAcc.right_side_bearing = (glyphAcc.left_side_bearing + glyphAcc.right_side_bearing)/2



# espace = font.createChar(32)
# espace.width = font['f'].width
# espacefine = font.createChar(8201)
# espacefine.width = int(font['f'].width / 3)
# font.em = 1000

# trs = psMat.translate(0, int(yTranslate)) 
# font.selection.all()
# font.transform(trs)

font.selection.all()
font.correctDirection()
font.removeOverlap()
font.simplify()
font.round()
# font.fontname = FontName
font.familyname = 'fontName'
font.generate('FINAL.otf')
