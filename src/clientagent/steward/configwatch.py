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
        lastTime = None
        pass

    def update(self, timeDelta):
        if lastTime is None:
            lastTime = timeDelta
        else:
            pass

    def shutdown(self):
        # Nothing to do
        pass

# vim:set ai et sts=4 sw=4 tw=80:
