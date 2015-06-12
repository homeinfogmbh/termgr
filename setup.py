#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='1.2.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    requires=['docopt',
              'homeinfo.lib',
              'homeinfo.crm',
              'homeinfo.terminals'],
    packages=['termgr',
              'termgr.controllers',
              'termgr.lib'],
    data_files=[('/usr/sbin', ['files/usr/sbin/termgr']),
                ('/usr/lib/termgr',
                 ['files/usr/lib/termgr/build-key-terminal',
                  'files/usr/lib/termgr/hosts.gen',
                  'files/usr/lib/termgr/nagios-config.gen',
                  'files/usr/lib/termgr/openvpn-client-config.gen']),
                ('/usr/share/termgr',
                 ['files/usr/share/termgr/mgr.wsgi',
                  'files/usr/share/termgr/setup.wsgi',
                  'files/usr/share/termgr/pacman.conf.temp',
                  'files/usr/share/termgr/openvpn.conf.temp',
                  'files/usr/share/termgr/nagios.hostgroup.temp',
                  'files/usr/share/termgr/nagios.terminal.temp']),
                ('/etc/uwsgi/apps-available',
                 ['files/etc/uwsgi/apps-available/termgr-mgr.ini',
                  'files/etc/uwsgi/apps-available/termgr-setup.ini'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
