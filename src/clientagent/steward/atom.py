'''
atom.py
-------
Base-class from which other steward sub-classes are derived.
'''

import exceptions

class Atom:
    '''
    All atomic steward sub-classes must be derived from this base class.

    The way this works is as follows:

        * Each atom sub-class is added to a queue in the steward.

        * Every 30 seconds, this queue is ran through and the atom sub-classes
            are updated.

        * It is up to the sub-class to determine what (if anything) it needs to
            do.

    The sub-classes thus will have a minimum resolution of 30 seconds, however,
    this is not guaranteed. Due to each class being atomic, they are not
    guaranteed to finish within the next 30 second window. Each could
    potentially be blocking. It's left up to the developer to make their sub-
    classes thread-safe if this is a concern.
    '''

    '''
    Determines whether this atom is active or not.
    '''
    ACTIVE = False

    def __init__(self):
        raise exceptions.NotImplementedError()

    def update(self, timeDelta):
        '''
        Called a minimum of every 30 seconds with the current timeDelta since
        the last time the update loop was begun.
        '''
        raise exceptions.NotImplementedError()

    def shutdown(self):
        '''
        Called at the end of the process- when the agent exits gracefully.
        '''
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
