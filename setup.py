#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='1.3.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    requires=[
        'docopt',
        'homeinfo.lib',
        'homeinfo.crm',
        'homeinfo.terminals',
        'hipster'],
    packages=[
        'termgr',
        'termgr.controllers',
        'termgr.lib'],
    data_files=[
        ('/etc', ['files/etc/termgr.conf']),
        ('/usr/bin', [
            'files/usr/bin/termgr',
            'files/usr/bin/termadm']),
        ('/usr/share/termgr', [
            'files/usr/share/termgr/check.wsgi',
            'files/usr/share/termgr/mgr.wsgi',
            'files/usr/share/termgr/query.wsgi',
            'files/usr/share/termgr/setup.wsgi']),
        ('/etc/uwsgi/apps-available', [
            'files/etc/uwsgi/apps-available/termcheck.ini',
            'files/etc/uwsgi/apps-available/termgr.ini',
            'files/etc/uwsgi/apps-available/termquery.ini',
            'files/etc/uwsgi/apps-available/termsetup.ini'])],
    description=('Homeinfo Terminal Manager'))
