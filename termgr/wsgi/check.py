"""Terminal checking web service."""

from collections import defaultdict

from terminallib import Terminal
from wsgilib import JSON

from termgr.ctrl import TerminalController
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

    return {
        str(customer.id): {
            'id': customer.id,
            'name': customer.name,
            'terminals': [{
                'tid': terminal.tid,
                'cid': customer.id,
                'address': terminal.address.to_json(),
                'annotation': terminal.annotation}
                          for terminal in terminals]}
        for customer, terminals in grouped_terminals.items()}


def authorized_terminals(user):
    """Yields terminals readable by the respective user."""

    for terminal in Terminal.select().where(~(Terminal.address >> None)):
        if user.authorize(terminal, read=True):
            yield terminal


@authenticated
def list_terminals(user):
    """Checks the terminals."""

    return JSON(dict_terminals(group_terminals(
        authorized_terminals(user))))


@authenticated
@authorized(read=True)
def identify_terminal(terminal):
    """Identifies the respective terminal by beep test."""

    if TerminalController(terminal).sudo('/usr/bin/beep'):
        return 'Display should have beeped.'

    return ('Could not get display to beep.', 500)


ROUTES = (
    ('POST', '/check/list', list_terminals, 'list_terminals'),
    ('POST', '/check/identify', identify_terminal, 'identify_terminal'))
