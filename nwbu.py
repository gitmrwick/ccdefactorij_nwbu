#!/usr/bin/env python3

import sys
from datetime import datetime
from csv import reader
import pexpect
import subprocess

isodatetime = datetime.now().isoformat()

def dellbu(host):
    ''' backup for a dell unit
    '''
    c = pexpect.spawn(r'ssh {}'.format(host), encoding='utf-8')
    c.logfile = sys.stdout
    c.sendline('enable')
    c.expect(r'sw1#')
    c.sendline(r'copy running-config scp://burnout@burnout/running-config')
    c.expect(r'Password:')
    c.sendline(r'=niet voor scm=')
    c.expect(r'(y/n)')
    c.send(r'y')
    c.expect(r'sw1#', timeout=120)
    c.sendline(r'exit')
    c.expect(r'sw1>')
    c.sendline(r'exit')
    c.close()

def fortigatebu(host):
    ''' backup for a fortigate unit
    '''

dellbu('sw1')
