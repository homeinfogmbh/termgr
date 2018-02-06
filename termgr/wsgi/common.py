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


def _get_container(legacy):
    """Returns the respective request data container."""

    return request.args if legacy else DATA.json


def get_user(legacy=False):
    """Returns the appropriate user."""

    container = _get_container(legacy)

    try:
        passwd = container['passwd']
    except KeyError:
        raise Error('No password specified.')

    try:
        user_name = container['user_name']
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


def get_customer(legacy=False):
    """Returns the respective customer."""

    container = _get_container(legacy)

    try:
        cids = container['cid'].split(':')
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


def get_terminal(legacy=False):
    """Returns the respective terminal."""

    container = _get_container(legacy)

    try:
        tid = container['tid']
    except KeyError:
        raise Error('No TID specified.')

    try:
        return Terminal.get(
            (Terminal.customer == get_customer(legacy=legacy))
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
