from svg.path import parse_path

d = 'M 4,1 V 22 M 5,1 v 21 m 5,-21 3,1 2,2 1,2 v 2 l -1,2 -2,1 -3,1 m -5,0 h 5 l 4,-1 2,-1 1,-2 V 6 L 16,4 14,2 10,1 H 2 3 L 4,2 M 4,21 3,22 H 2 7 6 L 5,21 m 6,-9 1,3 1,2 2,3 2,2 -3,-2 -2,-3 -1,-2 -1,-3'

y = 40
def parsePath(path):
    dparse = parse_path(path)
    print(dparse)
    cordonates = []
    draws = []
    inc = 0
    incD = 0 
    for point in dparse:
        if str(point)[0:4] == 'Move':
            if incD > 0:
                cordonates.append('x' + str(inc) + ' = ' + str(dparse[inc].end.real) + 'ux;')
                cordonates.append('y' + str(inc) + ' = ' + str(dparse[inc].end.imag) + 'uy;')
                draws.append(' --')
                draws.append(' z' + str(inc))
                draws.append('; \n')
                inc = inc + 1

            draws.append('draw')
            incD = 1
            ii = 0

        elif str(point)[0:4] == 'Line': 

            cordonates.append('x' + str(inc) + ' = ' + str(point.start.real) + 'ux;')
            cordonates.append('y' + str(inc)+ ' = ' + str(point.start.imag) + 'uy;')
            # cordonates.append('x' + str(inc + 1) + ' = ' + str(point.end.real) + 'ux;')
            # cordonates.append('y' + str(inc + 1)+ ' = ' + str(point.end.imag) + 'uy;')
 
            if ii > 0:
                draws.append(' --')

            draws.append(' z' + str(inc))
            inc = inc + 1
            # draws.append(' --')
            # draws.append(' z' + str(inc + 1))
            
            # inc = inc + 1
            ii = 1
        elif str(point)[0:4] == 'Close': 
            draws.append(';')
    cordonates.append('x' + str(inc) + ' = ' + str(dparse[inc].end.real) + 'ux;')
    cordonates.append('y' + str(inc) + ' = ' + str(dparse[inc].end.imag) + 'uy;')
    draws.append(' --')
    draws.append(' z' + str(inc))
    draws.append('; \n')

    return [cordonates, draws]

valueP = parsePath(d)  # [0] ) cordonates; [1] draws


buildFig = '''
outputtemplate := "%j%c.svg";
ux = 1;
uy = 1;
beginfig({keycode}):
    {cordonates} 
    {draws}
endfig;

end;
'''.format(keycode= 1, cordonates='\n    '.join(valueP[0]), draws=''.join(valueP[1]) )

f = open('a.mp', 'w')
f.write(buildFig)  # python will convert \n to os.linesep
f.close()
print(buildFig)
