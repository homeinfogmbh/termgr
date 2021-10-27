"""Controller for terminal setup."""

from contextlib import suppress
from datetime import datetime
from os.path import basename

from flask import Response, request

from his import authenticated, authorized
from hwdb import Group, System, operating_system, get_free_ipv6_address
from wsgilib import Error, JSON, Binary

from termgr.openvpn import package
from termgr.wireguard import get_wireguard_config, reload
from termgr.wsgi.common import admin, groupadmin


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@admin
def get_system_info(system: System) -> Response:
    """Returns the system information."""

    return JSON(system.to_json(brief=True))


@authenticated
@authorized('termgr')
@admin
def get_openvpn_data(system: System) -> Response:
    """Returns the OpenVPN data for the respective system."""

    windows = request.json.get('windows', False)
    openvpn = system.openvpn

    if openvpn is None:
        raise Error('Missing OpenVPN coniguration for system.')

    try:
        data, filename = package(openvpn, windows=windows)
    except FileNotFoundError as error:
        raise Error(f'Missing file: {basename(error.filename)}',
                    status=500) from None
    except PermissionError as error:
        raise Error(f'Cannot access file: {basename(error.filename)}',
                    status=500) from None

    return Binary(data, filename=filename)


@authenticated
@authorized('termgr')
@admin
def finalize(system: System) -> Response:
    """Posts setup data."""

    with suppress(KeyError):
        system.serial_number = request.json['sn'] or None   # Delete iff empty.

    with suppress(KeyError):
        system.operating_system = operating_system(request.json['os'])

    with suppress(KeyError):
        system.model = request.json['model']

    system.configured = datetime.now()
    system.save()
    return 'System finalized.'


@authenticated
@authorized('termgr')
@groupadmin
def add_system(group: Group) -> JSON:
    """Adds a new WireGuard-only system."""

    system = System(
        group=group,
        ipv6address=get_free_ipv6_address(),
        pubkey=request.json['pubkey'],
        configured=datetime.now(),
        operating_system=operating_system(request.json['os']),
        monitor=request.json.get('monitor'),
        serial_number=request.json.get('sn'),
        model=request.json.get('model')
    )
    system.save()
    reload()
    return JSON({
        **system.to_json(brief=True),
        'wireguard': get_wireguard_config(system)
    })


@authenticated
@authorized('termgr')
@admin
def patch_system(system: System) -> JSON:
    """Patches the given system."""

    with suppress(KeyError):
        system.pubkey = request.json['pubkey']

    with suppress(KeyError):
        system.operating_system = operating_system(request.json['os'])

    with suppress(KeyError):
        system.monitor = request.json['monitor']

    with suppress(KeyError):
        system.serial_number = request.json['sn']

    with suppress(KeyError):
        system.model = request.json['model']

    system.configured = datetime.now()
    system.save()
    reload()
    return JSON({
        **system.to_json(brief=True),
        'wireguard': get_wireguard_config(system)
    })


ROUTES = (
    ('POST', '/setup/info', get_system_info),
    ('POST', '/setup/openvpn', get_openvpn_data),
    ('POST', '/setup/finalize', finalize),
    ('POST', '/setup/system', add_system),
    ('PATCH', '/setup/system', patch_system)
)
