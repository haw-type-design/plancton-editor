import lib.svg2mpost as s2m


# s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', 65, [5,2])
s2m.buildMp('files/input-svg/', 'files/mpost/mpost-files/', '-all', [0, 18])
s2m.buildSvg('files/mpost/mpost-files/', '-all') 
