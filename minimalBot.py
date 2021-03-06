import re
from time import sleep
import socket
import time
import os

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


def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)


def chat(sock, msg):
    """

    :type sock: socket.socket
    :type msg: string
    """
    log('sending...')
    sock.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode())


def main_loop():
    s = socket.socket()
    try:
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
                elif "!test" == messageLower:
                    chat(s, "HAMSTER!")
                elif 'hamster' in message:
                    chat(s, "HAMSTER! \o/")

        except Exception as ex:
            print(ex)
            connected = False

        sleep(0.1)


if __name__ == "__main__":
    main_loop()
