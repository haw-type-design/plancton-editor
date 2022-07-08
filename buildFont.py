import fontforge 
import glob

font = fontforge.open('.tmp/empty.sfd')
_dir_svg = glob.glob('projects/noto/output-svg/*.svg')


for svg in _dir_svg:
    key = svg.split("/")[-1].replace('.svg', '')

    letter_char = font.createMappedChar(int(key))

    try:
    	letter_char.importOutlines(svg)
	except:
    	pass
    


font.generate('temp.otf')

