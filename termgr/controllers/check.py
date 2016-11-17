"""Terminal checking web service"""

from peewee import DoesNotExist

from homeinfo.terminals.orm import Terminal
from homeinfo.terminals.ctrl import RemoteController
from homeinfo.lib.wsgi import Error, InternalServerError, JSON, OK, \
    RequestHandler

from termgr.orm import User

__all__ = ['CheckHandler']


class CheckHandler(RequestHandler):
    """Handles requests to check terminals"""

    def get(self):
        """Handles GET requests"""
        try:
            user_name = self.query['user_name']
        except KeyError:
            return Error('No user name provided', status=400)

        try:
            passwd = self.query['passwd']
        except KeyError:
            return Error('No password provided', status=400)

        user = User.authenticate(user_name, passwd)

        if user:
            try:
                action = self.query['action']
            except KeyError:
                return Error('No action specified', status=400)
            else:
                if action == 'list':
                    return self._list(user)
                elif action == 'identify':
                    try:
                        tid = self.query['tid']
                    except KeyError:
                        return Error('No terminal ID specified', status=400)
                    else:
                        try:
                            tid = int(tid)
                        except (ValueError, TypeError):
                            return Error('Terminal ID must be an integer',
                                         status=400)

                    try:
                        cid = self.query['cid']
                    except KeyError:
                        return Error('No customer ID specified', status=400)
                    else:
                        try:
                            cid = int(cid)
                        except (ValueError, TypeError):
                            return Error('Customer ID must be an integer',
                                         status=400)

                    try:
                        terminal = Terminal.by_ids(cid, tid)
                    except DoesNotExist:
                        return Error('No such terminal: {tid}.{cid}'.format(
                            tid=tid, cid=cid), status=400)

                    if user.authorize(terminal, read=True):
                        remote_controller = RemoteController(
                            'termgr', terminal)
                        if remote_controller.execute(
                                '/usr/bin/sudo /usr/bin/beep'):
                            return OK('Display should have beeped')
                        else:
                            return InternalServerError(
                                'Could not get display to beep')
                    else:
                        return Error('You are not authorized to identify '
                                     'this terminal', status=400)
                else:
                    return Error('Invalid action: {}'.format(action),
                                 status=400)
        else:
            return Error('Invalid credentials', status=400)

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
