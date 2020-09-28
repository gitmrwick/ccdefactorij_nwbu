#!/usr/bin/env python3

import sys
from csv import reader
import click
import pexpect

type_fg = 'fortigate'
type_dl = 'dell'

def dellcmd(host, commando, priviledge):
    ''' backup for a dell unit
    '''
    c = pexpect.spawn(r'ssh {}'.format(host), encoding='utf-8')
    c.logfile = sys.stdout
    c.sendline('enable')
    c.expect(r'{}#'.format(host))
    c.sendline(commando)
    c.expect(r'{}#'.format(host), timeout=120)
    c.sendline(r'exit')
    c.expect(r'{}>'.format(host))
    c.sendline(r'exit')
    c.close()

def fortigatebu(host):
    ''' backup for a fortigate unit
    '''

@click.command()
@click.option('-c', '--commando', default='ping burnout',
        help='commando dat zal op elke host uitgevoerd worden')
@click.option('-t', '--host_type',
        help='dell of fortigate')
@click.option('-p', '--priviledge/--no-priviledge',
        default=True,
        help='voer uit met hoge rechten, priviledge is default')
@click.argument('csv_bestand', type=click.File('r'))
def nwcmd(csv_bestand, commando, host_type, priviledge):
    '''neem een csv bestand met de volgdende formaat:
    host,host_type

     * host is de naam van de host, dit zal ook de prompt zijn voor pexpect

     * host_type is 'dell' of 'fortigate'

    en voer een commando uit op elke host een per een
    '''
    csv_reader = reader(csv_bestand)
    for host in csv_reader:
        if host[1] == type_fg:
            fortigatecmd(host[0], commando, priviledge)
        elif host[1] == type_dl:
            dellcmd(host[0], commando, priviledge)

if __name__ == '__main__':
    nwcmd()
