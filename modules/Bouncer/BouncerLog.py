import os
import datetime
from typing import List

import config_loader as config
from modules import helper
from modules.Bouncer.UserInfo import UserInfo


class BouncerLog:
    def __init__(self):
        self.__log_entries: List[UserInfo] = []
        self.__locked_date_time = None
        self.__locked_date = None
        self.__log_folder = ''
        self.__log_file = ''
        self.__set_today_log_file()

    def add_log_entry(self, _user_info: UserInfo):
        self.__set_today_log_file()
        self.__log_entries.append(_user_info)

    def save_log(self):
        helper.saveJson(self.__log_file, [obj.__dict__ for obj in self.__log_entries])

    def __set_today_log_file(self):
        # check if initial call or today has changed
        if self.__locked_date is not None and self.__locked_date == datetime.datetime.now().date():
            # make sure the folder exists
            if os.path.isdir(self.__log_folder):
                return

        # it's a new date, save and clear log
        if self.__log_entries:
            self.save_log()
            self.__log_entries = []

        self.__locked_date_time = datetime.datetime.now()
        self.__locked_date = self.__locked_date_time.date()
        self.__log_folder = self.__get_today_folder()
        self.__create_today_folders()
        self.__log_file = os.path.join(self.__log_folder, str(self.__locked_date_time.timestamp()) + ".json")

    def __get_today_folder(self):
        return os.path.join(config.BOUNCER_LOG_PATH, str(self.__locked_date.year))

    def __create_today_folders(self):
        os.makedirs(self.__log_folder, exist_ok=True)
