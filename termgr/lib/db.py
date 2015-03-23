"""Library for terminal database management"""

from homeinfo.crm.customer import Customer
from peewee import DoesNotExist
from ..db.terminal import Terminal
from ..config import net

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['DBEntry']


class DBEntry():
    """Manages terminal database records"""

    @classmethod
    def add(self, cid, tid, domain=None):
        """Adds a new terminal"""
        try:
            cst = Customer.iget(Customer.id == cid)  # @UndefinedVariable
        except DoesNotExist:
            return False    # TODO: Improve error handling
        else:
            try:
                terminal = Terminal.iget(   # @UndefinedVariable
                    (Terminal.customer == cst) & (Terminal.tid == tid))
            except DoesNotExist:
                terminal = Terminal()
                terminal.customer = cst
                terminal.tid = tid
                if domain is None:
                    terminal.domain = net['DOMAIN']
                else:
                    terminal.domain = domain
                try:
                    terminal.isave()
                except:
                    return False
                else:
                    return terminal
            else:
                return False

    def delete(self):
        """Deletes the terminal"""
        pass

    def lockdown(self):
        """Lockdown terminal"""
        pass

    def unlock(self):
        """Unlock terminal"""
        pass
