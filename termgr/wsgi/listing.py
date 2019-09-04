"""List systems."""

from his import ACCOUNT, authenticated
from wsgilib import JSON

from termacls import get_administerable_deployments, get_administerable_systems


__all__ = ['ROUTES']


@authenticated
def list_systems():
    """Lists the available systems."""

    return JSON([
        system.to_json(cascade=3, brief=True) for system in
        get_administerable_systems(ACCOUNT)])


@authenticated
def list_deployments():
    """Lists available deployments."""

    return JSON([
        deployment.to_json(systems=True, cascade=2) for deployment in
        get_administerable_deployments(ACCOUNT)])


ROUTES = (
    ('GET', '/list/deployments', list_deployments),
    ('GET', '/list/systems', list_systems)
)
