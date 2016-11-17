#! /usr/bin/env python3
"""Terminal checking interface"""

from homeinfo.lib.wsgi import WsgiApp
from termgr.controllers.check import CheckHandler

application = WsgiApp(CheckHandler, cors=True)
