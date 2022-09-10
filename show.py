import sys
from modules import helper

if len(sys.argv) == 2:
    if sys.argv[1] == 'dynamic' or True:
        jsonData = helper.loadJson('dynamicCommands.json')
        for key, value in jsonData.items():
            print(key)

        print(10 * '-')

        for key, value in jsonData.items():
            print(key, value)
