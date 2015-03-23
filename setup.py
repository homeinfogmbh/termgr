#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='0.1.0-indev',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    packages=['termgr',
              'termgr.controllers',
              'termgr.db',
              'termgr.lib'],
    data_files=[('/usr/local/bin', ['files/usr/local/bin/build-key-auto']),
                ('/usr/local/etc', ['files/usr/local/etc/termgr.conf']),
                ('/usr/local/share',
                 ['files/usr/local/share/pacman.conf.temp',
                  'files/usr/local/share/setup.wsgi',
                  'files/usr/local/share/terminals.conf.temp']),
                ('/etc/uwsgi/apps-available',
                 ['files/etc/uwsgi/apps-available/termgr.ini'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
