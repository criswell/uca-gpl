'''
Basic utilities which we may need multiple times
'''

import os

def mkdir_p(path):
    '''
    Does the equivalent of a 'mkdir -p' (Linux) on both platforms.
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

# vim:set ai et sts=4 sw=4 tw=80:
