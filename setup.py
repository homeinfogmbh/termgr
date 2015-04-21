#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='1.2.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    requires=['docopt',
              'homeinfo',
              'homeinfo.crm',
              'homeinfo.terminals'],
    packages=['termgr',
              'termgr.controllers',
              'termgr.lib'],
    data_files=[('/usr/local/bin', ['files/usr/local/bin/termgr']),
                ('/usr/local/share/termgr',
                 ['files/usr/local/share/termgr/mgr.wsgi',
                  'files/usr/local/share/termgr/setup.wsgi']),
                ('/etc/uwsgi/apps-available',
                 ['files/etc/uwsgi/apps-available/termgr-mgr.ini',
                  'files/etc/uwsgi/apps-available/termgr-setup.ini'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
