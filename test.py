from plancton import Plancton
import plancton.gitManager as gm 

#
# gitm = gm.gitManager()
# gitm.project_path = 'projects/tmp/meta-old-french/'
# gitm.save('.', 'test', 'yess')

branch = '*test'

if branch.startswith('*'):
    print('est la branch courante') 

