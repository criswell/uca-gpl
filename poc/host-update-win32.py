#!/usr/bin/env python

''' Silly host munger '''

f = open('C:\windows\system32\drivers\etc\hosts', 'a')

f.write('10.4.0.29       goblinserver2\n')
f.write('172.16.3.10     rmssrvr01.eil-infra.com rmssvr01\n')
f.write('172.16.3.10     eilauto01.eil-infra.com eilauto01\n')

f.close()
