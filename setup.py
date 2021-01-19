#! /usr/bin/env python3

from setuptools import setup

setup(
    name='termgr',
    use_scm_version={
        "root": "..",
        "relative_to": __file__,
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configlib',
        'emaillib',
        'flask',
        'functoolsplus',
        'hipster',
        'his',
        'hwdb',
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
    entry_points={'console_scripts': ['dephist = termgr.dephist:main']},
    description=('Homeinfo Terminal Manager')
)
