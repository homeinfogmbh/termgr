"""Terminal checking web service."""

from collections import defaultdict

from terminallib import Terminal, RemoteController
from wsgilib import JSON

from termgr.wsgi.common import get_user, get_action, get_terminal

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


def check_terminal(action):
    """Checks the terminals."""

    user = get_user()

    if action == 'list':
        return JSON(dict_terminals(group_terminals(
            authorized_terminals(user))))
    elif action == 'identify':
        terminal = get_terminal()

        if user.authorize(terminal, read=True):
            if identify_terminal(terminal):
                return 'Display should have beeped.'

            return ('Could not get display to beep.', 500)

        return ('You are not authorized to identify this terminal.', 403)

    return ('Invalid action: {}.'.format(action), 400)


ROUTES = (('/check/<action>', 'POST', check_terminal),)
