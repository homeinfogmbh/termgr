#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='1.2.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    packages=['homeinfo.termgr',
              'homeinfo.termgr.controllers',
              'homeinfo.termgr.lib'],
    data_files=[('/usr/local/sbin', ['files/usr/local/sbin/build-key-auto']),
                ('/usr/local/share/termgr',
                 ['files/usr/local/share/termgr/mgr.wsgi',
                  'files/usr/local/share/termgr/pacman.conf.temp',
                  'files/usr/local/share/termgr/setup.wsgi',
                  'files/usr/local/share/termgr/terminals.conf.temp']),
                ('/etc/uwsgi/apps-available',
                 ['files/etc/uwsgi/apps-available/termgr-mgr.ini',
                  'files/etc/uwsgi/apps-available/termgr-setup.ini'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
