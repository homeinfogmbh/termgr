"""Common WSGI functions."""

from flask import request
from peewee import DoesNotExist

from homeinfo.crm import Customer
from terminallib import Terminal
from wsgilib import DATA, Error

from termgr.orm import AuthenticationError, User

__all__ = ['get_user', 'get_action', 'get_customer', 'get_terminal']


def get_user(legacy=False):
    """Returns the appropriate user."""

    if legacy:
        contaner = request.args
    else:
        container = DATA.json

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


def get_customer():
    """Returns the respective customer."""

    try:
        cids = request.args['cid'].split(':')
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
        except DoesNotExist:
            raise Error('No such customer.', status=404)

    return customer


def get_terminal():
    """Returns the respective terminal."""

    try:
        tid = request.args['tid']
    except KeyError:
        raise Error('No TID specified.')

    try:
        return Terminal.get(
            (Terminal.customer == get_customer()) & (Terminal.tid == tid))
    except DoesNotExist:
        raise Error('No such terminal.', status=404)
