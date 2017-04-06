#! /usr/bin/env python3
"""Terminal checking interface"""

from wsgilib import WsgiApp
from termgr.controllers.check import CheckHandler

application = WsgiApp(CheckHandler, cors=True)
