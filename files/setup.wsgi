#! /usr/bin/env python3
"""Terminal setup interface"""

from wsgilib import WsgiApp
from termgr.controllers.setup import SetupHandler

application = WsgiApp(SetupHandler, cors=True)
