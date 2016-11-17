#! /usr/bin/env python3
"""Terminal query interface"""

from homeinfo.lib.wsgi import WsgiApp
from termgr.controllers.query import QueryHandler

application = WsgiApp(QueryHandler, cors=True)
