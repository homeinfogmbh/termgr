"""Terminal query web service"""

from homeinfo.lib.wsgi import WsgiApp, Error, OK
from homeinfo.terminals.orm import Terminal, AddressUnconfiguredError

from ..lib import dom
from ..orm import User

__all__ = ['TerminalQuery']


class TerminalQuery(WsgiApp):
    """Controller for terminal queries"""

    DEBUG = True

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)

    def get(self, environ):
        """Interpret query dictionary"""
        query_string = self.query_string(environ)
        qd = self.qd(query_string)
        user_name = qd.get('user_name')

        if not user_name:
            return Error('No user name specified', status=400)

        passwd = qd.get('passwd')

        if not passwd:
            return Error('No password specified', status=400)

        user = User.authenticate(user_name, passwd)

        if user:
            cid_str = qd.get('cid')

            try:
                cid = int(cid_str)
            except ValueError:
                return Error(
                    'Not a customer ID: {0}'.format(cid_str), status=400)
            except TypeError:
                cid = None  # all customers

            terminals_dom = dom.terminals()

            for terminal in self.terminals(cid, user):
                terminal_dom = self.term2dom(terminal)
                terminals_dom.terminal.append(terminal_dom)

            return OK(terminals_dom, content_type='application/xml')
        else:
            return Error('Invalid credentials', status=401)

    def terminals(self, cid, user):
        """List terminals of customer with CID"""
        if cid is None:
            for terminal in Terminal:
                if not terminal.testing:
                    if user.authorize(terminal, read=True):
                        yield terminal
        else:
            for terminal in Terminal.select().where(
                    (Terminal.customer == cid) &
                    (Terminal.testing == 0)):
                if user.authorize(terminal, read=True):
                    yield terminal

    def term2dom(self, terminal, status=False):
        """Formats a terminal to a DOM"""
        terminal_dom = dom.TerminalInfo()

        if terminal.location is not None:
            address_dom = dom.Address()
            address_dom.street = terminal.location.address.street
            address_dom.house_number = terminal.location.address.house_number
            address_dom.city = terminal.location.address.city
            address_dom.zip_code = terminal.location.address.zip_code
            terminal_dom.location = address_dom
        else:
            terminal_dom.location = None

        terminal_dom.annotation = terminal.annotation
        terminal_dom.tid = terminal.tid
        terminal_dom.deployed = terminal.deployed

        if status:
            # This is slow!
            terminal_dom.status = terminal.status

        terminal_dom.cid = terminal.customer.id

        return terminal_dom
