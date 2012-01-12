#!/usr/bin/env python

'''
uca-bootstrap.py
----------------
Basic bootstrap tool for the Unified Agent which runs on both Windows and Linux.
NOTE- For now, this will be fairly rough. But if we decide to keep using it, we
will want to refine it considerably.
'''

import urllib, zipfile

PRODUCTION_IP = '172.16.3.10'
STAGING_IP = '10.4.0.66'

HOSTS = {
        '10.4.0.29' = ['goblinserver2'],
        '172.16.3.10' = ['rmssrvr01.eil-infra.com', 'rmssvr01'],
        '172.16.3.10' = ['eilauto01.eil-infra.com', 'eilauto01'],
        '10.4.0.123' = [' nmsa01.eil-infra.com', 'nmsa01']
    }



# vim:set ai et sts=4 sw=4 tw=80:
