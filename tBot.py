import re
from time import sleep
import socket
import time
import os
import shortTermMemory
import helper


if os.path.isfile('config_local.py'):
    import config_local as config
else:
    import config

#http://www.twitchapps.com/tmi/
#http://dev.twitch.tv/
#https://help.twitch.tv/customer/de/portal/articles/1302780-twitch-irc
#https://www.twitch.tv/kraken/oauth2/clients
#http://stackoverflow.com/questions/33049383/twitch-irc-chat-bot-successfully-connects-but-does-not-detect-commands

HOST = "irc.twitch.tv"
PORT = 6667
NICK = config.NICK
PASS = config.PASS
CHAN = config.CHAN
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
SOCKET_TIMEOUT = 2.0

class tBot(object):
    def __init__(self):
        self.startTime = time.time()
        self.sock = socket.socket()
        self.sock.settimeout(SOCKET_TIMEOUT)
        self.timeoutCounter = 0
        self.connected = False
        self.die = False

        self.myMasters = {'timkalation', 'bison_42'}

        self.mySubMasters = ['tomblex', 'Racesore', 'Plantprogrammer']
        self.mySubMastersFile = 'mySubMasters.json'
        mySubMastersTmp = helper.loadJson(self.mySubMastersFile)
        if mySubMastersTmp is not None:
           self.mySubMasters = mySubMastersTmp

        self.revivedCounter = 0

        self.dynamicCommandsFile = 'dynamicCommands.json'
        self.dynamicCommands = {}
        self.chatMemory = shortTermMemory.shortTermMemory()
        self.timerMemory = shortTermMemory.shortTermMemory()

        self.isSilent = config.START_SILENT
        self.matchList = []

        dynamicCommandsTmp = helper.loadJson(self.dynamicCommandsFile)
        if dynamicCommandsTmp is not None:
           self.dynamicCommands = dynamicCommandsTmp

        self.userGreetingsFile = 'userGreetings.json'
        self.userGreetings = {}
        userGreetingsTmp = helper.loadJson(self.userGreetingsFile)
        if userGreetingsTmp is not None:
           self.userGreetings = userGreetingsTmp

        self.usersInChatLastRefresh = 0
        self.usersInChat = set()

        self.EXECUTOR_STATE_DEAD = 0
        self.EXECUTOR_STATE_OK = 1
        self.EXECUTOR_STATE_EMPTY = 2


    def checkMaster(self, username, message=''):
        if username in self.myMasters:
            return True
        else:
            if message == '':
                self.chat('@' + username + ' your kung fu is not strong enough!')
            else:
                self.chat(message)
            return False

    def checkSubMaster(self, username, message='', checkMastersToo=True):
        if checkMastersToo and username in self.myMasters:
            return True

        if username in self.mySubMasters:
            return True
        else:
            if message == '':
                self.chat('@' + username + ' your kung fu is not strong enough!')
            else:
                self.chat(message)
            return False

    def commands(self, username, message, messageLower):
        chatName = '@' + username

        if "!test" == messageLower:
            self.chat("HAMSTER!")
        #elif '!lupfer' == messageLower:
        #    self.chat('lupfe die lupf hupf ¯\_(ツ)_/¯')
        #elif '!deckel' == messageLower:
        #    self.chat("!dackel")
        #elif '!woher' == messageLower:
        #    self.chat("aus dem meer")
        #elif '!wohin' == messageLower:
        #    self.chat("ins TOR natürlich!")
        #elif '!wovon' == messageLower:
        #    self.chat("purer skill!!1!")
        #elif '!wann' == messageLower:
        #    self.chat("bis dann o/")
        elif '!wurm' == messageLower:
            self.chat("~~~~~~~~~~~~~~~~~~~~~~~~O<")
        elif '!wasstimmtdennmitdirnicht' == messageLower:
            helper.realitycheck(self)
        elif '!hilfe' == message or '!help' == messageLower:
            self.chat("help your self :P")
        elif '!wassindhamster' == messageLower or '!hamster' == messageLower:
            helper.explainHamster(self)
        elif '!go' == messageLower:
            self.chat("@timkalation: GO GO TIM TIM GO GO!")
        elif '!burn' == messageLower:
            self.chat('🔥'*10)
        elif '!!myrank' == messageLower or '!!wutcoins' == messageLower:
            self.chat('!wutcoins')
        elif '!silence' == messageLower:
            if self.checkMaster(username):
                if self.isSilent:
                    self.isSilent = False
                    self.chat(chatName + ' deactivating stealth-mode')
                else:
                    self.chat(chatName + ' I am going to stealth-mode now!')
                    self.isSilent = True
        elif '!kill' == messageLower:
            if self.checkMaster(username):
                self.isSilent = False
                self.chat('live long and prosper 🖖')
                self.die = True
                self.connected = False
        elif '!alive' == messageLower:
            secondsAlive = time.time() - self.startTime
            self.chat('ich bin seit {} sekunden / {} am leben und wurde {}x wiederbelebt'.format(secondsAlive, helper.getReadableTime(secondsAlive), self.revivedCounter))
        elif '!takebluepill' == messageLower or '!bluepill' == messageLower:
            if self.checkSubMaster(username):
                self.chat('i will forget everything...')
                self.chatMemory.clean(True)
                self.timerMemory.clean(True)
        elif messageLower.startswith('!wetten'):
            if not hasattr(self, 'wette'):
                import iBet
                self.wette = iBet.iBet(self)
            self.wette.commands(username, message, messageLower)
        elif message.startswith('!addGreeting'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) < 4:
                    self.chat(chatName + ' this is wrong -.- syntax: username triggerOn(* for default) greetingTEXT')
                else:
                    _userName = cmdParts[1]
                    _triggerOn = cmdParts[2]
                    if (_triggerOn[0] == '!'):
                        self.chat(chatName + ' this is wrong! commands with "!" NOT allowed!!1!')
                        return

                    _text = ' '.join(cmdParts[3:])
                    if _userName in self.userGreetings:
                        self.chat(chatName + ' i will change my greeting for "' + _userName + '"')
                    else:
                        self.chat(chatName + ' i added "' + _userName + '" to my greeting log!')
                    self.userGreetings[_userName] = {'triggerOn':_triggerOn, 'text':_text}
                    helper.saveJson(self.userGreetingsFile, self.userGreetings)

        elif messageLower.startswith('!match'):
            if messageLower == '!match':
                if username in self.matchList:
                    self.chat(chatName + ' du bist schon in der liste an Platz ' + str(self.matchList.index(username) + 1))
                else:
                    self.matchList.append(username)
                    self.chat(chatName + ' du bist jetzt in der liste an Platz ' + str(self.matchList.index(username) + 1))
            elif messageLower == '!matchclear':
                if self.checkMaster(username):
                    self.matchList = []
                    self.chat(chatName + ' match liste wurde gelöscht!')
            elif messageLower == '!matchlist':
                finalStr = ''
                index = 1
                for player in self.matchList:
                    finalStr += '{}. {}, '.format(index, player)
                    index += 1
                self.chat('Die Matchreihenfolge lautet wie folgt: ' + finalStr)

        elif messageLower.startswith('!!submaster'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) < 2:
                    self.chat(chatName + ' this is wrong -.-')
                cmdKey = cmdParts[1]
                if len(cmdParts) == 2 and cmdKey == 'list':
                    listOfAllSubMasters = ', '.join(self.mySubMasters)
                    self.chat(listOfAllSubMasters)
                elif len(cmdParts) == 3:
                    newSubMasterName = cmdParts[2]
                    if cmdKey == 'add':
                        self.mySubMasters.add(newSubMasterName)
                        helper.saveJson(self.mySubMastersFile, self.mySubMasters)
                        self.chat('added "' + newSubMasterName + '" as my new sub master!')
                    elif cmdKey == 'del':
                        self.mySubMasters.add(newSubMasterName)
                        helper.saveJson(self.mySubMastersFile, self.mySubMasters)
                        self.chat('removed "' + newSubMasterName + '" as sub master!')
                    else:
                        self.chat('WRONG COMMAND  "' + cmdKey + '"')

        elif message.startswith('!!add'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) < 3:
                    self.chat(chatName + ' this is wrong -.-')
                else:
                    cmdKey = cmdParts[1]
                    cmdText = ' '.join(cmdParts[2:])
                    if cmdKey in self.dynamicCommands:
                        self.chat(chatName + ' i will change my quest for "' + cmdKey + '"')
                    else:
                        self.chat(chatName + ' i added "' + cmdKey + '" to my quest log!')
                    self.dynamicCommands[cmdKey] = cmdText
                    helper.saveJson(self.dynamicCommandsFile, self.dynamicCommands)

        elif message.startswith('!!del'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) != 2:
                    self.chat(chatName + ' this is wrong -.-')
                else:
                    cmdKey = cmdParts[1]
                    if cmdKey not in self.dynamicCommands:
                        self.chat('sorry ' + chatName + ', i dont have "' + cmdKey + '" in my quest log... :(')
                    else:
                        self.chat(chatName + ' i will drop my quest for "' + cmdKey + '"')
                        del self.dynamicCommands[cmdKey]
                        helper.saveJson(self.dynamicCommandsFile, self.dynamicCommands)

        elif message in self.dynamicCommands:
            self.chat(self.dynamicCommands[message])

    def main_loop(self):
        try:
            self.sock.connect((HOST, PORT))
            self.sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
            self.sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
            self.sock.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
            self.connected = True
            self.chat('hallo alle o/')
        except Exception as ex:
            self.connected = False
            print('main_loop 1:', ex)

        while self.connected:
            try:
                self.getUsers()
                if self.executor() == self.EXECUTOR_STATE_DEAD:
                    helper.log('main_loop 2: EXECUTOR FAILED!')
                    break

            except Exception as ex:
                self.connected = False
                print('main_loop 3:', ex)

            sleep(0.1)

        helper.log('PASSED AWAY')

    def executor(self):
        response = None
        try:
            received = self.sock.recv(2048)
            response = received.decode("utf-8")
            self.timeoutCounter = 0
        except socket.timeout:
            #helper.log('timeout')
            self.timeoutCounter += 1
        except Exception as ex:
            self.connected = False
            helper.log('FATAL recv ERROR: ' + str(ex))

        if self.timeoutCounter >= 400:
            helper.log('timeoutCounter ERROR: ' + str(self.timeoutCounter))
            self.connected = False
            return self.EXECUTOR_STATE_DEAD

        if response is None:
            return  self.EXECUTOR_STATE_EMPTY

        if response == "PING :tmi.twitch.tv\r\n":
            self.sock.send("PONG :tmi.twitch.tv\r\n".encode())
            helper.log("PONG")
        else:
            username = ''
            message = ''
            try:
                #'NoneType' object has no attribute 'group'
                username = re.search(r"\w+", response).group(0)
                message = CHAT_MSG.sub("", response)
            except Exception as ex:
                helper.log('executor: ' + str(ex) + ' response:' + response)
                return  self.EXECUTOR_STATE_DEAD

            message = message.strip()
            messageLower = message.lower()

            helper.log(username + ': ' + message)

            for intervalKey, intervalTime in config.INTERVALS.items():
                if message == intervalKey:
                    self.timerMemory.setTimeFor(intervalKey, intervalTime)
                elif not self.timerMemory.isInMemory(intervalKey):
                    self.chat(intervalKey)
                    self.timerMemory.add(intervalKey, intervalTime)
                    sleep(2.2)

            if username == 'tmi' or username == config.NICK:
                pass
            elif message[0] == '!':
                self.commands(username, message, messageLower)
            elif 'bison' in messageLower and ('hi ' in messageLower or 'hallo ' in messageLower or 'nabend ' in messageLower):
                self.chat("hi " + username + " o/")
            elif 'momentum' in messageLower:
                if username == 'varu7777777':
                     self.chat("@" + username + ' und die erde ne scheibe :P')
                else:
                    self.chat("@" + username + ' es gibt kein momentum!')
            elif 'chemie ' in messageLower or ' chemie' in messageLower:
                self.chat("baukasten")
            elif 'hamster' in  messageLower:
                self.chat("HAMSTER! \o/")
            elif username in self.userGreetings and self.userGreetings[username]['triggerOn'] == message:
                self.chat(self.userGreetings[username]['text'], 120)
            elif len(messageLower) <= 42:
                if 'nabend' in messageLower \
                        or 'moin' in messageLower \
                        or 'huhu' in messageLower \
                        or 'hallo' in messageLower \
                        or 'guten abend'in messageLower \
                        or 'servus'in messageLower:
                    if username in self.userGreetings:
                        if self.userGreetings[username]['triggerOn'] == '*' and not self.chatMemory.isInMemory(self.userGreetings[username]['text']):
                            self.chat(self.userGreetings[username]['text'], 120)
                    elif not self.chatMemory.isInMemory('_GREETING_'):
                        self.chatMemory.add('_GREETING_', 120)
                        import random
                        greetText = random.choice(['ohai', 'hallo @' + username, 'servus', 'noot noot @' + username])
                        greetText +=  random.choice(['', ' o/'])
                        self.chat(greetText, 120)
        return self.EXECUTOR_STATE_OK

    def getUsers(self, forceLoad=False):
        #https://tmi.twitch.tv/group/user/timkalation/chatters
        #http://tmi.twitch.tv/group/user/timkalation/chat_stream
        if False and (forceLoad or self.usersInChatLastRefresh + 10 < time.time()):
            try:
                self.usersInChatLastRefresh = time.time()
                newUsers = set()
                import json
                from urllib.request import urlopen
                url = 'https://tmi.twitch.tv/group/user/' + config.CHAN.replace('#', '') + '/chatters'
                response = urlopen(url, timeout=2)
                data = json.loads(response.read().decode('utf-8'))
                '''
                    {'chatters':
                            {'admins': [], 'staff': [],
                                'viewers': ['bisons_ghost', 'okalot'], 'global_mods': [],
                                'moderators': ['bison_42', 'moobot', 'nightbot', 'timkalation']
                            },
                            '_links': {},
                            'chatter_count': 18
                    }
                '''

                for name in data['chatters']['viewers']:
                    if name is not config.NICK:
                        newUsers.add(name)
                for name in data['chatters']['moderators']:
                    if name is not config.NICK:
                        newUsers.add(name)

                self.usersInChat = newUsers
            except Exception as ex:
                helper.log('getUsers ERROR: ' + str(ex))

        return self.usersInChat

    def chat(self, msg, memoryLifeTime = 30):
        """

        :type msg: string
        """

        if self.chatMemory.isInMemory(msg):
            helper.log('MEMORY BLOCK FOR: "' + msg + '"')
            return False

        if self.isSilent:
            helper.log('stealth-mode: "' + msg + '"')
            return False

        self.chatMemory.add(msg, memoryLifeTime)
        helper.log('sending... "' + msg + '"')
        try:
            self.sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())
        except Exception as ex:
            helper.log('CHAT SEND ERROR: ' + str(ex))
            return False

        return True


if __name__ == "__main__":
    keepRunning = True
    revivedCount = 0
    while keepRunning:
        revivedCount += 1
        helper.log('REVIVED: ' + str(revivedCount))
        bot = tBot()
        bot.revivedCounter = revivedCount
        bot.main_loop()
        if bot.die:
            keepRunning = False
        else:
            sleep(config.REANIMATE_IN_SECONDS)

helper.log('DEAD!')