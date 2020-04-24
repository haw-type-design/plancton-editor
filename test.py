from svgpathtools import svg2paths, parse_path
import lxml.etree as ET

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



adjust_viewbox("106.svg")
