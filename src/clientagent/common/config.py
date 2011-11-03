import ConfigParser as configparser
import clientagent
from clientagent.common.platform_id import PlatformID

class Config:
    '''
    The unified client agent's configuration system.
    '''

    def __init__(self):
        self.platformID = PlatformID()
        self.configFile = "%s/home/clientagent.cfg" % clientagent.ClientAgentState.CLIENTAGENT_ROOT

# vim:set ai et sts=4 sw=4 tw=80:
