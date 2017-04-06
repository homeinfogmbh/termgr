"""Terminal checking web service"""

from peewee import DoesNotExist

from homeinfo.terminals.orm import Terminal
from homeinfo.terminals.ctrl import RemoteController
from wsgilib import Error, InternalServerError, JSON, OK, RequestHandler

from termgr.orm import User

__all__ = ['CheckHandler']


class CheckHandler(RequestHandler):
    """Handles requests to check terminals"""

    def get(self):
        """Handles GET requests"""
        try:
            user_name = self.query['user_name']
        except KeyError:
            raise Error('No user name provided', status=400) from None

        try:
            passwd = self.query['passwd']
        except KeyError:
            raise Error('No password provided', status=400) from None

        user = User.authenticate(user_name, passwd)

        if user:
            try:
                action = self.query['action']
            except KeyError:
                raise Error('No action specified', status=400) from None
            else:
                if action == 'list':
                    return self._list(user)
                elif action == 'identify':
                    try:
                        tid = self.query['tid']
                    except KeyError:
                        raise Error('No terminal ID specified',
                                    status=400) from None
                    else:
                        try:
                            tid = int(tid)
                        except (ValueError, TypeError):
                            raise Error('Terminal ID must be an integer',
                                        status=400) from None

                    try:
                        cid = self.query['cid']
                    except KeyError:
                        raise Error('No customer ID specified',
                                    status=400) from None
                    else:
                        try:
                            cid = int(cid)
                        except (ValueError, TypeError):
                            raise Error('Customer ID must be an integer',
                                        status=400) from None

                    try:
                        terminal = Terminal.by_ids(cid, tid)
                    except DoesNotExist:
                        raise Error('No such terminal: {tid}.{cid}'.format(
                            tid=tid, cid=cid), status=400) from None

                    if user.authorize(terminal, read=True):
                        remote_controller = RemoteController(
                            'termgr', terminal)
                        result = remote_controller.execute(
                            '/usr/bin/sudo /usr/bin/beep')

                        if result:
                            return OK('Display should have beeped')
                        else:
                            raise InternalServerError(
                                'Could not get display to beep:\n{}'.format(
                                    str(result)))
                    else:
                        raise Error('You are not authorized to identify '
                                    'this terminal', status=400) from None
                else:
                    raise Error('Invalid action: {}'.format(action),
                                status=400) from None
        else:
            raise Error('Invalid credentials', status=400) from None

    def _list(self, user):
        """List customer terminals"""
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
