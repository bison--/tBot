from . import RandomList
from . import helper


class EightBall:

    def __init__(self, tBot):
        """
        :type tBot: tBot.tBot
        """
        self.tBot = tBot
        self.fortunes = RandomList.RandomList()

        self.dataFile = 'eightball.json'
        self.helpUrl = 'https://github.com/bison--/tbot#8-ball'

        # commands are key / requires master level value
        self.availableCommands = {
            '!8ball': False
        }

        self.availableSubCommandsMasterLevel = {
            'add',
            'del',
            'remove',
            'list'
        }

        self.loadData()

    def saveData(self):
        helper.saveJson('data/' + self.dataFile, self.fortunes.elements)

    def loadData(self):
        loaded = helper.loadJson('data/' + self.dataFile)
        if loaded is not None:
            self.fortunes.elements = loaded

    def isCommandCatched(self, message):
        """
        :param message: command from the user
        :type message: str
        :return: bool
        """

        for command in self.availableCommands:
            if message.startswith(command):
                return True

        return False

    def isSubCommandCatched(self, command, commandList):
        if command in commandList:
            return True

        return False

    def process(self, userName, message, messageLower):
        if messageLower == '!8ball':
            self.tBot.chatMemory.add('!8ball', 30)
            self.sendRandomMessage(userName)
            return

        if not self.tBot.checkSubMaster(userName):
            return

        cmdParts = message.split(' ')
        subCommand = ''
        if len(cmdParts) >= 2:
            if self.isSubCommandCatched(cmdParts[1], self.availableSubCommandsMasterLevel):
                subCommand = cmdParts[1]
            else:
                self.tBot.chat(f'({self.tBot.sendMessageCounter}) Unknown command for 8ball, see ' + self.helpUrl, helper.DURATION_IGNORE)
                return

        if len(cmdParts) >= 3:
            if subCommand == 'add':
                self.fortunes.elements.append(message.replace('!8ball add ', ''))
                self.saveData()
                self.tBot.chat(f'({self.tBot.sendMessageCounter}) i will remember this fortune', helper.DURATION_IGNORE)
                return

            if subCommand == 'del' or subCommand == 'remove':
                messageModified = message.replace('!8ball del ', '')
                messageModified = messageModified.replace('!8ball remove ', '')

                try:
                    self.fortunes.elements.remove(messageModified)
                    self.saveData()
                    self.tBot.chat(f'({self.tBot.sendMessageCounter}) i will forget this fortune', helper.DURATION_IGNORE)
                except Exception as ex:
                    self.tBot.chat(f'({self.tBot.sendMessageCounter}) unFORTUNEately i dont know of that', helper.DURATION_IGNORE)

                return

        self.tBot.chat(f'({self.tBot.sendMessageCounter}) Insufficient parameters, see ' + self.helpUrl, helper.DURATION_IGNORE)

    def sendRandomMessage(self, userName):
        modifiedMessage = self.fortunes.getElement()

        if modifiedMessage is None:
            self.tBot.chat(f'({self.tBot.sendMessageCounter}) i have nothing to say')
            return

        modifiedMessage = modifiedMessage.replace('{username}', userName)
        self.tBot.chat(modifiedMessage)
