import os

from modules import helper


class UserListFile:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = os.path.basename(self.__file_path)
        self.__file_name_no_ext = os.path.splitext(self.__file_name)[0]

        self.__file_change_date = 0.0
        if os.path.isfile(self.__file_path):
            self.__file_change_date = self.__get_modified_time()

        self.__user_names = set()

        self.__has_data = self.__load_user_list()

    def __load_user_list(self):
        self.__user_names.clear()

        if not self.file_exists():
            helper.log("file '{}' not found.".format(self.__file_path))
            return False

        with open(self.__file_path, 'r') as file_handle:
            for line in file_handle:
                user_name = line.strip()
                if user_name and user_name not in self.__user_names:
                    self.__user_names.add(user_name)

        return True

    def __get_modified_time(self):
        return os.path.getmtime(self.__file_path)

    def file_exists(self):
        return os.path.isfile(self.__file_path)

    def update_file(self):
        if not self.file_exists():
            # when the file got deleted, we need to clear the user list
            self.__user_names.clear()
            return False

        if self.get_user_count() == 0 or self.__get_modified_time() > self.__file_change_date:
            self.__file_change_date = self.__get_modified_time()
            return self.__load_user_list()

        return False

    def get_user_set(self):
        return self.__user_names

    def get_user_count(self):
        return len(self.__user_names)

    def get_file_name_no_ext(self):
        return self.__file_name_no_ext

    def contains_user(self, user_name):
        return user_name in self.__user_names
