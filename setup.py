#! /usr/bin/env python3

from setuptools import setup

setup(
    name='termgr',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configlib',
        'emaillib',
        'flask',
        'hipster',
        'his',
        'hwdb',
        'mdb',
        'peewee',
        'peeweeplus',
        'setuptools',
        'termacls',
        'wgtools',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    packages=['termgr', 'termgr.wsgi'],
    entry_points={'console_scripts': [
        'dephist = termgr.dephist:main',
        'reload-terminals = termgr.wireguard:update_peers',
        'toggle-ddb-install-account = termgr.ddbaccount:main'
    ]},
    description='Homeinfo Terminal Manager'
)
