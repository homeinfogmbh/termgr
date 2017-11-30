"""Terminal query web service."""

from datetime import datetime

from flask import request, jsonify, Response, Flask
from terminallib import Terminal

from termgr import dom
from termgr.orm import AuthenticationError, User

__all__ = ['APPLICATION']


APPLICATION = Flask('termquery')


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

        if terminal.location:
            address_dom = dom.Address()
            address_dom.annotation = terminal.location.annotation

            if terminal.location.address:
                address = terminal.location.address
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
        raise ValueError('Invalid ISO date: {}.'.format(scheduled)) from None

    return scheduled.date()


def get_terminals(user):
    """List terminals of customer with CID."""

    scheduled = get_scheduled()
    undeployed = request.args.get('undeployed', False)
    cid = request.args.query['cid']

    if cid is None:
        terminals = Terminal
    else:
        terminals = Terminal.select().where(
            (Terminal.customer == cid) & (Terminal.testing == 0))

    for terminal in terminals:
        if terminal.testing:
            continue

        if scheduled is not None:
            if terminal.scheduled is None:
                continue
            elif terminal.scheduled.date() != scheduled:
                continue

        if undeployed and terminal.deployed is not None:
            continue

        if user.authorize(terminal, read=True):
            yield terminal


@APPLICATION.route('/')
def list_terminals():
    """Lists the respective terminals."""

    try:
        user = User.authenticate(
            request.args['user_name'], request.args['passwd'])
    except AuthenticationError:
        return ('Invalid user name and / or password.', 401)

    if request.args.get('json'):
        return jsonify(
            [terminal.to_dict(short=True) for terminal in get_terminals(user)])

    xml = terminals_to_dom(get_terminals(user)).toxml()
    return Response(xml, mimetype='application/xml')
