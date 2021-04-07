"""WSGI services."""

from his import Application

from termgr.wsgi import administer, listing, misc, setup


__all__ = ['ROUTES', 'APPLICATION']


ROUTES = (*administer.ROUTES, *listing.ROUTES, *misc.ROUTES, *setup.ROUTES)
APPLICATION = Application('termgr', debug=True)
APPLICATION.add_routes(ROUTES)
