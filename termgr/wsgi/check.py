"""Terminal checking web service."""

from collections import defaultdict

from terminallib import Terminal, RemoteController
from wsgilib import JSON

from termgr.wsgi.common import authenticated, authorized

__all__ = ['ROUTES']


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


@authenticated
def list_terminals(user):
    """Checks the terminals."""

    return JSON(dict_terminals(group_terminals(
        authorized_terminals(user))))


@authorized(read=True)
@authenticated
def identify_terminal(terminal):
    """Identifies the respective terminal by beep test."""

    if identify_terminal(terminal):
        return 'Display should have beeped.'

    return ('Could not get display to beep.', 500)


ROUTES = (
    ('POST', '/check/list', list_terminals, 'list_terminals'),
    ('POST', '/check/identify', identify_terminal, 'identify_terminal'))
