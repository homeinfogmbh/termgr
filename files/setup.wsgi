#! /usr/bin/env python3
"""Terminal setup interface"""

from wsgilib import WsgiApp
from termgr.wsgi.setup import SetupHandler

application = WsgiApp(SetupHandler, cors=True)
