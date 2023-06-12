import shortTermMemory
import config_loader as config

from modules import helper
from modules.Bouncer.UserInfo import UserInfo


class Bouncer:
    BOUNCER_BAD_USER_TIME_TO_LIVE = helper.DURATION_HOURS_4
    BOUNCER_GOOD_USER_TIME_TO_LIVE = helper.DURATION_HOURS_1
    BOUNCER_FILES_UPDATE_INTERVAL = helper.DURATION_MINUTES_1 * 10
    BOUNCER_FILES_LAST_UPDATE_KEY = 'BOUNCER_FILES_LAST_UPDATE_KEY'

    def __init__(self):
        self.__memory_users = shortTermMemory.shortTermMemory()
        self.__memory = shortTermMemory.shortTermMemory()
        self.update_files()

    def get_user_info(self, user_name) -> UserInfo:
        user_info = UserInfo(user_name, False)

        if not config.BOUNCER_ACTIVE:
            return user_info

        if self.__memory_users.isInMemory(user_info):
            memory_info: shortTermMemory.memory = self.__memory_users.getFromMemory(user_info)
            return memory_info.data

        for blacklist_file in config.BOUNCER_BLACKLIST:
            if blacklist_file.contains_user(user_name):
                user_info.is_bad = True
                user_info.in_file_name = blacklist_file.get_file_name_no_ext()
                self.__memory_users.add(user_info, self.BOUNCER_BAD_USER_TIME_TO_LIVE)
                return user_info

        self.__memory_users.add(user_info, self.BOUNCER_GOOD_USER_TIME_TO_LIVE)
        return user_info

    def update_files(self):
        if not config.BOUNCER_ACTIVE:
            return

        for blacklist_file in config.BOUNCER_BLACKLIST:
            blacklist_file.update_file()

        self.__memory.addUpdate(self.BOUNCER_FILES_LAST_UPDATE_KEY, self.BOUNCER_FILES_UPDATE_INTERVAL)

    def auto_update_files(self):
        if not config.BOUNCER_ACTIVE:
            return

        if self.__memory.isInMemory(self.BOUNCER_FILES_LAST_UPDATE_KEY):
            return

        self.update_files()
