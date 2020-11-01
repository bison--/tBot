import re
from time import sleep
import socket
import time
import os

# more information: https://dev.twitch.tv/docs/irc

if os.path.isfile('config_local.py'):
    import config_local as config
else:
    import config


HOST = "irc.twitch.tv"
PORT = 6667
NICK = config.NICK
PASS = config.PASS
CHAN = config.CHAN
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
LOG_FILE = "recorded_chat.txt"


def log(msg, writeFile):
    logLine = time.strftime("%Y-%m-%d %H:%M:%S: ") + msg
    print(logLine)
    if writeFile:
        open(LOG_FILE, "a").write(logLine)


def chat(sock, msg):
    """
    :type sock: socket.socket
    :type msg: string
    """
    log('sending...', False)
    sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())


def main_loop():
    s = socket.socket()
    try:
        s.connect((HOST, PORT))
        # activate all features
        s.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
        s.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
        s.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
        s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        connected = True
    except Exception as ex:
        print(ex)
        connected = False

    while connected:
        try:
            response = s.recv(2048).decode("utf-8")
            if response == "PING :tmi.twitch.tv\r\n":
                log("PONG: " + response, False)
                s.send("PONG :tmi.twitch.tv\r\n".encode())
            else:
                log(response, True)
                # .tmi.twitch.tv PRIVMSG #jujibla :
                #if ".tmi.twitch.tv PRIVMSG " + CHAN + " :" in response:
                #    log("IGNORED: " + response, False)
                #else:
                #    log(response, True)

        except Exception as ex:
            print(ex)
            connected = False

        sleep(0.1)


if __name__ == "__main__":
    main_loop()
