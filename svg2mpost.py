from svg.path import parse_path

d = 'M 15,5 V 22 M 15,11 13,9 11,8 H 8 L 6,9 4,11 3,14 v 2 l 1,3 2,2 2,1 h 3 l 2,-1 2,-2'


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
                draws.append('; \n')

            draws.append('draw')
            incD = 1
            inc = 0

        elif str(point)[0:4] == 'Line': 

            cordonates.append('x' + str(inc) + ' = ' + str(point.start.real) + 'ux;')
            cordonates.append('y' + str(inc)+ ' = ' + str(point.start.imag) + 'uy;')
            cordonates.append('x' + str(inc + 1) + ' = ' + str(point.end.real) + 'ux;')
            cordonates.append('y' + str(inc + 1)+ ' = ' + str(point.end.imag) + 'uy;')
 
            if inc > 0:
                draws.append(' --')

            draws.append(' z' + str(inc))
            draws.append(' --')
            draws.append(' z' + str(inc + 1))
            
            inc = inc + 2
        elif str(point)[0:4] == 'Close': 
            draws.append(';')

    return [cordonates, draws]

valueP = parsePath(d)  # [0] ) cordonates; [1] draws

# print(''.join(valueP[1]))

''.join(valueP[0])
# for v in valueP[0]:
#     print(v)
#     



buildFig = '''
outputtemplate := "%j%c.svg";
ux = 1;
uy = 1;
beginfig({keycode}):
    {cordonates} 
    {draws};
endfig;

end;
'''.format(keycode= 1, cordonates='\n    '.join(valueP[0]), draws=''.join(valueP[1]) )

f = open('a.mp', 'w')
f.write(buildFig)  # python will convert \n to os.linesep
f.close()
print(buildFig)
