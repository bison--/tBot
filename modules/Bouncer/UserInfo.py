from datetime import datetime


class UserInfo:
    SOURCE_MESSAGE = 'message'
    SOURCE_STATUS = 'status'

    def __init__(self, _user_name, _is_bad, _source, _in_file_name=None):
        self.user_name = _user_name
        self.is_bad = _is_bad
        self.in_file_name = _in_file_name
        self.source = _source
        self.detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __eq__(self, other):
        return self.user_name == other.user_name
