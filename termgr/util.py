"""Termgr common utilities."""

from collections import namedtuple

__all__ = ['Addr', 'TerminalLine', 'TerminalCSVRecord']


SEP = ';'


Addr = namedtuple('Addr', ('street', 'house_number', 'zip_code'))


TerminalLine = namedtuple('TerminalLine', ('city', 'addr', 'scheduled'))


class TerminalCSVRecord(namedtuple('TerminalCSVRecord', (
        'tid', 'cid', 'street', 'house_number', 'zip_code', 'city'))):
    """A terminal CSV record."""

    __slots__ = ()

    def __str__(self):
        """Returns a CSV representation of the respective terminal."""
        return SEP.join(map(lambda col: '' if col is None else str(col), self))

    @classmethod
    def from_terminal(cls, terminal):
        """Creates a TerminalCSV record from the respective terminal."""
        try:
            address = terminal.location.address
        except AttributeError:
            street = None
            house_number = None
            zip_code = None
            city = None
        else:
            street = address.street
            house_number = address.house_number
            zip_code = address.zip_code
            city = address.city

        return cls(terminal.tid, terminal.customer.id, street, house_number,
                   zip_code, city)
