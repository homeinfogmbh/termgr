#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='latest',
    author='Richard Neumann',
    packages=['termgr', 'termgr.controllers'],
    data_files=[
        ('/usr/local/bin', [
            'files/usr/bin/termacls',
            'files/usr/bin/termgr']),
         ('/usr/local/sbin', ['files/usr/bin/termadm']),
        ('/usr/share/termgr', [
            'files/usr/share/termgr/check.wsgi',
            'files/usr/share/termgr/query.wsgi',
            'files/usr/share/termgr/setup.wsgi']),
        ('/etc/uwsgi/apps-available', [
            'files/etc/uwsgi/apps-available/termcheck.ini',
            'files/etc/uwsgi/apps-available/termquery.ini',
            'files/etc/uwsgi/apps-available/termsetup.ini'])],
    description=('Homeinfo Terminal Manager'))
