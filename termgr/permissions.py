"""Permissions management."""

from termgr.orm import SystemAdministrator, CustomerAdministrator


__all__ = [
    'grant_system',
    'revoke_system',
    'grant_customer',
    'revoke_customer']


def grant_system(account, system):
    """Grats system setup privileges."""

    try:
        return SystemAdministrator.get(
            (SystemAdministrator.account == account)
            & (SystemAdministrator.system == system))
    except SystemAdministrator.DoesNotExist:
        record = SystemAdministrator(account=account, system=system)
        record.save()
        return record


def revoke_system(account, system):
    """Revokes system setup privileges."""

    for record in SystemAdministrator.select().where(
            (SystemAdministrator.account == account)
            & (SystemAdministrator.system == system)):
        record.delete_instance()


def grant_customer(account, customer):
    """Grants customer administration privileges."""

    try:
        return CustomerAdministrator.get(
            (CustomerAdministrator.account == account)
            & (CustomerAdministrator.customer == customer))
    except CustomerAdministrator.DoesNotExist:
        record = CustomerAdministrator(account=account, customer=customer)
        record.save()
        return record


def revoke_customer(account, customer):
    """Revokes customer administration privileges."""

    for record in CustomerAdministrator.select().where(
            (CustomerAdministrator.account == account)
            & (CustomerAdministrator.customer == customer)):
        record.delete_instance()
