import time

class iBet(object):
    def __init__(self, tBot):
        """
        :type tBot: tBot.tBot
        """
        self.tBot = tBot
        self.currentBetName = ''
        self.userBets = {}
        self.betsOpen = False

    def commands(self, username, message, messageLower):
        """
        :type username: string
        :type message: string
        :type messageLower: string
        """
        chatName = '@' + username

        parts = message.split(' ')
        if len(parts) < 2:
            self.tBot.chat('falsches Kommando ' + chatName)
            return False
        command = parts[1]
        option = ' '.join(parts[2:])
        print('*' * 10)
        print('commands')
        print(parts)
        print(option)

        if '!start' == command:
            self.betsOpen = True
            if username not in self.tBot.myMasters:
                self.tBot.chat(chatName + ' you are not my master!')
                return False
            else:
                self.currentBetName = option
                self.tBot.chat('wette {} gestartet'.format(self.currentBetName))
        elif '!stop' == command:
            if username not in self.tBot.myMasters:
                self.tBot.chat(chatName + ' you are not my master!')
                return False
            else:
                if option.strip() == '':
                    self.tBot.chat(chatName + ' keine siegbedingung gesetzt!')
                    return False

                self.betsOpen = False
                #self.tBot.chat('es werden keine wetten mehr angenommen!')
                betResult = option.lower()

                self.tBot.chat('*' * 23)
                time.sleep(2.3)
                self.tBot.chat('wette "{}" beendet, Ergebnis: "{}"'.format(self.currentBetName, option))
                time.sleep(2.1)

                winnerList = []
                loserList = []
                for key, value in self.userBets.items():
                    if value.lower() == betResult:
                        winnerList.append(key)
                    else:
                        loserList.append(key)

                self.tBot.chat('gewonnen haben ' + ', '.join(winnerList) + ' und verloren haben ' + ', '.join(loserList))

        elif '!gilt' == command:
            if username not in self.tBot.myMasters:
                self.tBot.chat(chatName + ' you are not my master!')
                return False
            else:
                self.betsOpen = False
                self.tBot.chat('es werden keine wetten mehr angenommen!')

        elif '!hilfe' == command or '!help' == command:
            wettString = 'wette erstellen: !wetten !start namederwette'
            wettString += ' | wetten: !wetten !das sieg'
            wettString += ' | wetten: !wetten !das niederlage'
            wettString += ' | keine wetten mehr zulassen !wetten !gilt namederwette'
            wettString += ' | wette beenden !wetten !stop namederwette'
            self.tBot.chat(wettString)

        elif '!das' ==  command:
            if not self.betsOpen:
                self.tBot.chat(chatName + 'es werden keine wetten mehr angenommen')
            if username in self.userBets:
                self.tBot.chat(chatName + ' du hast bereits "' + self.userBets[username] + '" gewettet')
            else:
                self.userBets[username] = option
                self.tBot.chat(chatName + ' wette auf "' + option +  '" angenommen!')

