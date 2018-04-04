"""Termgr common utilities."""

from collections import namedtuple

__all__ = ['Addr', 'TerminalLine', 'TerminalCSVRecord']


SEP = ';'


def _stringify(value):
    """Returns the string representation of not-None values."""

    if value is None:
        return ''

    return str(value)


class Addr(namedtuple('Addr', ('street', 'house_number', 'zip_code'))):
    """An address respresentation."""

    @classmethod
    def from_address(cls, address):
        """Creates the respective address tuple from the given address."""
        if not address:
            return None

        return cls(address.street, address.house_number, address.zip_code)


TerminalLine = namedtuple('TerminalLine', ('city', 'addr', 'scheduled'))


class TerminalCSVRecord(namedtuple('TerminalCSVRecord', (
        'tid', 'cid', 'street', 'house_number', 'zip_code', 'city'))):
    """A terminal CSV record."""

    def __str__(self):
        """Returns a CSV representation of the respective terminal."""
        return SEP.join(map(_stringify, self))

    @classmethod
    def from_terminal(cls, terminal):
        """Creates a TerminalCSV record from the respective terminal."""
        addr = None

        if terminal.location:
            addr = Addr.from_address(terminal.location.address)

        return cls(terminal.tid, terminal.customer.cid, address.street,
                   address.house_number, address.zip_code, address.city)
