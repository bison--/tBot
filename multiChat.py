import asyncio
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
CHANS = [config.CHAN, '#limquats']
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


class MultiChat:

    def __init__(self):
        self.connected = False
        self.sock = socket.socket()

    def log(self, msg):
        print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)

    def chat(self, msg):
        """

        :type sock: socket.socket
        :type msg: string
        """
        self.log('sending...')
        for chan in CHANS:
            self.sock.send("PRIVMSG {} :{}\r\n".format(chan, msg).encode())

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
            self.sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
            self.sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
            for chan in CHANS:
                self.sock.send("JOIN {}\r\n".format(chan).encode("utf-8"))

            self.connected = True
        except Exception as ex:
            print(ex)
            self.connected = False

    def main_loop(self):
        while self.connected:
            try:
                response = self.sock.recv(2048).decode("utf-8")
                if response == "PING :tmi.twitch.tv\r\n":
                    self.sock.send("PONG :tmi.twitch.tv\r\n".encode())
                    self.log("PONG")
                else:
                    username = re.search(r"\w+", response).group(0)
                    message = CHAT_MSG.sub("", response)

                    message = message.strip()
                    messageLower = message.lower()

                    self.log(username + ": " + message)

                    if username == 'tmi' or username == config.NICK:
                        pass
                    #elif "!test" == messageLower:
                    #    chat(s, "HAMSTER!")
                    #elif 'hamster' in message:
                    #    chat(s, "HAMSTER! \o/")

                user_message = input("send: ")
                if user_message:
                    self.chat(user_message)

            except Exception as ex:
                print(ex)
                self.connected = False

            sleep(0.1)


async def async_chat(chat):
    while True:
        user_message = await asyncio.to_thread(input, "send: ")
        if user_message:
            await chat(chat.sock, user_message)


if __name__ == "__main__":
    chat = MultiChat()
    chat.connect()
    asyncio.run(async_chat(chat))
    chat.main_loop()
