import json
from pprint import pprint


def writeGlobal() :
    out = []
    Tmp = '''{In} := {Out};'''

    with open('global.json') as f:
        data = json.load(f)

    global_variables = data['global_variables']


    for gv in global_variables :
        item = global_variables[gv]

        if type(item) == dict:
            IN = '\n% ' +item['description']+ '\n' +item['name']
            OUT = item['value'] + item['unity']
        else:
            IN = gv
            OUT = global_variables[gv]

        Line = Tmp.format(
                   In = IN,
                   Out = OUT,
                )
        out.append(Line)

    f = open('mpost/global.mp', 'w')
    f.write('\n'.join(out)) 
    f.close()

    print('\n'.join(out))

