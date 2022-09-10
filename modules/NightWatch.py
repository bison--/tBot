import time
import modules.helper as helper
import config_loader as config
# tells the bot when it's time to "sleep" because there is nobody there


class NightWatch:

    def __init__(self):
        self.time_last_message = 0
        self.sleeping_time = 0
        self.time_till_sleep = helper.DURATION_MINUTES_30
        self.known_bots = {'tmi', config.NICK}

        self.__set_time__()

    def is_asleep(self):
        return time.time() > self.sleeping_time

    def received_message(self, user_name):
        # make sure to trigger this only when the message is not from the bot itself
        if user_name in self.known_bots:
            return

        if self.is_asleep():
            helper.log('WAKE UP!')

        self.__set_time__()

    def __set_time__(self):
        self.sleeping_time = self.time_till_sleep + time.time()
