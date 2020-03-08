import re, json

class projectInfo:
    def __init__(self, arg):
        self.msg = arg

    def name(): 
        global name
        name=input('Project name : ')
        if re.match(r'^\w+$', name):
            print('     > > > project name is ' + name)

            return name
        else: 
            print('     > > > invalid character !')
            projectInfo.name()
    
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

data = {}
data['name'] = projectInfo.name()
data['author'] = projectInfo.author()
data['author_email'] = projectInfo.author_email()
data['licence'] = projectInfo.licence()
data['ascent'] = projectInfo.ascent()
data['descent'] = projectInfo.descent()
data['x_height'] = projectInfo.x_height()
json_data = json.dumps(data)

print(json_data)


