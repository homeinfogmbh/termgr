"""WSGI services."""

from wsgilib import Application

from termgr.wsgi import administer, list, setup


__all__ = ['ROUTES', 'APPLICATION']


ROUTES = administer.ROUTES + list.ROUTES + setup.ROUTES
APPLICATION = Application('termgr', cors=True, debug=True)
APPLICATION.add_routes(ROUTES)
