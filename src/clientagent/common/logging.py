'''
logging.py
----------

The client agent's logging class. Simple, cross-platform, logging functionality.
'''

class Logging:
    __borg_state = {}

    __is_setup = False

    def __init__(self):
        self.__dict__ = self.__borg_state

# vim:set ai et sts=4 sw=4 tw=80: