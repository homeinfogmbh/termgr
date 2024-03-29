"""Controller for terminal setup."""

from contextlib import suppress
from datetime import datetime

from flask import request

from his import authenticated, authorized
from hwdb import Group, System, operating_system, get_free_ipv6_address
from wsgilib import JSON

from termgr.hooks import reload
from termgr.wireguard import get_wireguard_config
from termgr.wsgi.common import sysadmin, groupadmin


__all__ = ["ROUTES"]


@authenticated
@authorized("termgr")
@sysadmin
def get_system_info(system: System) -> JSON:
    """Returns the system information."""

    return JSON(system.to_json(brief=True))


@authenticated
@authorized("termgr")
@sysadmin
def finalize(system: System) -> str:
    """Posts setup data."""

    with suppress(KeyError):
        system.serial_number = request.json["sn"] or None  # Delete iff empty.

    with suppress(KeyError):
        system.operating_system = operating_system(request.json["os"])

    with suppress(KeyError):
        system.model = request.json["model"]

    if request.json.get("exclusive", False):
        system.pubkey = None

    system.configured = datetime.now()
    system.save()
    reload("bind9")
    return "System finalized."


@authenticated
@authorized("termgr")
@groupadmin
def add_system(group: Group) -> JSON:
    """Adds a new WireGuard-only system."""

    system = System(
        group=group,
        ipv6address=get_free_ipv6_address(),
        pubkey=request.json["pubkey"],
        configured=datetime.now(),
        operating_system=operating_system(request.json["os"]),
        serial_number=request.json.get("sn"),
        model=request.json.get("model"),
        ddb_os=request.json.get("ddb_os", False),
    )
    system.save()
    reload("bind9", wireguard=True)
    return JSON(
        {**system.to_json(brief=True), "wireguard": get_wireguard_config(system)}
    )


@authenticated
@authorized("termgr")
@sysadmin
def patch_system(system: System) -> JSON:
    """Patches the given system."""

    with suppress(KeyError):
        system.pubkey = request.json["pubkey"]

    with suppress(KeyError):
        system.operating_system = operating_system(request.json["os"])

    with suppress(KeyError):
        system.serial_number = request.json["sn"]

    with suppress(KeyError):
        system.model = request.json["model"]

    with suppress(KeyError):
        system.ddb_os = request.json["ddb_os"]

    system.configured = datetime.now()
    system.save()
    reload("bind9", wireguard=True)
    return JSON(
        {**system.to_json(brief=True), "wireguard": get_wireguard_config(system)}
    )


ROUTES = [
    ("POST", "/setup/info", get_system_info),
    ("POST", "/setup/finalize", finalize),
    ("POST", "/setup/system", add_system),
    ("PATCH", "/setup/system", patch_system),
]
