"""List systems."""

from his import ACCOUNT, authenticated
from mdb import Customer
from terminallib import System
from wsgilib import JSON

from termgr.orm import CustomerAdministrator, SystemAdministrator


__all__ = ['ROUTES']


def get_systems():
    """Yields the allowed systems."""

    if ACCOUNT.root:
        yield from System
        return

    for sysadmin in SystemAdministrator.select().where(
            SystemAdministrator.account == ACCOUNT.id):
        yield sysadmin.system


def get_customers():
    """Yields the allowed customers."""

    if ACCOUNT.root:
        yield from Customer
        return

    for customer_admin in CustomerAdministrator.select().where(
            CustomerAdministrator.account == ACCOUNT.id):
        yield customer_admin.customer


@authenticated
def list_systems():
    """Lists the available systems."""

    return JSON([
        system.to_json(cascade=True, brief=True) for system in get_systems()])


@authenticated
def list_customers():
    """Groups the respective terminals by customers."""

    return JSON([
        customer.to_json(company=True) for customer in get_customers()])


ROUTES = (
    ('GET', '/list/systems', list_systems),
    ('GET', '/list/customers', list_customers)
)
