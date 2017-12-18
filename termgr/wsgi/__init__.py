"""WSGI services."""

from wsgilib import Application

from termgr.wsgi import check, query, setup

__all__ = ['APPLICATION']


APPLICATION = Application('termgr', debug=True)

for route, method, function in check.ROUTES + query.ROUTES + setup.ROUTES:
    APPLICATION.route(route, methods=[method])(function)
