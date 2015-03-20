"""Terminal data storage"""

from .abc import TermgrModel
from peewee import ForeignKeyField, IntegerField, CharField, DoesNotExist
from ipaddress import IPv4Address
from homeinfolib import create, connection
from homeinfo.crm.customer import Customer

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Terminal']

# TODO: Move this into configuration!
vpn = {'keys_dir': '/etc/openvpn/terminals/openssl/keys'}


@create
class Terminal(TermgrModel):
    """CRM's customer(s)"""

    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='terminals')
    """The customer this terminal belongs to"""
    tid = IntegerField(11)
    """The terminal ID"""
    domain = CharField(64)
    """The terminal's domain"""
    _ipv4addr = IntegerField(11, db_column='ipv4addr')
    """The terminal's IPv4 address"""

    def __repr__(self):
        """Converts the terminal to a unique string"""
        return '.'.join([str(ident) for ident in self.idents])

    @classmethod
    def by_ids(cls, cid, tid):
        """Get a terminal by customer id and terminal id"""
        with connection(Terminal), connection(Customer):
            try:
                term = Terminal.get(Terminal.customer == cid,
                                    Terminal.tid == tid)
            except DoesNotExist:
                term = None
        return term

    @property
    def cid(self):
        """Returns the customer's ID"""
        with connection(Customer):
            return self.customer.id

    @property
    def idents(self):
        """Returns the terminals identifiers"""
        return (self.tid, self.cid)

    @property
    def hostname(self):
        """Generates and returns the terminal's host name"""
        return '.'.join([str(self.tid), str(self.cid), self.domain])

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address"""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address"""
        self._ipv4addr = int(ipv4addr)
