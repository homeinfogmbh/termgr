"""Common WSGI functions."""

from flask import request

from homeinfo.crm import Customer
from terminallib import Terminal
from wsgilib import Error, PostData

from termgr.orm import AuthenticationError, User

__all__ = [
    'DATA',
    'get_user',
    'get_action',
    'get_customer',
    'get_terminal',
    'authenticated',
    'authorized']


DATA = PostData()


def get_user():
    """Returns the appropriate user."""

    json = DATA.json

    try:
        passwd = json['passwd']
    except KeyError:
        raise Error('No password specified.')

    try:
        user_name = json['user_name']
    except KeyError:
        raise Error('No user name specified.')

    try:
        return User.authenticate(user_name, passwd)
    except AuthenticationError:
        raise Error('Invalid user name and / or password.', status=401)


def get_action():
    """Returns the respective action."""

    try:
        return request.args['action']
    except KeyError:
        raise Error('No action specified.')


def get_customer(json=None):
    """Returns the respective customer."""

    if json is None:
        json = DATA.json

    try:
        cids = json['cid'].split(':')
    except KeyError:
        raise Error('No CID specified.')

    customer = None

    for cid in reversed(cids):
        if customer is None:
            reseller_match = Customer.reseller >> None
        else:
            reseller_match = Customer.reseller == customer

        try:
            customer = Customer.get((Customer.cid == cid) & reseller_match)
        except Customer.DoesNotExist:
            raise Error('No such customer.', status=404)

    return customer


def get_terminal():
    """Returns the respective terminal."""

    json = DATA.json

    try:
        tid = json['tid']
    except KeyError:
        raise Error('No TID specified.')

    try:
        return Terminal.get(
            (Terminal.customer == get_customer(json=json))
            & (Terminal.tid == tid))
    except Terminal.DoesNotExist:
        raise Error('No such terminal.', status=404)


def authenticated(function):
    """Enforces a terminal manager user login."""

    def wrapper(*args, **kwargs):
        """Calls the function with additional user parameter."""
        return function(get_user(), *args, **kwargs)

    return wrapper


def authorized(read=None, administer=None, setup=None, forward_user=False):
    """Enforces a terminal authorization."""

    def wrap(function):
        """Wraps the actual function."""
        def wrapper(user, *args, **kwargs):
            """Performs terminal check and runs function."""
            terminal = get_terminal()

            if user.authorize(
                    terminal, read=read, administer=administer, setup=setup):
                if forward_user:
                    return function(user, terminal, *args, **kwargs)

                return function(terminal, *args, **kwargs)

            raise Error('Terminal operation unauthorized.', status=403)

        return wrapper

    return wrap
