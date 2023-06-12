import os


from config import *
try:
    from config_local import *
except ImportError:
    pass


from config_bouncer import *
try:
    from config_bouncer_local import *
except ImportError:
    pass
