"""Terminal checking web service."""

from terminallib import Terminal, RemoteController
from wsgilib import Error, InternalServerError, JSON, OK

from .abc import TermgrHandler

__all__ = ['CheckHandler']


def group_terminals(terminals):
    """Groups the respective terminals by customers."""

    grouped = {}

    for terminal in terminals:
        try:
            _, customer_terminals = grouped[terminal.customer.id]
        except KeyError:
            grouped[terminal.customer.id] = (terminal.customer, [terminal])
        else:
            customer_terminals.append(terminal)

    return grouped


def list_terminals(grouped_terminals):
    """Lists customer terminals."""

    customers = []

    for customer, terminals in grouped_terminals.items():
        customer_terminals = []

        for terminal in terminals:
            customer_terminals.append({
                'id': terminal.tid, 'location': repr(terminal.location)})

        customers.append({
            'id': customer.id, 'name': customer.name,
            'terminals': customer_terminals})

    return JSON({'customers': customers})


class CheckHandler(TermgrHandler):
    """Handles requests to check terminals."""

    @property
    def terminals(self):
        """Yields terminals readable by the respective user."""
        for terminal in Terminal:
            if self.user.authorize(terminal, read=True):
                yield terminal

    def get(self):
        """Handles GET requests."""
        action = self.action

        if action == 'list':
            return list_terminals(group_terminals(self.terminals))
        elif action == 'identify':
            terminal = self.terminal

            if self.user.authorize(terminal, read=True):
                remote_controller = RemoteController('termgr', terminal)
                result = remote_controller.execute(
                    '/usr/bin/sudo /usr/bin/beep')

                if result:
                    return OK('Display should have beeped.')

                raise InternalServerError(
                    'Could not get display to beep:\n{}'.format(str(result)))

            raise Error('You are not authorized to identify this terminal.',
                        status=400) from None

        raise Error('Invalid action: {}.'.format(action), status=400) from None
