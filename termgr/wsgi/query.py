"""Terminal query web service."""

from datetime import datetime

from flask import request
from terminallib import Terminal

from wsgilib import JSON, XML, Error

from termgr import dom
from termgr.wsgi.common import authenticated

__all__ = ['ROUTES']


def terminals_to_dom(terminals):
    """Returns terminals as XML response."""

    terminals_dom = dom.terminals()

    for terminal in terminals:
        terminal_dom = dom.Terminal()
        terminal_dom.tid = terminal.tid
        terminal_dom.cid = terminal.customer.id
        terminal_dom.scheduled = terminal.scheduled
        terminal_dom.deployed = terminal.deployed
        terminal_dom.annotation = terminal.annotation
        address = terminal.address

        if address:
            address_dom = dom.Address()
            address_dom.street = address.street
            address_dom.house_number = address.house_number
            address_dom.zip_code = address.zip_code
            address_dom.city = address.city
            terminal_dom.address = address_dom

        terminals_dom.terminal.append(terminal_dom)

    return terminals_dom


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


def get_terminals(user):
    """List terminals of customer with CID."""

    scheduled = get_scheduled()
    cid = request.args['cid']
    expression = Terminal.testing == 0

    if cid is not None:
        expression &= Terminal.customer == cid

    if scheduled is not None:
        expression &= Terminal.scheduled == scheduled

    if request.args.get('undeployed', False):
        expression &= Terminal.deployed >> None

    for terminal in Terminal.select().where(expression):
        if user.authorize(terminal, read=True):
            yield terminal


@authenticated
def query_terminals(user):
    """Lists the respective terminals."""

    if request.args.get('json'):
        return JSON([
            terminal.to_json(short=True) for terminal in get_terminals(user)])

    return XML(terminals_to_dom(get_terminals(user)))


ROUTES = (('POST', '/query', query_terminals, 'query_terminals'),)
