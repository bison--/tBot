import random
import re
from time import sleep
import socket
import time
import os
from modules import NightWatch


import config_loader as config
if os.path.isfile('config_local_koernerkissenkater.py'):
    import config_local_koernerkissenkater as config


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


def get_flirt_message():
    message_options = [
        'mau',
        'mrau',
        'miau',
        'meow'
    ]

    chosen = random.choice(message_options)

    if chosen == 'mrau':
        return 'mr{}au'.format('r' * random.randint(1, 11))

    return '{}'.format((chosen + ' ') * random.randint(1, 4))


def main_loop():
    sleep(config.LAUNCH_DELAY)

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

    next_interaction = time.time() + 10
    nightwatch = NightWatch.NightWatch()

    while connected:
        if not nightwatch.is_asleep() and time.time() >= next_interaction:
            next_interaction = time.time() + random.randint(60, 3600)
            chat(s, "@Koernerkissenkatze " + get_flirt_message())

        try:
            response = s.recv(2048).decode("utf-8")
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode())
                log("PONG")
            else:
                username = re.search(r"\w+", response).group(0)
                # log(username + ": " + message)

                if username == 'tmi' or username == config.NICK:
                    continue

                nightwatch.received_message(username)

                message = CHAT_MSG.sub("", response)

                message = message.strip()
                message_lower = message.lower()

                if username == 'koernerkissenkatze':
                    answer_her_call = False
                    if 'koernerkissenkater' in message_lower:
                        answer_her_call = True
                    else:
                        answer_her_call = random.randint(0, 100) >= 75

                    if answer_her_call:
                        chat(s, "@Koernerkissenkatze <3 <3 <3 " + get_flirt_message() + ' <3 <3 <3')

        except Exception as ex:
            print(ex)
            connected = False

        sleep(0.1)


if __name__ == "__main__":
    main_loop()
