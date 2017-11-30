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
    scripts=[
        'files/termacls', 'files/termgr', 'files/termadm', 'files/termcheckd',
        'files/termqueryd'],
    data_files=[
        ('/usr/share/termgr', [
            'files/setup.wsgi']),
        ('/etc/uwsgi/apps-available', [
            'files/termsetup.ini']),
        ('/usr/lib/systemd/system', [
            'files/termcheck.service',
            'files/termquery.service'])],
    description=('Homeinfo Terminal Manager'))
