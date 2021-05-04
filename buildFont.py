import fontforge 
import glob

font = fontforge.open('.tmp/empty.sfd')
_dir_svg = glob.glob('projects/meta-old-french/output-svg/*.svg')


for svg in _dir_svg:
    key = svg.split("/")[-1].replace('.svg', '')

    letter_char = font.createMappedChar(int(key))
    letter_char.importOutlines(svg)


font.generate('temp.otf')

