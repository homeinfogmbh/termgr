"""List systems."""

from his import ACCOUNT, authenticated
from hwdb import System
from wsgilib import JSON

from termacls import get_administerable_deployments, get_administerable_systems


__all__ = ['ROUTES']


@authenticated
def list_deployments():
    """Lists available deployments."""

    return JSON([
        deployment.to_json(systems=True, cascade=2) for deployment in
        get_administerable_deployments(ACCOUNT)])


@authenticated
def get_system(ident):
    """Lists the available systems."""

    systems = get_administerable_systems(ACCOUNT).where(System.id == ident)

    try:
        system = systems.get()
    except System.DoesNotExist:
        return ('No such system.', 404)

    return JSON(system.to_json(cascade=3, brief=True))


@authenticated
def list_systems():
    """Lists the available systems."""

    return JSON([
        system.to_json(cascade=3, brief=True) for system in
        get_administerable_systems(ACCOUNT)])


ROUTES = (
    ('GET', '/list/deployments', list_deployments),
    ('GET', '/list/systems/<int:ident>', get_system),
    ('GET', '/list/systems', list_systems)
)
