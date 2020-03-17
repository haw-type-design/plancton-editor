import re, json, os, sys 
from slugify import slugify

class projectInfo:
    def __init__(self, arg):
        self.msg = arg

    def name(): 
        global name
        name=input('Project name : ')
        print('     > > > project name is ' + name)
        return name
    
    def author(): 
        global author
        author=input('Author : ')
        print('     > > > author is ' + author)
        return author
    
    def author_email(): 
        global author_email
        author_email=input('Author email: ')
        print('     > > > author email is ' + author_email)
        return author_email
    
    def licence(): 
        global author_email
        author_email=input('Licence Project: ')
        print('     > > > Licence is ' + author_email)
        return author_email
    
    def ascent(): 
        global ascent
        ascent=int(input('Ascent value: '))
        
        if type(ascent) == int :
            print('     > > > ascent value ' + str(ascent))
            return ascent
        else: 
            print('     > > > use number only !')
            projectInfo.ascent()
    
    def descent(): 
        global descent
        descent=int(input('Descent value: ')) 
        if type(descent) == int :
            print('     > > > descent value ' + str(descent))
            return descent
        else: 
            print('     > > > use number only !')
            projectInfo.descent()

    def x_height(): 
        global descent
        descent=int(input(' x height value: ')) 
        if type(descent) == int :
            print('     > > > x height ' + str(descent))
            return descent
        else: 
            print('     > > > use number only !')
            projectInfo.descent()

# fontInfo = {}
# fontInfo['name'] = projectInfo.name()
# fontInfo['name_slug'] = slugify(data['name'])
# fontInfo['author'] = projectInfo.author()
# fontInfo['author_email'] = projectInfo.author_email()
# fontInfo['licence'] = projectInfo.licence()
# fontInfo['ascent'] = projectInfo.ascent()
# fontInfo['descent'] = projectInfo.descent()
# fontInfo['x_height'] = projectInfo.x_height()

fontInfo = {}
fontInfo['name'] = 'meta old' 
fontInfo['name_slug'] = 'meta-old' 
fontInfo['author'] = 'luuse' 
fontInfo['author_email'] = 'luuse@luuse.io' 
fontInfo['licence'] = 'ofl' 
fontInfo['ascent'] = 15 
fontInfo['descent'] = 5 
fontInfo['x_height'] = 10 

defFile = open( 'tpl/def.mp.tpl', 'r')

buildDef = defFile.read().format(
        height = (fontInfo['ascent'] + fontInfo['descent']),
        x_height = fontInfo['x_height'],
        ascent = fontInfo['ascent'],
        descent = fontInfo['descent']
        )

if not os.path.exists('projects/' + fontInfo['name_slug']):
    os.mkdir('projects/' + fontInfo['name_slug'])

os.mkdir('projects/' + fontInfo['name_slug'] + '/mpost')
os.mkdir('projects/' + fontInfo['name_slug'] + '/fonts')
os.mkdir('projects/' + fontInfo['name_slug'] + '/input-svg')
os.mkdir('projects/' + fontInfo['name_slug'] + '/output-svg')


# defFile = open( fontInfo + '')

# print(buildDef)
# print(json_data)
