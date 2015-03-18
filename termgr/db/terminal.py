"""Terminal data storage"""

from .abc import TermgrModel
from peewee import ForeignKeyField, IntegerField, CharField, NotFoundError,\
    DoesNotExist
from homeinfolib import create, connection
from homeinfo.crm.customer import Customer
import tarfile
from tempfile import NamedTemporaryFile
from os.path import join
from os import unlink
from contextlib import suppress

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
    def vpn_keys(self):
        """Returns the VPN keys specified for the terminal"""
        ok = True
        ca_file = join(vpn['keys_dir'], 'ca.crt')
        crt_file = join(vpn['keys_dir'], '.'.join([self.hostname, 'crt']))
        key_file = join(vpn['keys_dir'], '.'.join([self.hostname, 'key']))
        with NamedTemporaryFile('wb', suffix='.tar.gz', delete=False) as tmp:
            pass
        with tarfile.open(tmp.name, 'w:gz') as tar:
            for f in [ca_file, crt_file, key_file]:
                try:
                    tar.add(f)
                except:
                    ok = False
                    break
        if ok:
            return tmp.name
        else:
            with suppress(FileNotFoundError):
                unlink(tmp.name)
            return None

    
