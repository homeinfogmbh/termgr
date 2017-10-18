#! /usr/bin/env python3
"""Terminal checking interface"""

from wsgilib import WsgiApp
from termgr.wsgi.check import CheckHandler

application = WsgiApp(CheckHandler, cors=True)
