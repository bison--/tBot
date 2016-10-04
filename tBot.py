import re
from time import sleep
import socket
import time
import os

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


def realitycheck(s):
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
        chat(s, line)


def explainHamster(s):
    """

    :param s: socket.socket
    """
    chat(s, "HAMSTER sind im grunde genau wie Zigaretten...")
    sleep(1.5)
    chat(s, "Vollkommen harmlos... bis man sie sich in den Mund steckt und anzündet!")
    sleep(1.5)


def commands(s, username, message, messageLower):
    if "!test" == messageLower:
        chat(s, "HAMSTER!")
    elif '!deckel' == messageLower:
        chat(s, "!dackel")
    elif '!woher' == messageLower:
        chat(s, "aus dem meer")
    elif '!wohin' == messageLower:
        chat(s, "ins TOR natürlich!")
    elif '!wovon' == messageLower:
        chat(s, "purer skill!!1!")
    elif '!wann' == messageLower:
        chat(s, "bis dann o/")
    elif '!wurm' == messageLower:
        chat(s, "~~~~~~~~~~~~~~~~~~~~~~~~O<")
    elif '!wasstimmtdennmitdirnicht' == messageLower:
        realitycheck(s)
    elif '!hilfe' == message or '!help' == messageLower:
        chat(s, "help your self :P")
    elif '!wassindhamster' == messageLower or '!hamster' == messageLower:
        explainHamster(s)
    elif '!go' == messageLower:
        chat(s, "@timkalation: GO GO TIM TIM GO GO!")
    elif '!burn' == messageLower:
        chat(s, '🔥'*10)


def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)


def main_loop():
    s = None
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        connected = True
    except Exception as ex:
        print(ex)
        connected = False

    while connected:
        try:
            executor(s)
        except Exception as ex:
            print(ex)

        sleep(0.1)


def executor(s):
    """

    :type s: socket.socket
    """
    response = s.recv(2048).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode())
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
            commands(s, username, message, messageLower)
        elif 'hamster' in  message:
            chat(s, "HAMSTER! \o/")
        elif 'bison' in messageLower and ('hi ' in messageLower or 'hallo ' in messageLower or 'nabend ' in messageLower):
            chat(s, "hi " + username + " o/")
        elif 'nabend' in messageLower \
                or 'moin' in messageLower \
                or 'huhu' in messageLower \
                or 'hallo' in messageLower \
                or 'guten abend'in messageLower\
                or 'servus'in messageLower:
            chat(s, "ohai o/")
        elif 'chemie ' in messageLower or ' chemie' in messageLower:
            chat(s, "baukasten")


def chat(sock, msg):
    """

    :type sock: socket.socket
    :type msg: string
    """
    log('sending...')
    sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())


if __name__ == "__main__":
    main_loop()
