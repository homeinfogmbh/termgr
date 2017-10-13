"""Web application for terminal management."""

from peeweeplus import FieldValueError
from terminallib import Terminal
from wsgilib import OK, JSON, RestHandler

from .abc import TermgrHandler


class TerminalHandler(TermgrHandler):
    """Handles listing and creation of terminals."""

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
