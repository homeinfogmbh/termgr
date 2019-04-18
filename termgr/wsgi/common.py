"""Common WSGI functions."""

from functools import wraps

from flask import request

from his import ACCOUNT
from mdb import Customer
from terminallib import System
from wsgilib import Error, JSON

from termgr.auth import chkadmin, chkdeploy, chksetup


__all__ = [
    'get_customer',
    'get_system',
    'get_address',
    'admin',
    'setup',
    'deploy']


def get_customer():
    """Returns the respective customer."""

    ident = request.json.get('customer')

    if ident is None:
        raise Error('No customer ID specified.')

    try:
        return Customer[ident]
    except Customer.DoesNotExist:
        raise Error('No such customer.', status=404)


def get_system():
    """Returns the respective system."""

    ident = request.json.get('system')

    if ident is None:
        raise Error('No system specified.')

    try:
        return System[ident]
    except System.DoesNotExist:
        raise Error('No such system.', status=404)


def get_address():
    """Returns an address from JSON data."""

    try:
        address = request.json['address']
    except KeyError:
        raise Error('No address specified.')

    if address is None:
        return None

    missing_keys = set()
    address = []

    for key in ('street', 'houseNumber', 'zipCode', 'city'):
        value = address.pop(key, None)

        if value:
            address.append(value)
        else:
            missing_keys.add(key)

    if missing_keys:
        json = {'message': 'Missing keys.', 'keys': tuple(missing_keys)}
        raise JSON(json, status=400)

    if address:
        json = {'message': 'Superfluous keys.', 'keys': tuple(address)}
        raise JSON(json, status=400)

    return tuple(address)


def admin(function):
    """Wraps the actual with admin permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = get_system()

        if chkadmin(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error('Administration unauthorized.', status=403)

    return wrapper


def setup(function):
    """Wraps the actual with setup permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = get_system()

        if chksetup(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error('Setup operation unauthorized.', status=403)

    return wrapper


def deploy(function):
    """Wraps the actual with deployment permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = get_system()
        customer = get_customer()

        if chkdeploy(ACCOUNT, system, customer):
            return function(system, customer, *args, **kwargs)

        raise Error('Setup operation unauthorized.', status=403)

    return wrapper
