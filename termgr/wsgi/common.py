"""Common WSGI functions."""

from functools import wraps
from typing import Callable, Optional, Union

from flask import request

from his import ACCOUNT
from hwdb import Deployment, Group, System
from mdb import Address
from termacls import can_administer_deployment
from termacls import can_administer_system
from termacls import can_deploy
from termacls import GroupAdmin
from wsgilib import Error


__all__ = ["depadmin", "sysadmin", "deploy", "groupadmin", "get_address"]


def _get_deployment(deployment: Optional[int] = None) -> Optional[Deployment]:
    """Returns the respective deployment."""

    if deployment is None:
        try:
            deployment = request.json["deployment"]
        except KeyError:
            raise Error("No deployment ID specified.")

    if deployment is None:
        return None

    try:
        return Deployment.select(cascade=True).where(Deployment.id == deployment).get()
    except Deployment.DoesNotExist:
        raise Error("No such deployment.", status=404) from None


def _get_system(system: Optional[int] = None) -> System:
    """Returns the respective system."""

    if system is None:
        system = request.json["system"]

    if system is None:
        raise Error("No system specified.")

    try:
        return System.select(cascade=True).where(System.id == system).get()
    except System.DoesNotExist:
        raise Error("No such system.", status=404) from None


def _get_group(ident: int) -> Group:
    """Returns a hardware group."""

    if ACCOUNT.root:
        return Group[ident]

    return (
        Group.select()
        .join(GroupAdmin)
        .where((Group.id == ident) & (GroupAdmin.account == ACCOUNT.id))
        .get()
    )


def depadmin(function: Callable) -> Callable:
    """Wraps a deployment-related action with admin permission checks."""

    @wraps(function)
    def wrapper(*args, deployment: Optional[int] = None, **kwargs):
        deployment = _get_deployment(deployment=deployment)

        if can_administer_deployment(ACCOUNT, deployment):
            return function(deployment, *args, **kwargs)

        raise Error("Deployment administration unauthorized.", status=403)

    return wrapper


def sysadmin(function: Callable) -> Callable:
    """Wraps a system-related action  with admin permission checks."""

    @wraps(function)
    def wrapper(*args, system: Optional[int] = None, **kwargs):
        system = _get_system(system=system)

        if can_administer_system(ACCOUNT, system):
            return function(system, *args, **kwargs)

        raise Error("System administration unauthorized.", status=403)

    return wrapper


def deploy(function: Callable) -> Callable:
    """Wraps the actual deployment permission checks."""

    @wraps(function)
    def wrapper(*args, system: Optional[int] = None, **kwargs):
        system = _get_system(system=system)
        deployment = _get_deployment()

        if can_deploy(ACCOUNT, system, deployment):
            return function(system, deployment, *args, **kwargs)

        raise Error("Deployment operation unauthorized.", status=403)

    return wrapper


def groupadmin(function: Callable) -> Callable:
    """Wraps the actual group admin checks."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            group = _get_group(request.json["group"])
        except KeyError:
            raise Error("No group specified.") from None
        except Group.DoesNotExist:
            raise Error("No such group.") from None

        return function(group, *args, **kwargs)

    return wrapper


def get_address(address: Union[list[str], None]) -> Optional[Address]:
    """Returns an address object or None."""

    if address is None:
        return None

    address = Address.add(*address)

    if address.id is None:
        address.save()

    return address
