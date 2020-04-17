import argparse, glob, json, pprint

_DIRPROJ_ = 'projects'

class Utility:
    def loadJson(dirFiles):
        with open(dirFiles, 'r') as f:
            data = json.load(f):
        return data

    def writeJson(path_file, data):
        file = open(path_file, 'w')
        file.write(json.dumps(data, ensure_ascii=False)) 

        file.close()

    def stop():
        stop()
    
class 


class Interacive:

    def new_or_modify():

        print('\n [N] Create a new font project. ')
        print(' [M] Modify an existing font project. \n')

        def input_direction():
            r = input(' Type [N] or  [M] ? : ')
            if r == 'M' or r == 'm':
                mdf = Modify
                mdf.choose()
                mdf.global_file()
            elif r == 'N' or r == 'n':
                print('new project')
            else:
                print('\n Input value is wrong.\n')
                input_direction()

        input_direction()

class Modify:

    def choose():
        global project
        ps = glob.glob(_DIRPROJ_ + '/*/')
        pns = [] 
        i = 0
        print('\n-------------------')
        print(' List of projects : ')
        print('-------------------\n')

        for p in ps:
            l = p.split('/')
            print('     ['+str(i)+'] - ' + l[1])
            pns.append([l[1], p])
            i = i + 1

        num_name=int(input('\n Tape the number of the project: '))
        
        if type(num_name == int):
            if pns[num_name]:
                project = [num_name, pns[num_name][1], pns[num_name][0]] 
                return project
        else:
            num_name=int(input('\n Tape the number of the project: '))
    
    def global_file(pname='false'):

        if pname == 'false':
            pname = project[2]
        global_path = _DIRPROJ_ + '/' + pname + '/global.json'
        data = Utility.loadJson(global_path)

        print('\n----------------------------')
        print(' Change values of ' + pname + ' :')
        print('----------------------------\n')

        if data['font_info']:
            i = 0
            d = []
            for item in data['font_info']:
                print("     [{}] {} =  {}".format(i,item,data['font_info'][item]))
                d.append(item)
                i = i + 1
            num=int(input('\n Tape the number of the key : '))

            if type(num) == int:

                def change_value():
                    r = input('\n change ' + d[num] + ' : ')  
                    data_type = type(data['font_info'][d[num]])
                    if type(r) == data_type:
                        data['font_info'][d[num]] = r
                        Utility.writeJson(global_path, data)
                        continu = input('\n Do you want to continue the changes [Y/N] ')
                        if continu == 'N' or continu == 'n':
                            print('Byyyyyy !!!')
                            Utility.stop()
                        else:
                            Modify.global_file(pname)
                    else:
                        print(' The value must be a ' + data_type )
                        change_value()

                change_value()
        else: 
            print('font info is missing')


def Main():
    parser = argparse.ArgumentParser(description="[Plancton Editor Manager] by Luuse")
    parser.add_argument("-n", "--new-project", help="Create a new font project.", action="store_true")
    parser.add_argument("-m", "--modify-project", help="Modify an existing font project.", action="store_true")
    parser.add_argument("-i", "--interactive", help="Interactive mode.", action="store_true")
    args = parser.parse_args()

    if args.interactive:
        Interacive.new_or_modify()

    if args.new_project:
        print('new project')
    elif args.modify_project: 
        print(' Modify an existing font project')
        print(args.modify_project)




if __name__ == '__main__':

    Main()
