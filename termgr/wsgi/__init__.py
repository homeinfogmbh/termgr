"""WSGI services."""

from his import Application

from termgr.wsgi import administer, dephist, documents, listing, setup


__all__ = ['ROUTES', 'APPLICATION']


ROUTES = (
    *administer.ROUTES, *dephist.ROUTES, *documents.ROUTES, *listing.ROUTES,
    *setup.ROUTES
)
APPLICATION = Application('termgr', debug=True)
APPLICATION.add_routes(ROUTES)
