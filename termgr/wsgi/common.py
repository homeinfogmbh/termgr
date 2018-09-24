"""Common WSGI functions."""

from json import loads

from flask import request

from his import Account
from mdb import Customer
from terminallib import Terminal
from wsgilib import Error

from termgr.auth import authorize


__all__ = [
    'get_json',
    'get_account',
    'get_customer',
    'get_terminal',
    'authenticated',
    'authorized']


INVALID_CREDENTIALS = Error(
    'Invalid account name and / or password.', status=401)


def get_json():
    """Returns the JSON post data."""

    json = request.json

    if json is None:
        return loads(request.get_data().decode())

    return json


def get_account():
    """Returns the appropriate account."""

    json = get_json()

    try:
        name = json['userName']
    except KeyError:
        try:
            name = json['user_name']
        except KeyError:
            raise INVALID_CREDENTIALS

    try:
        account = Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise INVALID_CREDENTIALS

    try:
        passwd = json['passwd']
    except KeyError:
        raise INVALID_CREDENTIALS

    return account.login(passwd)


def get_customer():
    """Returns the respective customer."""

    json = get_json()

    try:
        cid = int(json['cid'])
    except (KeyError, TypeError):
        raise Error('No CID specified.')
    except ValueError:
        raise Error('CID must be an interger.')

    try:
        return Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise Error('No such customer.', status=404)


def get_terminal():
    """Returns the respective terminal."""

    json = get_json()

    try:
        tid = json['tid']
    except KeyError:
        raise Error('No TID specified.')

    try:
        return Terminal.get(
            (Terminal.customer == get_customer())
            & (Terminal.tid == tid))
    except Terminal.DoesNotExist:
        raise Error('No such terminal.', status=404)


def authenticated(function):
    """Enforces a terminal manager account login."""

    def wrapper(*args, **kwargs):
        """Calls the function with additional account parameter."""
        return function(get_account(), *args, **kwargs)

    return wrapper


def authorized(read=None, administer=None, setup=None):
    """Enforces a terminal authorization."""

    def wrap(function):
        """Wraps the actual function."""
        def wrapper(account, *args, **kwargs):
            """Performs terminal check and runs function."""
            terminal = get_terminal()

            if authorize(
                    account, terminal, read=read, administer=administer,
                    setup=setup):
                return function(terminal, *args, **kwargs)

            raise Error('Terminal operation unauthorized.', status=403)

        return wrapper

    return wrap
