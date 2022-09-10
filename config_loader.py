import os


if os.path.isfile('config_local.py'):
    from config_local import *
else:
    from config import *
