import sys
import helper

if len(sys.argv) == 2:
    if sys.argv[1] == 'dynamic' or True:
        dict = helper.loadJson('dynamicCommands.json')
        for key, value in dict.items():
            print(key)

        print(10*'-')

        for key, value in dict.items():
            print(key, value)