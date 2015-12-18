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
              'homeinfo.terminals',
              'hipster'],
    packages=['termgr',
              'termgr.controllers',
              'termgr.lib'],
    data_files=[('/etc', ['files/etc/termgr.conf']),
                ('/usr/bin', [
                    'files/usr/bin/termgr',
                    'files/usr/bin/termadm']),
                ('/usr/share/termgr',
                 ['files/usr/share/termgr/mgr.wsgi',
                  'files/usr/share/termgr/setup.wsgi',
                  'files/usr/share/termgr/stats.wsgi']),
                ('/etc/uwsgi/apps-available',
                 ['files/etc/uwsgi/apps-available/termgr.ini',
                  'files/etc/uwsgi/apps-available/termsetup.ini',
                  'files/etc/uwsgi/apps-available/termstats.ini'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
