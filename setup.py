#! /usr/bin/env python3

from distutils.core import setup

# OS-independent setup only here!
setup(
    name='termgr',
    version='0.1.0-indev',
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    packages=['termgr'],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Manager')
    )
