import re
from time import sleep
import socket
import time
import os
import json
import shortTermMemory


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


def realitycheck(bot):
    """

    :param bot: tBot
    """
    checks = [
        '''13.06.2016 10:44 :~: Einmal Popcorn bitte. 50 Liter.

        Reality
        Ich höre: "Forever alone"

        Story
        Ich habe eine Szene aus Indiana Jones und der Tempel des Todes im Kopf und denke: "Die Insekten lassen dich niemals allein."''',

        '''02.06.2016 20:52 :~: Saudi Arabi Money Rich

        Reality
        Ich lese auf Twitter: "Haftbefehl gegen mutmaßlichen IS-Terroristen."

        Story
        Ich frage mich, was mehr Terror bedeutet. So eine kleine Explosion oder 3:28 Gesinge von Chabos und Babos?''',

        '''13.02.2016 17:54 :~: Die Stange war zu kurz

        Reality
        Eine neue Person betritt den Raum. Bewaffnet mit Hut und Heißklebepistole läuft sie zielstrebig auf jemanden zu. Dieser ist allerdings nicht zu Gesprächen aufgelegt...
        Story
        ... und sagt: "Gib mal kurz!", schnappt sich die Heißklebepistole, hält sie sich an die Schläfe und drückt ab.'''
    ]
    import random
    for line in random.choice(checks).split("\n"):
        bot.chat(line)


def explainHamster(bot):
    """

    :param bot: tBot
    """
    bot.chat("HAMSTER sind im grunde genau wie Zigaretten...")
    sleep(1.5)
    bot.chat("Vollkommen harmlos... bis man sie sich in den Mund steckt und anzündet!")
    sleep(1.5)


def saveJson(file, data):
    try:
        with open(file, 'w') as data_file:
            json.dump(data, data_file)
    except Exception as ex:
        print(ex)


def loadJson(file):
    data = None
    try:
        with open(file) as data_file:
            data = json.load(data_file)
    except Exception as ex:
        print(ex)

    return data


def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)


class tBot(object):
    def __init__(self):
        self.sock = socket.socket()
        self.connected = False
        self.die = False
        self.dynamicCommandsFile = 'dynamicCommands.json'
        self.dynamicCommands = {}
        self.chatMemory = shortTermMemory.shortTermMemory()

        dynamicCommandsTmp = loadJson(self.dynamicCommandsFile)
        if dynamicCommandsTmp is not None:
           self.dynamicCommands = dynamicCommandsTmp

    def commands(self, username, message, messageLower):
        chatName = '@' + username
        myMasters = {'timkalation', 'bison_42'}

        if "!test" == messageLower:
            self.chat("HAMSTER!")
        elif '!lupfer' == messageLower:
            self.chat('lupfe die lupf hupf ¯\_(ツ)_/¯')
        elif '!deckel' == messageLower:
            self.chat("!dackel")
        elif '!woher' == messageLower:
            self.chat("aus dem meer")
        elif '!wohin' == messageLower:
            self.chat("ins TOR natürlich!")
        elif '!wovon' == messageLower:
            self.chat("purer skill!!1!")
        elif '!wann' == messageLower:
            self.chat("bis dann o/")
        elif '!wurm' == messageLower:
            self.chat("~~~~~~~~~~~~~~~~~~~~~~~~O<")
        elif '!wasstimmtdennmitdirnicht' == messageLower:
            realitycheck(self)
        elif '!hilfe' == message or '!help' == messageLower:
            self.chat("help your self :P")
        elif '!wassindhamster' == messageLower or '!hamster' == messageLower:
            explainHamster(self)
        elif '!go' == messageLower:
            self.chat("@timkalation: GO GO TIM TIM GO GO!")
        elif '!burn' == messageLower:
            self.chat('🔥'*10)
        elif '!kill' == messageLower:
            if username in myMasters:
                self.chat('live long and prosper 🖖')
                self.die = True
                self.connected = False
            else:
                self.chat(chatName + ' your kung fu is not strong enough!')
        elif message.startswith('!add'):
            if username in myMasters:
                cmdParts = message.split(' ')
                if len(cmdParts) <= 3:
                    self.chat(chatName + ' this is wrong -.-')
                else:
                    cmdKey = cmdParts[1]
                    cmdText = ' '.join(cmdParts[2:])
                    if cmdKey in self.dynamicCommands:
                        self.chat(chatName + ' i will change my quest for "' + cmdKey + '"')
                    else:
                        self.chat(chatName + ' i added "' + cmdKey + '" to my quest log!')
                    self.dynamicCommands[cmdKey] = cmdText
                    saveJson(self.dynamicCommandsFile, self.dynamicCommands)
            else:
                self.chat(chatName + ' your kung fu is not strong enough!')
        elif message in self.dynamicCommands:
            self.chat(self.dynamicCommands[message])

    def main_loop(self):
        try:
            self.sock.connect((HOST, PORT))
            self.sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
            self.sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
            self.sock.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
            self.connected = True
        except Exception as ex:
            self.connected = False
            print(ex)

        while self.connected:
            try:
                self.executor()
            except Exception as ex:
                self.connected = False
                print(ex)

            sleep(0.1)

        log('PASSED AWAY')

    def executor(self):
        response = self.sock.recv(2048).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            self.sock.send("PONG :tmi.twitch.tv\r\n".encode())
            log("PONG")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

            message = message.strip()
            messageLower = message.lower()

            log(username + ": " + message)

            if username == 'tmi' or username == config.NICK:
                pass
            elif message[0] == '!':
                self.commands(username, message, messageLower)
            elif 'hamster' in  message:
                self.chat("HAMSTER! \o/")
            elif 'bison' in messageLower and ('hi ' in messageLower or 'hallo ' in messageLower or 'nabend ' in messageLower):
                self.chat("hi " + username + " o/")
            elif 'nabend' in messageLower \
                    or 'moin' in messageLower \
                    or 'huhu' in messageLower \
                    or 'hallo' in messageLower \
                    or 'guten abend'in messageLower\
                    or 'servus'in messageLower:
                self.chat("ohai o/")
            elif 'momentum' in messageLower:
                if username == 'varu7777777':
                     self.chat("@" + username + ' und die erde ne scheibe :P')
                else:
                    self.chat("@" + username + ' es gibt kein momentum!')
            elif 'chemie ' in messageLower or ' chemie' in messageLower:
                self.chat("baukasten")

    def chat(self, msg):
        """

        :type msg: string
        """

        if self.chatMemory.isInMemory(msg):
            log('MEMORY BLOCK FOR: "' + msg + '"')
            return False

        self.chatMemory.add(msg, 30)
        log('sending...')
        self.sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())


if __name__ == "__main__":
    keepRunning = True
    revivedCount = 0
    while keepRunning:
        revivedCount += 1
        log('REVIVED: ' + str(revivedCount))
        bot = tBot()
        bot.main_loop()
        if bot.die:
            keepRunning = False
        else:
            sleep(10 * 60)

log('DEAD!')