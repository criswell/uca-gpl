import logging
import clientagent

class Daemon:
    '''
    Generic daemon class from which other daemon/service classes are derived.
    '''

    def __init__(self):
        self.config = clientagent.get_config()

# vim:set ai et sts=4 sw=4 tw=80:
