import os, sys, unittest
if sys.version_info[0] == 2:
    import imp
else:
    if sys.version_info[1] < 5:
        from importlib.machinery import SourceFileLoader
    else:
        import importlib.util

PATH = os.path.abspath(__file__).replace('\\','/')
DIS_PATH = PATH.split('/')
IGNORE = ['request_client', 'meta','seaborn_table','SeabornTable']

i = None
for i in range(len(DIS_PATH)):
    if DIS_PATH[-i]=='games':
        depth = i

DEPTH = depth

SUPER_PATH = '/'.join(DIS_PATH[:-DEPTH])
SISTER_PATHS = [SUPER_PATH + '/' + i for i in os.listdir(SUPER_PATH)
               if '.' not in i and i != DIS_PATH[-DEPTH]]

def main():
    print("Searching directory: %s"%SUPER_PATH)
    print("Found paths:")
    testmodules = []
    for dir_ in SISTER_PATHS:
        if os.path.isdir(dir_+'/test') and os.path.split(dir_)[1] not in IGNORE:
            testmodules += [dir_ + '/test/' + i#.replace('.py','')
                            for i in os.listdir(dir_+'/test')\
                            if 'test' in i and '.pyc' not in i]
            print(dir_)

    modules = []
    for path in testmodules:
        if sys.version_info[0]==2:
            modules += [imp.load_source('',path)]
        else:
            if sys.version_info[1] < 5:
                modules += [SourceFileLoader("",path).load_module()]
            else:
                spec = importlib.spec_from_file_location('',path)
                modules += [importlib.util.spec_from_file_location(spec)]
                spec.loader.exec_module(modules[-1])
        print("Found test:\t\t\t%s"%path)
    suite = unittest.TestSuite()

    for test in testmodules:
        print("Loading tests in:\t%s"%test)
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))

    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()
