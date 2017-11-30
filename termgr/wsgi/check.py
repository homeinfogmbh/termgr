"""Terminal checking web service."""

from collections import defaultdict

from flask import request, jsonify, Flask
from peewee import DoesNotExist

from terminallib import Terminal, RemoteController

from termgr.orm import AuthenticationError, User

__all__ = ['APPLICATION']


APPLICATION = Flask('termcheck')


def group_terminals(terminals):
    """Groups the respective terminals by customers."""

    grouped = defaultdict(list)

    for terminal in terminals:
        grouped[terminal.customer].append(terminal)

    return grouped


def dict_terminals(grouped_terminals):
    """Converts grouped terminals into JSON compliant dictionaries."""

    return {'customers': [{
        'id': customer.id, 'name': customer.name,
        'terminals': [{
            'id': terminal.tid,
            'location': repr(terminal.location)}
            for terminal in terminals]}
        for customer, terminals in grouped_terminals.items()]}


def authorized_terminals(user):
    """Yields terminals readable by the respective user."""

    for terminal in Terminal:
        if user.authorize(terminal, read=True):
            yield terminal


def identify_terminal(terminal):
    """Indentifies the respective terminal."""

    return RemoteController('termgr', terminal).execute(
        '/usr/bin/sudo /usr/bin/beep')


@APPLICATION.route('/')
def check_terminal():
    """Checks the terminals."""

    try:
        user = User.authenticate(
            request.args['user_name'], request.args['passwd'])
    except AuthenticationError:
        return ('Invalid user name and / or password.', 401)

    action = request.args.get('action')

    if action == 'list':
        return jsonify(dict_terminals(group_terminals(
            authorized_terminals(user))))
    elif action == 'identify':
        try:
            terminal = Terminal.get(
                (Terminal.customer == request.args.get('cid'))
                & (Terminal.tid == request.args.get('tid')))
        except DoesNotExist:
            return ('No such terminal.', 404)

        if user.authorize(terminal, read=True):
            if identify_terminal(terminal):
                return 'Display should have beeped.'

            return ('Could not get display to beep.', 500)

        return ('You are not authorized to identify this terminal.', 403)

    return ('Invalid action: {}.'.format(action), 400)
