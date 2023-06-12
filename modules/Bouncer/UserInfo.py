
class UserInfo:
    def __init__(self, _user_name, _is_bad, _in_file_name=None):
        self.user_name = _user_name
        self.is_bad = _is_bad
        self.in_file_name = _in_file_name

    def __eq__(self, other):
        return self.user_name == other.user_name
