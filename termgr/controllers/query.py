"""Terminal query web service"""

from homeinfo.lib.wsgi import Error, JSON, XML, RequestHandler
from homeinfo.terminals.orm import Terminal

from termgr.orm import User
from termgr import dom

__all__ = ['QueryHandler']


class QueryHandler(RequestHandler):
    """Handles requests for the TerminalQuery"""

    def get(self):
        """Interpret query dictionary"""
        user_name = self.query.get('user_name')

        if not user_name:
            raise Error('No user name specified', status=400) from None

        passwd = self.query.get('passwd')

        if not passwd:
            raise Error('No password specified', status=400) from None

        user = User.authenticate(user_name, passwd)

        if user:
            cid_str = self.query.get('cid')

            try:
                cid = int(cid_str)
            except ValueError:
                raise Error('Not a customer ID: {}'.format(
                    cid_str), status=400) from None
            except TypeError:
                cid = None  # all customers

            undeployed = self.query.get('undeployed', False)
            json = self.query.get('json')

            if json is None:
                terminals = dom.terminals()

                for terminal in self.terminals(
                        cid, user, undeployed=undeployed):
                    terminal_dom = dom.Terminal()
                    terminal_dom.tid = terminal.tid
                    terminal_dom.cid = terminal.customer.id
                    terminal_dom.scheduled = terminal.scheduled
                    terminal_dom.deployed = terminal.deployed
                    terminal_dom.annotation = terminal.annotation

                    if terminal.location:
                        terminal_dom.annotation = terminal.location.annotation

                        if terminal.location.address:
                            address = terminal.location.address
                            address_dom = dom.Address()
                            address_dom.street = address.street
                            address_dom.house_number = address.house_number
                            address_dom.zip_code = address.zip_code
                            address_dom.city = address.city
                            terminal_dom.address = address_dom

                    terminals.terminal.append(terminal_dom)

                return XML(terminals)
            else:
                if json is True:
                    indent = None
                else:
                    try:
                        indent = int(json)
                    except ValueError:
                        raise Error('Invalid indentation;: {}'.format(json))

                terminals = []

                for terminal in self.terminals(
                        cid, user, undeployed=undeployed):
                    terminals.append(terminal.to_dict(short=True))

                return JSON(terminals, indent=indent)
        else:
            raise Error('Invalid credentials', status=401) from None

    def terminals(self, cid, user, undeployed=False):
        """List terminals of customer with CID"""
        if cid is None:
            for terminal in Terminal:
                if undeployed and terminal.deployed is not None:
                    continue

                if not terminal.testing:
                    if user.authorize(terminal, read=True):
                        yield terminal
        else:
            for terminal in Terminal.select().where(
                    (Terminal.customer == cid) &
                    (Terminal.testing == 0)):
                if undeployed and terminal.deployed is not None:
                    continue

                if user.authorize(terminal, read=True):
                    yield terminal
