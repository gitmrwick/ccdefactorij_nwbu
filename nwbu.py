#!/usr/bin/env python3

import sys
import shutil
import pathlib
from datetime import datetime
from csv import reader
import click
import pexpect
import subprocess

isodatetime = datetime.now().isoformat(timespec='hours')
homedir = pathlib.Path().home()
budir = homedir.joinpath('backup')
if not budir.exists():
    budir.mkdir()

type_fg = 'fortigate'
type_dl = 'dell'

def dellbu(host):
    ''' backup for a dell unit
    '''
    bufile = '{}-running_{}u'.format(host, isodatetime)
    c = pexpect.spawn(r'ssh {}'.format(host), encoding='utf-8')
    c.logfile = sys.stdout
    c.sendline('enable')
    c.expect(r'{}#'.format(host))
    c.sendline(r'copy running-config scp://burnout@burnout/{}'.format(bufile))
    c.expect(r'Password:')
    # c.sendline(r'niet voor scm')
    c.expect(r'(y/n)')
    c.send(r'y')
    c.expect(r'{}#'.format(host), timeout=120)
    c.sendline(r'exit')
    c.expect(r'{}>'.format(host))
    c.sendline(r'exit')
    c.close()
    shutil.move(
            homedir.joinpath(bufile), 
            budir.joinpath(bufile))

def fortigatebu(host):
    ''' backup for a fortigate unit
    '''
    bufile = '{}-sys_config_{}u'.format(host, isodatetime)
    bupath = budir.joinpath(bufile)
    subprocess.run([
        'scp',
        'gateway:sys_config',
        '{}'.format(bupath)
        ])

@click.command()
@click.argument('csv_bestand', type=click.File('r'))
def nwbu(csv_bestand):
    '''nwbu netwerk backup
    neem een csv bestand met de volgdende formaat:
    host,host_type

     * host is de naam van de host, dit zal ook de prompt zijn voor pexpect

     * host_type is 'dell' of 'fortigate'

    maak een running-config backup en scp de backup naar ~/backup

    '''
    csv_reader = reader(csv_bestand)
    for host in csv_reader:
        print(r'{}'.format(host))
        if host[1] == type_fg:
            fortigatebu(host[0])
        elif host[1] == type_dl:
            dellbu(host[0] )

if __name__ == '__main__':
    nwbu()
