import asyncio
import re
import os
import time

if os.path.isfile('config_local.py'):
    import config_local as config
else:
    import config


HOST = "irc.twitch.tv"
PORT = 6667
NICK = config.NICK
PASS = config.PASS
CHANS = config.CHAN.split(',')
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


class SimpleChat:

    def __init__(self):
        self.reader: asyncio.streams.StreamReader | None = None
        self.writer: asyncio.streams.StreamWriter | None = None

    def log(self, msg):
        print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)

    async def chat(self, msg):
        for chan in CHANS:
            self.writer.write(f"PRIVMSG {chan} :{msg}\r\n".encode())

        await self.writer.drain()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        self.writer.write(f"PASS {PASS}\r\n".encode())
        self.writer.write(f"NICK {NICK}\r\n".encode())

        for chan in CHANS:
            self.writer.write(f"JOIN {chan}\r\n".encode())

        await self.writer.drain()

    async def receive_messages(self):
        while True:
            data = await self.reader.readline()
            message = data.decode()
            if message.startswith("PING"):
                self.writer.write("PONG :tmi.twitch.tv\r\n".encode())
                await self.writer.drain()
                # self.log("PONG")
            elif message:
                # self.log(message)
                username = re.search(r"\w+", message).group(0)
                chat_message = CHAT_MSG.sub("", message).strip()
                channel = ''

                if '.tmi.twitch.tv PRIVMSG #' in message:
                    channel = re.search(r"#\w+", message).group(0)

                self.log(f"{channel} | {username}: {chat_message}")

    async def user_input(self):
        while True:
            user_message = await asyncio.to_thread(input, "send: ")
            if user_message:
                await self.chat(user_message)


async def main():
    chat = SimpleChat()
    await chat.connect()
    task_receive_messages = asyncio.create_task(chat.receive_messages())
    task_user_input = asyncio.create_task(chat.user_input())
    await asyncio.gather(task_receive_messages, task_user_input)

if __name__ == "__main__":
    asyncio.run(main())
