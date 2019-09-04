"""Common WSGI functions."""

from functools import wraps

from flask import request

from his import ACCOUNT
from terminallib import Deployment, System
from wsgilib import Error

from termacls import can_administer_system
from termacls import can_deploy
from termacls import can_setup_system


__all__ = ['admin', 'deploy', 'setup']


def _get_deployment():
    """Returns the respective deployment."""

    ident = request.json.get('deployment')

    if ident is None:
        raise Error('No deployment ID specified.')

    try:
        return Deployment[ident]
    except Deployment.DoesNotExist:
        raise Error('No such deployment.', status=404)


def _get_system():
    """Returns the respective system."""

    ident = request.json.get('system')

    if ident is None:
        raise Error('No system specified.')

    try:
        return System[ident]
    except System.DoesNotExist:
        raise Error('No such system.', status=404)


def admin(function):
    """Wraps the actual with admin permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = _get_system()

        if can_administer_system(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error('Administration unauthorized.', status=403)

    return wrapper


def deploy(function):
    """Wraps the actual deployment permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = _get_system()
        deployment = _get_deployment()

        if can_deploy(ACCOUNT, system, deployment):
            return function(system, deployment, *args, **kwargs)

        raise Error('Deployment operation unauthorized.', status=403)

    return wrapper


def setup(function):
    """Wraps the actual with setup permission checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        system = _get_system()

        if can_setup_system(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error('Setup operation unauthorized.', status=403)

    return wrapper
