"""Common WSGI functions."""

from flask import request

from his import Account
from mdb import Customer
from terminallib import System
from wsgilib import Error, JSON

from termgr.auth import authorize


__all__ = [
    'get_account',
    'get_customer',
    'get_system',
    'get_address',
    'authenticated',
    'authorized']


INVALID_CREDENTIALS = Error(
    'Invalid account name and / or password.', status=401)


def get_account():
    """Returns the appropriate account."""

    try:
        name = request.json['userName']
    except KeyError:
        raise INVALID_CREDENTIALS

    try:
        account = Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise INVALID_CREDENTIALS

    try:
        passwd = request.json['passwd']
    except KeyError:
        raise INVALID_CREDENTIALS

    if account.login(passwd):
        return account

    raise INVALID_CREDENTIALS


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
        raise Error('No TID specified.')

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


def authenticated(function):
    """Enforces an account login."""

    def wrapper(*args, **kwargs):
        """Calls the function with additional account parameter."""
        return function(get_account(), *args, **kwargs)

    return wrapper


def authorized(read=None, administer=None, setup=None):
    """Enforces a system authorization."""

    def wrap(function):
        """Wraps the actual function."""
        def wrapper(account, *args, **kwargs):
            """Performs system check and runs function."""
            system = get_system()

            if authorize(
                    account, system, read=read, administer=administer,
                    setup=setup):
                return function(system, *args, **kwargs)

            raise Error('System operation unauthorized.', status=403)

        return wrapper

    return wrap
