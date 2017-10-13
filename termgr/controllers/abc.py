"""Abstract base classes."""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from terminallib import Terminal
from wsgilib import Error, RequestHandler

from termgr.orm import AuthenticationError, User

__all__ = ['TermgrHandler']


class TermgrHandler(RequestHandler):
    """User aware handler."""

    @property
    def user(self):
        """Returns the user."""
        try:
            user_name = self.query['user_name']
        except KeyError:
            raise Error('No user name specified.', status=400) from None

        try:
            passwd = self.query['passwd']
        except KeyError:
            raise Error('No password specified.', status=400) from None

        try:
            return User.authenticate(user_name, passwd)
        except AuthenticationError:
            raise Error('Invalid credentials.', status=401) from None

    @property
    def cid(self):
        """Returns the customer ID."""
        try:
            cid = self.query['cid']
        except KeyError:
            raise Error('No customer ID specified.', status=400) from None
        else:
            try:
                return int(cid)
            except ValueError:
                raise Error('Invalid customer ID.', status=400) from None

    @property
    def customer(self):
        """Returns the respective customer."""
        try:
            return Customer.get(Customer.id == self.cid)
        except DoesNotExist:
            raise Error('No such customer.', status=404) from None

    @property
    def terminals(self):
        """Lists available terminals."""
        for terminal in Terminal.select(Terminal.customer == self.customer):
            yield terminal

    @property
    def tid(self):
        """Returns the terminal ID."""
        try:
            tid = self.query['tid']
        except KeyError:
            raise Error('No terminal ID specified.', status=400) from None
        else:
            try:
                return int(tid)
            except ValueError:
                raise Error('Invalid terminal ID.', status=400) from None

    @property
    def terminal(self):
        """Returns the appropriate terminal."""
        try:
            return Terminal.get(
                (Terminal.customer == self.customer) &
                (Terminal.tid == self.tid) &
                (Terminal.deleted >> None))
        except DoesNotExist:
            raise Error('No such terminal.', status=404) from None
