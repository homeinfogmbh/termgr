"""WSGI services."""

from his import Application

from termgr.wsgi import administer
from termgr.wsgi import ddbaccounts
from termgr.wsgi import dephist
from termgr.wsgi import listing
from termgr.wsgi import setup


__all__ = ["ROUTES", "APPLICATION"]


ROUTES = (
    *administer.ROUTES,
    *ddbaccounts.ROUTES,
    *dephist.ROUTES,
    *listing.ROUTES,
    *setup.ROUTES,
)
APPLICATION = Application("termgr", debug=True)
APPLICATION.add_routes(ROUTES)
