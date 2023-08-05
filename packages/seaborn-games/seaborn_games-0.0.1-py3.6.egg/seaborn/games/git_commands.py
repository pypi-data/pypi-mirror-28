import os, sys
from subprocess import *

PATH = os.getcwd().replace('\\','/')
DIS_PATH = PATH.split('/')

depth = None
for i in range(len(DIS_PATH)):
    if DIS_PATH[-i]=='seaborn':
        depth = i

DEPTH = depth - 1

SUPER_PATH = '/'.join(DIS_PATH[:-DEPTH])
SISTER_PATHS = [SUPER_PATH + '/' + i for i in os.listdir(SUPER_PATH)
               if '.' not in i and not 'game' in i.lower()]

def seaborn_status(echo=True, *args):
    result = check_output('git status', shell=True)
    if echo:
        print(result.decode('utf-8'))
    return result

def seaborn_commit(*args):
    commit = 'not staged' in seaborn_status(False).decode('utf-8')
    if commit:
        print(check_output('git add -A', shell=True).decode('utf-8'))
        print(
            check_output(
                'git commit -m "%s"' % args[0], shell=True
            ).decode('utf-8'))
    else:
        print('Not committing: Everything up-to-date\n')
    return commit

def seaborn_push(*args):
    push = 'up-to-date' in seaborn_status(False).decode('utf-8')
    if push:
        print(check_output('git push', shell=True).decode('utf-8'))
    else:
        print('Not pushing: Not up-to-date')

def seaborn_pull(*args):
    mstr = '*master' in check_output('git branch').decode('utf-8')
    pull = 'up-to-date' in seaborn_status(False).decode('utf-8')
    if mstr and pull:
        print(check_output('git pull origin master').decode('utf-8'))
    else:
        print(check_output('git fetch origin master').decode('utf-8'))

FUNCS = {'status':seaborn_status,
         'commit':seaborn_commit,
         'push':seaborn_push,
         'pull':seaborn_pull}

def dir_iter(func_name,*args):
    func_iter(func_name)(*args)

def func_iter(func_name):
    func = FUNCS[func_name.replace('seaborn_','')]
    def ret(*args):
        for path in SISTER_PATHS:
            os.chdir(path)
            print('\n\n'+func_name+'-\t'+path)
            try:
                func(*args)
            except BaseException as e:
                pass
    return ret

iter_status = func_iter('status')
iter_commit = func_iter('commit')
iter_push = func_iter('push')
iter_pull = func_iter('pull')


if __name__ == '__main__':
    dir_iter(sys.argv[1], sys.argv[2:])