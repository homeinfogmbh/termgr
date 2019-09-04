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
    description=('Homeinfo Terminal Manager'))
