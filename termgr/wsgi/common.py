"""Common WSGI functions."""

from flask import request

from mdb import Customer
from terminallib import Terminal
from wsgilib import Error

from termgr.orm import AuthenticationError, User

__all__ = [
    'get_user',
    'get_customer',
    'get_terminal',
    'authenticated',
    'authorized']


INVALID_CREDENTIALS = Error('Invalid user name and / or password.', status=401)


def get_user():
    """Returns the appropriate user."""

    try:
        passwd = request.json['passwd']
    except KeyError:
        raise INVALID_CREDENTIALS

    try:
        user_name = request.json['user_name']
    except KeyError:
        raise INVALID_CREDENTIALS

    try:
        return User.authenticate(user_name, passwd)
    except AuthenticationError:
        raise INVALID_CREDENTIALS


def get_customer(json=None):
    """Returns the respective customer."""

    if json is None:
        json = request.json

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

    try:
        tid = request.json['tid']
    except KeyError:
        raise Error('No TID specified.')

    try:
        return Terminal.get(
            (Terminal.customer == get_customer(json=request.json))
            & (Terminal.tid == tid))
    except Terminal.DoesNotExist:
        raise Error('No such terminal.', status=404)


def authenticated(function):
    """Enforces a terminal manager user login."""

    def wrapper(*args, **kwargs):
        """Calls the function with additional user parameter."""
        return function(get_user(), *args, **kwargs)

    return wrapper


def authorized(read=None, administer=None, setup=None):
    """Enforces a terminal authorization."""

    def wrap(function):
        """Wraps the actual function."""
        def wrapper(user, *args, **kwargs):
            """Performs terminal check and runs function."""
            terminal = get_terminal()

            if user.authorize(
                    terminal, read=read, administer=administer, setup=setup):
                return function(terminal, *args, **kwargs)

            raise Error('Terminal operation unauthorized.', status=403)

        return wrapper

    return wrap
