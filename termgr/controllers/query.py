"""Terminal query web service"""

from homeinfo.lib.wsgi import Error, JSON, RequestHandler
from homeinfo.terminals.orm import Terminal

from termgr.orm import User

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

            terminals = []
            undeployed = self.query.get('undeployed', False)

            for terminal in self.terminals(cid, user, undeployed=undeployed):
                terminals.terminal.append(terminal.to_dict())

            return JSON({'terminals': terminals})
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
