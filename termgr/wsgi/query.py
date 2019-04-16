"""Terminal query web service."""

from datetime import datetime

from flask import request
from terminallib import System

from wsgilib import JSON, Error

from termgr.auth import authorize
from termgr.wsgi.common import authenticated

__all__ = ['ROUTES']


def get_scheduled():
    """Returns the scheduled date."""

    try:
        scheduled = request.args['scheduled']
    except KeyError:
        return None

    try:
        scheduled = datetime.strptime(scheduled, '%Y-%m-%d')
    except ValueError:
        raise Error('Invalid ISO date: {}.'.format(scheduled))

    return scheduled.date()


def get_systems(account):
    """List systems of customer with CID."""

    for system in System:
        if authorize(account, system, read=True):
            yield system


@authenticated
def query_systems(account):
    """Lists the respective systems."""

    return JSON([system.to_json() for system in get_systems(account)])


ROUTES = (('POST', '/query', query_systems),)
