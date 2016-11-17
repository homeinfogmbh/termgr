#! /usr/bin/env python3
"""Terminal setup interface"""

from homeinfo.lib.wsgi import WsgiApp
from termgr.controllers.setup import SetupHandler

application = WsgiApp(SetupHandler, cors=True)
