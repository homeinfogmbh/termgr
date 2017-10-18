#! /usr/bin/env python3
"""Terminal query interface"""

from wsgilib import WsgiApp
from termgr.wsgi.query import QueryHandler

application = WsgiApp(QueryHandler, cors=True)
