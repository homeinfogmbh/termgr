#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='termgr',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    packages=['termgr', 'termgr.wsgi'],
    scripts=['files/termacls', 'files/termgr', 'files/termadm'],
    data_files=[
        ('/usr/share/termgr', [
            'files/check.wsgi',
            'files/query.wsgi',
            'files/setup.wsgi']),
        ('/etc/uwsgi/apps-available', [
            'files/termcheck.ini',
            'files/termquery.ini',
            'files/termsetup.ini'])],
    description=('Homeinfo Terminal Manager'))
