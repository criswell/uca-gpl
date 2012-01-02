'''
dispatcher_helper.py
--------------------
Any helper functions for the dispatcher that do not fit in the main module.
'''

import os
import logging

# Linux specific methods

def linux_ExecuteCommand(command):
    '''
    Takes a command and executes the external dispatcher script with it. It
    does not sanity check this command- it relies upon either the caller or the
    dispatcher script to filter out incorrect commands.

    Will return the result.
    '''
    pass

# vim:set ai et sts=4 sw=4 tw=80: