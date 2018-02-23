"""WSGI services."""

from wsgilib import Application

from termgr.wsgi import administer, check, query, setup

__all__ = ['ROUTES', 'APPLICATION']


ROUTES = administer.ROUTES + check.ROUTES + query.ROUTES + setup.ROUTES
APPLICATION = Application('termgr', cors=True, debug=True)
APPLICATION.add_routes(ROUTES)
