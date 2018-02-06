"""WSGI services."""

from wsgilib import Application

from termgr.wsgi import check, query, setup

__all__ = ['APPLICATION']


APPLICATION = Application('termgr', debug=True)
APPLICATION.add_routes(check.ROUTES + query.ROUTES + setup.ROUTES)
