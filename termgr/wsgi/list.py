"""List systems."""

from his import ACCOUNT, authenticated
from wsgilib import JSON

from termgr.orm import SystemAdministrator


__all__ = ['ROUTES']


def get_systems():
    """Groups the respective terminals by customers."""

    for sysadmin in SystemAdministrator.select().where(
            SystemAdministrator.account == ACCOUNT.id):
        yield sysadmin.system


@authenticated
def list_systems():
    """Groups the respective terminals by customers."""

    return JSON([
        system.to_json(cascade=True, brief=True) for system in get_systems()])


ROUTES = (('GET', '/list', list_systems),)
