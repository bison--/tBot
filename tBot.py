import re
from time import sleep
import socket
import time
import os
import shortTermMemory
import randomList
import helper


if os.path.isfile('config_local.py'):
    import config_local as config
else:
    import config

STREAMER_NAME = config.CHAN.replace('#', '')
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
        self.lastTimeMessageReceived = 0
        self.connected = False
        self.die = False

        self.myMasters = {'timkalation': 'timkalation', 'bison_42': 'bison_42', 'raymonddoerr': 'raymonddoerr'}
        self.myMastersFile = 'myMasters.json'
        myMastersTmp = helper.loadJson(self.myMastersFile)

        if myMastersTmp is not None:
            myMasters = myMastersTmp

        if STREAMER_NAME not in self.myMasters:
            self.myMasters[STREAMER_NAME] = STREAMER_NAME

        self.mySubMasters = {'Plantprogrammer': 'Plantprogrammer'}
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

        self.giveAwayFile = 'giveAway.json'
        self.giveAways = {}
        giveAwaysTmp = helper.loadJson(self.giveAwayFile)
        if giveAwaysTmp is not None:
            self.giveAways = giveAwaysTmp

        self.rudesFile = 'rudes.json'
        self.rudes = {}
        rudesTmp = helper.loadJson(self.rudesFile)
        if rudesTmp is not None:
            self.rudes = rudesTmp

        self.songRequestsFile = 'songRequests.json'
        self.songRequests = {}
        songRequestsTmp = helper.loadJson(self.songRequestsFile)
        if songRequestsTmp is not None:
            self.songRequests = songRequestsTmp
        self.songRequestsModule = randomList.randomList()
        self.songRequestsModule.loadFromDict(self.songRequests)

        self.tquest = None

        self.usersInChatLastRefresh = 0
        self.usersInChat = set()

        self.messageQueue = []

        self.EXECUTOR_STATE_DEAD = 0
        self.EXECUTOR_STATE_OK = 1
        self.EXECUTOR_STATE_EMPTY = 2

        self.momentumIndex = 0

    def checkMaster(self, username, message='', silent=False):
        if username in self.myMasters:
            return True
        elif not silent:
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

    def checkRude(self, username):
        if username in self.rudes:
            self.rudes[username] += 1
            helper.saveJson(self.rudesFile, self.rudes)
            return True
        return False

    def getIntegratedList(self, listName=''):
        if listName == 'submasters':
            return self.mySubMasters
        elif listName == 'masters':
            return self.myMasters
        elif listName == 'dynamiccommands':
            return self.dynamicCommands

        return {'UNKNOWN:': listName}

    def commands(self, username, message, messageLower):
        chatName = '@' + username

        if self.checkRude(username):
            pass
        elif "!test" == messageLower:
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
        elif '!hilfe' == messageLower or '!help' == messageLower or '!commands' == messageLower:
            self.chat("help your self: https://github.com/bison--/tBot")
        elif '!wassindhamster' == messageLower or '!hamster' == messageLower:
            helper.explainHamster(self)
        elif '!go' == messageLower:
            self.chat("@" + STREAMER_NAME + ": GO GO TIM TIM GO GO!")
        elif '!burn' == messageLower:
            self.chat('🔥' * 10)
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

        elif message.startswith('!rude add '):
            if self.checkMaster(username):
                rudeUsername = message.replace('!rude add ', '')
                self.chat('adding @' + rudeUsername + ' to my rude user list.')
                self.rudes[rudeUsername] = 1
                helper.saveJson(self.rudesFile, self.rudes)

        elif not config.LOBOTOMY and message.startswith('!sr'):
            if self.checkMaster(username, '', True):
                songRequest = message.replace('!sr ', '')
                if songRequest not in self.songRequests:
                    self.songRequests[songRequest] = time.strftime("%Y-%m-%d %H:%M:%S: ") + username + ' ' + songRequest
                    helper.saveJson(self.songRequestsFile, self.songRequests)
                    self.songRequestsModule.loadFromDict(self.songRequests)

        elif not config.LOBOTOMY and messageLower.startswith('!!sr'):
            if self.checkSubMaster(username):
                amount = messageLower.replace('!!sr ', '')
                if amount.isnumeric():
                    amount = int(amount)
                    if amount > 5:
                        amount = 5
                else:
                    amount = 1

                #if not hasattr(self, 'songRequestsModule'):
                #    import randomList
                #    self.songRequestsModule = randomList.randomList()
                #    # TODO: load file to list

                for i in range(amount):
                    self.addMessageQueue('!sr ' + self.songRequestsModule.getElement())

        elif not config.LOBOTOMY and '!want' == messageLower:
            answerMessage = ''
            if username in self.giveAways:
                if self.giveAways[username] == 1:
                    answerMessage = 'you already got a key from me' + chatName
                else:
                    answerMessage = 'you are already on my wish list ' + chatName
            else:
                answerMessage = 'added you to my wish list ' + chatName
                self.giveAways[username] = 0
                helper.saveJson(self.giveAwayFile, self.giveAways)

            self.whisper(username, answerMessage)
            self.chat(answerMessage, 1)

        elif not config.LOBOTOMY and ('!wantsome' == messageLower or '!whowantsome' == messageLower):
            answerMessage = ''
            userAllowedList = []
            for wantName, wantHas in self.giveAways.items():
                if wantHas == 0:
                    userAllowedList.append(wantName)

            if len(userAllowedList) == 0:
                answerMessage = 'no one wants a key at this moment :*('
            else:
                answerMessage = str(len(userAllowedList)) + ' users !want some: ' + ','.join(userAllowedList)

            if len(answerMessage) > 490:
                answerMessage = answerMessage[0:490]
                answerMessage += '...'

            self.chat(answerMessage)

        elif not config.LOBOTOMY and '!wantyougone' == messageLower:
            if username == config.NICK or self.checkMaster(username):
                allGotOne = {}
                oldUserCount = len(self.giveAways)
                for wantName, wantHas in self.giveAways.items():
                    if wantHas == 1:
                        allGotOne[wantName] = 1

                self.giveAways = allGotOne
                self.chat('i removed ' + str(oldUserCount - len(self.giveAways)) + " users from the !want list (i'm so sorry)")
                helper.saveJson(self.giveAwayFile, self.giveAways)

        elif not config.LOBOTOMY and '!getsome' == messageLower:
            if username == config.NICK or self.checkMaster(username):
                import random

                userAllowedList = []
                for wantName, wantHas in self.giveAways.items():
                    if wantHas == 0:
                        userAllowedList.append(wantName)

                if len(userAllowedList) == 0:
                    self.chat('there is no one left who !want a key :*(')
                else:
                    _userGetOne = random.choice(userAllowedList)

                    key = helper.popGiveAway()
                    if key == '':
                        self.chat('there is no KEY left to give away :*(')
                    else:
                        getMsg = 'here is your key ' + _userGetOne + ' "' + key + '" have fun o/'
                        helper.log('GIVEAWAY TO: "'+ _userGetOne + '" KEY: "'+ key +'"')
                        #self.chat(getMsg)
                        if self.whisper(_userGetOne, getMsg):
                            #self.whisper('bison_42', getMsg)
                            self.whisper('raymonddoerr', 'COPY:' + getMsg)
                            self.giveAways[_userGetOne] = 1
                            helper.saveJson(self.giveAwayFile, self.giveAways)
                            self.chat('and the winner is: @' + _userGetOne)
                        else:
                            self.chat('something went wrong!')

        elif config.TQUEST_URL != '' and message.startswith('!tquest'):
            try:
                import tquest

                if self.tquest == None:
                    self.tquest = tquest.tquest()

                readyMessage = message.replace('!tquest', '')
                self.tquest.command(username, readyMessage)
                if self.tquest.toSend != '':
                    self.chat(self.tquest.toSend)
                    self.tquest.toSend = ''

            except Exception as ex:
                print('tquest error:', ex)

        elif '!alive' == messageLower:
            if not self.chatMemory.isInMemory('!alive'):
                self.chatMemory.add('!alive', helper.DURATION_MINUTES_2)
                secondsAlive = time.time() - self.startTime
                self.chat('ich bin seit {} sekunden / {} am leben und wurde {}x wiederbelebt'.format(secondsAlive, helper.getReadableTime(secondsAlive), self.revivedCounter))

        elif '!takebluepill' == messageLower or '!bluepill' == messageLower:
            if self.checkSubMaster(username):
                self.chat('i will forget everything...')
                self.chatMemory.clean(True)
                self.timerMemory.clean(True)

        elif not config.LOBOTOMY and messageLower.startswith('!wetten'):
            if not hasattr(self, 'wette'):
                import iBet
                self.wette = iBet.iBet(self)
            self.wette.commands(username, message, messageLower)

        elif not config.LOBOTOMY and message.startswith('!addGreeting'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) < 4:
                    self.chat(chatName + ' this is wrong -.- syntax: username triggerOn(* for default) greetingTEXT')
                else:
                    _userName = cmdParts[1]
                    _triggerOn = cmdParts[2]
                    if _triggerOn[0] == '!':
                        self.chat(chatName + ' this is wrong! commands with "!" NOT allowed!!1!')
                        return

                    _text = ' '.join(cmdParts[3:])
                    if _userName in self.userGreetings:
                        self.chat(chatName + ' i will change my greeting for "' + _userName + '"')
                    else:
                        self.chat(chatName + ' i added "' + _userName + '" to my greeting log!')
                    self.userGreetings[_userName] = {'triggerOn': _triggerOn, 'text': _text}
                    helper.saveJson(self.userGreetingsFile, self.userGreetings)

        elif not config.LOBOTOMY and messageLower.startswith('!match'):
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

        elif messageLower.startswith('!!submaster') or messageLower.startswith('!!master'):
            if self.checkMaster(username):
                cmdParts = message.split(' ')
                if len(cmdParts) < 2:
                    self.chat(chatName + ' this is wrong -.-')
                cmdKey = cmdParts[1]

                dynList = self.getIntegratedList(cmdParts[0].replace('!!', ''))
                isSubMaster = 'sub' in cmdParts[0]

                if len(cmdParts) == 2 and cmdKey == 'list':
                    listOfAllXMasters = ', '.join(dynList)
                    self.chat(listOfAllXMasters)
                elif len(cmdParts) == 3:
                    newXMasterName = cmdParts[2]
                    if cmdKey == 'add':
                        if isSubMaster:
                            self.mySubMasters[newXMasterName] = newXMasterName
                            helper.saveJson(self.mySubMastersFile, self.mySubMasters)
                            self.chat('added "' + newXMasterName + '" as my new sub master!')
                        else:
                            self.myMasters[newXMasterName] = newXMasterName
                            helper.saveJson(self.myMastersFile, self.myMasters)
                            self.chat('added "' + newXMasterName + '" as my new master!')
                    elif cmdKey == 'del':
                        if isSubMaster:
                            self.mySubMasters[newXMasterName] = newXMasterName
                            helper.saveJson(self.mySubMastersFile, self.mySubMasters)
                            self.chat('removed "' + newXMasterName + '" as sub master!')
                        else:
                            self.chat('sorry @' + chatName + ', i can not do that!')
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
                    if cmdText.startswith("\\"):
                        self.chat('sorry ' + chatName + ' but I can NOT do that!')
                    else:
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

        elif message.startswith('!!list'):
            if self.checkSubMaster(username):
                parts = messageLower.split()
                if len(parts) == 2:
                    listOfThings = self.getIntegratedList(parts[1])
                    msg = ', '.join(listOfThings)
                    self.chat(msg)

        elif message in self.dynamicCommands:
            self.chat(self.dynamicCommands[message])

    def main_loop(self):
        try:
            self.sock.connect((HOST, PORT))
            self.sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
            self.sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
            self.sock.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
            self.connected = True
            self.chat('hi all o/')
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
            if response.strip() != '':
                self.lastTimeMessageReceived = time.time()
            self.timeoutCounter = 0
        except socket.timeout:
            #helper.log('timeout')
            self.timeoutCounter += 1
        except Exception as ex:
            self.connected = False
            helper.log('FATAL recv ERROR: ' + str(ex))

        if self.lastTimeMessageReceived > 0 and time.time() > (self.lastTimeMessageReceived + 600):
            helper.log('lastTimeMessageReceived ERROR: ' + str(self.lastTimeMessageReceived))
            self.connected = False
            return self.EXECUTOR_STATE_DEAD

        if self.timeoutCounter >= 400:
            helper.log('timeoutCounter ERROR: ' + str(self.timeoutCounter))
            self.connected = False
            return self.EXECUTOR_STATE_DEAD

        if response is None or response == '':
            return self.EXECUTOR_STATE_EMPTY

        if self.sendMessageQueue():
            time.sleep(1)  # anti-spam protection

        if response == "PING :tmi.twitch.tv\r\n":
            self.sock.send("PONG :tmi.twitch.tv\r\n".encode())
            helper.log("PONG")
        else:
            username = ''
            message = ''
            try:
                # possible error on connection-loss: 'NoneType' object has no attribute 'group'
                username = re.search(r"\w+", response).group(0)
                message = CHAT_MSG.sub("", response)
            except Exception as ex:
                helper.log('executor: ' + str(ex) + ' response:' + response)
                return self.EXECUTOR_STATE_DEAD

            message = message.strip()
            messageLower = message.lower()

            helper.log(username + ': ' + message)

            for intervalKey, intervalTime in config.INTERVALS.items():
                if message == intervalKey:
                    self.timerMemory.setTimeFor(intervalKey, intervalTime)
                elif not self.timerMemory.isInMemory(intervalKey):
                    ## no lobotomy for configs!
                    # if not config.LOBOTOMY:
                    self.chat(intervalKey)
                    self.timerMemory.add(intervalKey, intervalTime)
                    sleep(2.2)

            if username == 'tmi' or username == config.NICK:
                pass
                #helper.log(response)
            elif self.checkRude(username):
                helper.log('RUDE BLOCK: ' + username)

            elif message[0] == '!':
                self.commands(username, message, messageLower)

            elif not config.LOBOTOMY:
                if ('bison' in messageLower or STREAMER_NAME in messageLower) \
                        and (
                            'hi ' in messageLower
                            or 'hallo ' in messageLower
                            or 'nabend ' in messageLower
                            or 'noot noot' in messageLower
                        ):
                    self.chat("hi " + username + " o/")
                    self.chatMemory.add('_GREETING_' + username, helper.DURATION_HOURS_1)
                elif config.NICK in message:
                    # direct talk
                    rudeWords = ['klappe', 'schnauze', 'fresse', 'idiot', 'nerven', 'nervt']
                    if any(rudeWord in messageLower for rudeWord in rudeWords):
                        self.chat('THAT was rude @' + username)
                        self.rudes[username] = 1
                        helper.saveJson(self.rudesFile, self.rudes)
                elif 'momentum' in messageLower:
                    if username == 'varu7777777':
                        self.chat("@" + username + ' und die erde ne scheibe :P')
                    else:
                        momentumList = [
                            ' Wir sind der Tempel der Momentum Verleugner. Man verliert wegen sich, nicht weil das Spiel entscheidet, dass man nicht gewinnen darf. Nächste Messe: morgen um 10:00. Kappa',
                            ' Nun bemerket doch, in welch heiligen Hallen wir uns befinden und huldigt denen die schweigend 40:0 darbieten und den Momentum Teufel Lügen strafen!',
                            'Bekehret Euer Selbstbildnis und den Glauben an Eure Stärken. Wendet Euch ab von höheren Mächten die Euch verlieren sehen wollen und wendet Euch Training und Leidenschaft zu. Lasset dies die Nahrung für Euren wachsenden FIFA Erfolg sein. Realtalk: Momentum-ich darf nicht gewinnen-MiMiMi nervt und findet hier keine Zustimmung. Danke. :)',
                            #'/timeout ' + username + ' 66'
                                        ]
                        momentumText = ''

                        if not self.chatMemory.isInMemory('MOMENTUM_TALK_LOCK') and self.momentumIndex >= len(momentumList)-1:
                            self.momentumIndex = 0

                        if self.momentumIndex <= len(momentumList)-1:
                            momentumText = momentumList[self.momentumIndex]
                            self.momentumIndex += 1
                            if momentumText.startswith('/'):
                                self.chat(momentumText)
                            else:
                                self.chat("@" + username + momentumText)

                            if self.momentumIndex >= len(momentumList)-1:
                                self.chatMemory.add('MOMENTUM_TALK_LOCK', helper.DURATION_HOURS_2)

                elif 'chemie ' in messageLower or ' chemie' in messageLower:
                    self.chat("baukasten", helper.DURATION_HOURS_2)
                elif 'hamster' in messageLower:
                    self.chat("HAMSTER! \o/")
                elif username in self.userGreetings and self.userGreetings[username]['triggerOn'] == message:
                    self.chat(self.userGreetings[username]['text'], helper.DURATION_MINUTES_2)
                elif len(messageLower) <= 42:
                    if 'nabend' in messageLower \
                            or 'moin' in messageLower \
                            or 'huhu' in messageLower \
                            or ('hallo' in messageLower and not 'halloween' in messageLower) \
                            or 'guten abend' in messageLower \
                            or 'servus' in messageLower \
                            or 'noot noot' in messageLower:
                        if self.chatMemory.isInMemory('_GREETING_' + username):
                            pass
                        elif username in self.userGreetings:
                            if self.userGreetings[username]['triggerOn'] == '*' and not self.chatMemory.isInMemory(self.userGreetings[username]['text']):
                                self.chatMemory.add('_GREETING_' + username, helper.DURATION_HOURS_4)
                                self.chat(self.userGreetings[username]['text'], helper.DURATION_HOURS_4)
                        elif not self.chatMemory.isInMemory('_GREETING_'):
                            self.chatMemory.add('_GREETING_', helper.DURATION_MINUTES_2)
                            self.chatMemory.add('_GREETING_' + username, helper.DURATION_HOURS_4)
                            import random
                            greetText = random.choice(['ohai', 'ohai @' + username, 'hallo @' + username, 'servus', 'noot noot @' + username])
                            greetText += random.choice(['', ' o/'])
                            self.chat(greetText, 120)
            else:
                pass
                #helper.log('UNKNOWN:' + response)

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

    def whisper(self, userName, msg):
        helper.log('whispering to "' + userName + '"... "' + msg + '"')
        try:
            self.sock.send("PRIVMSG #jtv :/w {} {}\r\n".format(userName, msg).encode())
        except Exception as ex:
            helper.log('CHAT SEND WHISPER ERROR: ' + str(ex))
            return False

        return True

    def chat(self, msg, memoryLifeTime=30, chatDelay=0):
        """

        :type msg: string
        :type memoryLifeTime: int
        :type chatDelay: int
        """

        if self.chatMemory.isInMemory(msg):
            helper.log('MEMORY BLOCK FOR: "' + msg + '"')
            return False

        if self.isSilent:
            helper.log('stealth-mode: "' + msg + '"')
            return False

        self.chatMemory.add(msg, memoryLifeTime)
        self.addMessageQueue(msg)

        if chatDelay > 0:
            time.sleep(chatDelay)

        # for commands that rely on a timeout send one instantly for an outer-function sleep-loop
        # TODO: hope that there is nothing else in the buffer ^^"
        return self.sendMessageQueue()

    def addMessageQueue(self, msg='', maxLength=499):
        if len(msg) <= maxLength:
            self.messageQueue.append(msg)
            return

        words = msg.split()
        rebuildParts = ''
        for word in words:
            rebuildPartsTest = rebuildParts + ' ' + word
            if len(rebuildPartsTest) >= maxLength:
                self.messageQueue.append(rebuildParts)
                rebuildParts = word
            else:
                rebuildParts = rebuildPartsTest

        if rebuildParts:
            self.messageQueue.append(rebuildParts)

    def sendMessageQueue(self):
        if len(self.messageQueue) == 0:
            return False

        msg = self.messageQueue.pop(0)

        helper.log('sending "' + msg + '"')
        try:
            self.sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())
        except Exception as ex:
            helper.log('CHAT SEND ERROR: ' + str(ex))
            return False

        return True


if __name__ == "__main__":
    keepRunning = True
    revivedCount = 0
    time.sleep(config.LAUNCH_DELAY)

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
