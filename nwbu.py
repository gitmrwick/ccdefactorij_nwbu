#!/usr/bin/env python3

import sys
from datetime import datetime
from csv import reader
import click
import pexpect

isodatetime = datetime.now().isoformat()

type_fg = 'fortigate'
type_dl = 'dell'

def dellbu(host):
    ''' backup for a dell unit
    '''
    c = pexpect.spawn(r'ssh {}'.format(host), encoding='utf-8')
    c.logfile = sys.stdout
    c.sendline('enable')
    c.expect(r'{}#'.format(host))
    c.sendline(r'copy running-config scp://burnout@burnout/{}-running-config_{}'.format(host, isodatetime))
    c.expect(r'Password:')
    # c.sendline(r'niet voor scm')
    c.expect(r'(y/n)')
    c.send(r'y')
    c.expect(r'{}#'.format(host), timeout=120)
    c.sendline(r'exit')
    c.expect(r'{}>'.format(host))
    c.sendline(r'exit')
    c.close()

def fortigatebu(host):
    ''' backup for a fortigate unit
    '''

@click.command()
@click.argument('csv_bestand', type=click.File('r'))
def nwbu(csv_bestand):

dellbu('sw9')
if __name__ == '__main__':
    nwbu()
