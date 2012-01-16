'''
configwatch.py
--------------
Pings the config instance to recheck for config file changes every 60 seconds.
'''

from clientagent import get_config
from clientagent.steward.atom import Atom

class ConfigWatch(Atom):
    '''
    This is a very simple class that calls the config recheck every 60 seconds.
    '''
    def __init__(self):
        self.config = get_config()

# vim:set ai et sts=4 sw=4 tw=80:
