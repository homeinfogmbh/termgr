"""List systems."""

from his import ACCOUNT, authenticated
from mdb import Customer
from terminallib import Connection, Deployment, System, Type
from wsgilib import JSON

from termgr.orm import CustomerAdministrator, SystemAdministrator


__all__ = ['ROUTES']


def _get_systems():
    """Yields the allowed systems."""

    if ACCOUNT.root:
        yield from System
        return

    for sysadmin in SystemAdministrator.select().where(
            SystemAdministrator.account == ACCOUNT.id):
        yield sysadmin.system


def _get_customers():
    """Yields the allowed customers."""

    if ACCOUNT.root:
        yield from Customer
        return

    for customer_admin in CustomerAdministrator.select().where(
            CustomerAdministrator.account == ACCOUNT.id):
        yield customer_admin.customer


def _get_deployments():
    """Yields the allowed deployments."""

    if ACCOUNT.root:
        return Deployment

    join_condition = CustomerAdministrator.customer == Deployment.customer
    return Deployment.select().join(
        CustomerAdministrator, on=join_condition, join_type='LEFT').where(
            CustomerAdministrator.account == ACCOUNT.id)


@authenticated
def list_systems():
    """Lists the available systems."""

    return JSON([
        system.to_json(cascade=3, brief=True) for system in _get_systems()])


@authenticated
def list_deployments():
    """Lists available deployments."""

    return JSON([
        deployment.to_json(systems=True, cascade=2)
        for deployment in _get_deployments()])


@authenticated
def list_customers():
    """Groups the respective terminals by customers."""

    return JSON([customer.to_json(cascade=1) for customer in _get_customers()])


@authenticated
def list_connections():
    """Lists available connections."""

    return JSON([connection.value for connection in Connection])


@authenticated
def list_types():
    """Lists available types."""

    return JSON([typ.value for typ in Type])


ROUTES = (
    ('GET', '/list/connections', list_connections),
    ('GET', '/list/customers', list_customers),
    ('GET', '/list/deployments', list_deployments),
    ('GET', '/list/systems', list_systems),
    ('GET', '/list/types', list_types)
)
