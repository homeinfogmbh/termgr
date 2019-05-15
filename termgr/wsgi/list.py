"""List systems."""

from his import ACCOUNT, authenticated
from mdb import Customer
from terminallib import Connection, Deployment, System, Type
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


def get_deployments():
    """Yields the allowed deployments."""

    if ACCOUNT.root:
        return Deployment

    customers = set(get_customers())
    return Deployment.select().where(Deployment.customer << customers)


@authenticated
def list_systems():
    """Lists the available systems."""

    return JSON([
        system.to_json(cascade=3, brief=True) for system in get_systems()])


@authenticated
def list_deployments():
    """Lists available deployments."""

    return JSON([
        deployment.to_json(systems=True, cascade=2)
        for deployment in get_deployments()])


@authenticated
def list_customers():
    """Groups the respective terminals by customers."""

    return JSON([customer.to_json(cascade=1) for customer in get_customers()])


@authenticated
def list_connections():
    """Lists available connections."""

    return JSON([connection.value for connection in Connection])


@authenticated
def list_types():
    """Lists available types."""

    return JSON([typ.value for typ in Type])


ROUTES = (
    ('GET', '/list/systems', list_systems),
    ('GET', '/list/customers', list_customers),
    ('GET', '/list/connections', list_connections),
    ('GET', '/list/types', list_types)
)
