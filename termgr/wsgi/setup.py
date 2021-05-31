"""Controller for terminal setup."""

from contextlib import suppress
from datetime import datetime
from os.path import basename

from flask import Response, request

from his import authenticated, authorized
from hwdb import System, operating_system
from wsgilib import Error, JSON, Binary

from termgr.openvpn import package
from termgr.wireguard import get_wireguard_config, update_peers
from termgr.wsgi.common import admin


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
        raise Error('Missing file: {}'.format(basename(error.filename)),
                    status=500) from None
    except PermissionError as error:
        raise Error('Cannot access file: {}'.format(basename(error.filename)),
                    status=500) from None

    return Binary(data, filename=filename)


@authenticated
@authorized('termgr')
@admin
def get_wireguard_data(system: System) -> Response:
    """Returns the WireGuard configuration for the respective system."""

    return JSON(get_wireguard_config(system))


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

    system.configured = datetime.now()  # Mark system as configured.
    system.wireguard.pubkey = request.json.get('wg_pubkey')
    print('Pubkey:', system.wireguard.pubkey, flush=True)
    system.wireguard.save()
    system.save()
    update_peers()
    return 'System finalized.'


ROUTES = (
    ('POST', '/setup/info', get_system_info),
    ('POST', '/setup/openvpn', get_openvpn_data),
    ('POST', '/setup/wireguard', get_wireguard_data),
    ('POST', '/setup/finalize', finalize)
)
