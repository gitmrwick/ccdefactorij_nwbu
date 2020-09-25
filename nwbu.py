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
    c.sendline(r'copy running-config scp://burnout@burnout/running-config')
    c.expect(r'Password:')
    c.sendline(r'exit')
    c.sendline(r'exit')
    c.close()

def fortigatebu(host):
    ''' backup for a fortigate unit
    '''

dellbu('sw1')
