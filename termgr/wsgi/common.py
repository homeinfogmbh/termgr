"""Common WSGI functions."""

from functools import wraps
from typing import Callable, Optional

from flask import request

from his import ACCOUNT
from hwdb import Deployment, System
from wsgilib import Error

from termacls import can_administer_system
from termacls import can_deploy


__all__ = ['admin', 'deploy']


def _get_deployment() -> Deployment:
    """Returns the respective deployment."""

    ident = request.json.get('deployment')

    if ident is None:
        raise Error('No deployment ID specified.')

    try:
        return Deployment.select(cascade=True).where(
            Deployment.id == ident).get()
    except Deployment.DoesNotExist:
        raise Error('No such deployment.', status=404) from None


def _get_system(system: Optional[int] = None) -> System:
    """Returns the respective system."""

    if system is None:
        system = request.json.get('system')

    if system is None:
        raise Error('No system specified.')

    try:
        return System.select(cascade=True).where(System.id == system).get()
    except System.DoesNotExist:
        raise Error('No such system.', status=404) from None


def admin(function: Callable) -> Callable:
    """Wraps the actual with admin permission checks."""

    @wraps(function)
    def wrapper(*args, system: Optional[int] = None, **kwargs):
        system = _get_system(system=system)

        if can_administer_system(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error('Administration unauthorized.', status=403)

    return wrapper


def deploy(function: Callable) -> Callable:
    """Wraps the actual deployment permission checks."""

    @wraps(function)
    def wrapper(*args, system: Optional[int] = None, **kwargs):
        system = _get_system(system=system)
        deployment = _get_deployment()

        if can_deploy(ACCOUNT, system, deployment):
            return function(system, deployment, *args, **kwargs)

        raise Error('Deployment operation unauthorized.', status=403)

    return wrapper
