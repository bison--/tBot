import re
from time import sleep
import socket
import time

import config_loader as config

# more information: https://dev.twitch.tv/docs/irc

HOST = "irc.twitch.tv"
PORT = 6667
NICK = config.NICK
PASS = config.PASS
CHAN = config.CHAN
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


def log(msg, write_to_file):
    log_line = time.strftime("%Y-%m-%d %H:%M:%S: ") + msg
    print(log_line)
    if write_to_file:
        log_file = "data/recorded/recorded_chat_{0}.txt".format(time.strftime("%Y-%m-%d"))
        open(log_file, "a", encoding='utf-8').write(log_line)


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
