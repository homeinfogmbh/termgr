"""Web application for terminal management."""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from peeweeplus import FieldValueError
from terminallib import Terminal
from wsgilib import Error, OK, JSON, RestHandler


class TerminalHandler(RestHandler):
    """Handles listing and creation of terminals."""

    @property
    def cid(self):
        """Returns the customer ID."""
        try:
            return int(self.query.get('cid'))
        except TypeError:
            raise Error('No customer ID specified.') from None
        except ValueError:
            raise Error('Invalid customer ID specified.') from None

    @property
    def tid(self):
        """Returns the terminal ID."""
        try:
            return int(self.resource)
        except TypeError:
            raise Error('No terminal ID specified.') from None
        except ValueError:
            raise Error('Invalid terminal ID specified.') from None

    @property
    def customer(self):
        """Returns the respective customer."""
        try:
            return Customer.get(Customer.id == self.cid)
        except DoesNotExist:
            raise Error('No such customer.', status=404) from None

    @property
    def terminal(self):
        """Returns a single terminal."""
        try:
            return Terminal.get(Terminal.id == self.tid)
        except DoesNotExist:
            raise Error('No such terminal.', status=404) from None

    @property
    def terminals(self):
        """Lists available terminals."""
        for terminal in Terminal.select(Terminal.customer == self.customer):
            yield terminal

    def get(self):
        """Lists terminals."""
        if self.resource is None:
            return JSON([terminal.to_dict() for terminal in self.terminals])

        return JSON(self.terminal.to_dict())

    def post(self):
        """Requests a new terminal."""
        try:
            terminal = Terminal.from_dict(self.data.json)
        except FieldValueError as field_value_error:
            return JSON(field_value_error.to_dict(), status=422)
        else:
            return JSON(terminal.to_dict())

    def patch(self):
        """Modifies terminal data."""
        try:
            self.terminal.patch(self.data.json)
        except FieldValueError as field_value_error:
            return JSON(field_value_error.to_dict(), status=422)
        else:
            return OK()


class TerminalManager(RestHandler):
    """Generates OpenVPN keys for the respective terminal."""

    def get(self):
        """Returns an OpenVPN key pair for the respective terminal."""
        return self.generate_key()
