"""Terminal checking web service."""

from terminallib import Terminal, RemoteController
from wsgilib import Error, InternalServerError, JSON, OK

from .abc import TermgrHandler

__all__ = ['CheckHandler']


def list_terminals(user):
    """List customer terminals."""

    # Group terminals to customers
    customers = {}

    for terminal in Terminal:
        if user.authorize(terminal, read=True):
            try:
                _, terminals = customers[terminal.customer.id]
            except KeyError:
                customer, terminals = (terminal.customer, [terminal])
                customers[terminal.customer.id] = (customer, terminals)
            else:
                terminals.append(terminal)

    # Build JSON dict from grouped terminals
    customers_json = []
    json = {'customers': customers_json}

    for cid in customers:
        customer, terminals = customers[cid]
        terminals_json = []

        for terminal in terminals:
            terminal_json = {
                'id': terminal.tid,
                'location': repr(terminal.location)}

            terminals_json.append(terminal_json)

        customer_json = {
            'id': customer.id,
            'name': customer.name,
            'terminals': terminals_json}

        customers_json.append(customer_json)

    return JSON(json)


class CheckHandler(TermgrHandler):
    """Handles requests to check terminals."""

    def get(self):
        """Handles GET requests."""
        action = self.action

        if action == 'list':
            return list_terminals(self.user)
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
