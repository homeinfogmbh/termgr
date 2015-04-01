"""Library for terminal database management"""

from homeinfo.crm.customer import Customer
from peewee import DoesNotExist
from terminallib.db import Terminal
from ..config import net

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['DBEntry']


class DBEntry():
    """Manages terminal database records"""

    @classmethod
    def add(cls, cid, tid, domain=None):
        """Adds a new terminal"""
        if cls.exists(cid, tid):
            return False
        else:
            terminal = Terminal()
            terminal.customer = cid
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

    @classmethod
    def exists(cls, cid, tid):
        """Determines whether a certain terminal exists"""
        try:
            cst = Customer.iget(Customer.id == cid)  # @UndefinedVariable
        except DoesNotExist:
            return False    # TODO: Improve error handling
        else:
            try:
                terminal = Terminal.iget(   # @UndefinedVariable
                    (Terminal.customer == cst) & (Terminal.tid == tid))
            except DoesNotExist:
                return False
            else:
                return terminal

    def delete(self):
        """Deletes the terminal"""
        pass

    def lockdown(self):
        """Lockdown terminal"""
        pass

    def unlock(self):
        """Unlock terminal"""
        pass
