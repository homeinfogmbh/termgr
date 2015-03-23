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
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
