import os

import urllib.parse
import urllib.request

if os.path.isfile('config_local.py'):
    import config_local as config
else:
    import config

class tquest():
    def __init__(self):
        self.toSend = ''

    def command(self, username, command):
        import urllib.request
        with urllib.request.urlopen(config.TQUEST_URL) as response:
            self.toSend = response.read()
        values = {
            'username':username,
            'command':command
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(config.TQUEST_URL, data)
        with urllib.request.urlopen(req) as response:
            self.toSend = response.read().strip().decode('utf-8')
        #self.toSend = 'Sorry @' + username + ', i could not find the command "' + username + '"'
