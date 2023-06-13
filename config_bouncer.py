# don't change anything here that should not be global!
# create a config_bouncer_local.py file and override the values there
from typing import List
from modules.Bouncer.UserListFile import UserListFile

# Bouncer
BOUNCER_ACTIVE = True
BOUNCER_AUTO_BAN = False
BOUNCER_REPORT_TO = []  # list of nicks here
BOUNCER_LOG_PATH = 'data/bouncerLog'  # leave empty to not log

BOUNCER_BLACKLIST: List[UserListFile] = [
    UserListFile('data/userLists/twitch_ban_lists/hate_troll_list_0_g.txt'),
    UserListFile('data/userLists/twitch_ban_lists/hate_troll_list_h_m.txt'),
    UserListFile('data/userLists/twitch_ban_lists/hate_troll_list_n_z.txt'),
    UserListFile('data/userLists/twitch_ban_lists/mad_tos_list.txt'),
    UserListFile('data/userLists/twitch_ban_lists/security_ban_list.txt'),
    UserListFile('data/userLists/twitch_ban_lists/spam_bot_list.txt'),
    UserListFile('data/userLists/twitch_ban_lists/streamsniper_list.txt'),
    UserListFile('data/userLists/test_users.txt'),
]
