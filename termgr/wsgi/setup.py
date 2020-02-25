"""Controller for terminal setup."""

from contextlib import suppress
from datetime import datetime
from os.path import basename

from flask import request

from his import authenticated
from wsgilib import Error, JSON, Binary

from termgr.openvpn import package
from termgr.wireguard import get_wireguard_config
from termgr.wsgi.common import setup


__all__ = ['ROUTES']


@authenticated
@setup
def get_system_info(system):
    """Returns the system information."""

    return JSON(system.to_json(brief=True))


@authenticated
@setup
def get_openvpn_data(system):
    """Returns the OpenVPN data for the respective system."""

    windows = request.json.get('windows', False)
    openvpn = system.openvpn

    if openvpn is None:
        raise Error('Missing OpenVPN coniguration for system.')

    try:
        data, filename = package(openvpn, windows=windows)
    except FileNotFoundError as error:
        raise Error('Missing file: {}'.format(basename(error.filename)),
                    status=500)
    except PermissionError as error:
        raise Error('Cannot access file: {}'.format(basename(error.filename)),
                    status=500)

    return Binary(data, filename=filename)


@authenticated
@setup
def get_wireguard_data(system):
    """Returns the WireGuard configuration for the respective system."""

    JSON(get_wireguard_config(system))


@authenticated
@setup
def finalize(system):
    """Posts setup data."""

    with suppress(KeyError):
        system.serial_number = request.json['sn'] or None   # Delete iff empty.

    system.configured = datetime.now()  # Mark system as configured.
    system.wireguard.pubkey = request.json.get('wg_pubkey')
    system.wireguard.save()
    system.save()
    return 'System finalized.'


ROUTES = (
    ('POST', '/setup/info', get_system_info),
    ('POST', '/setup/openvpn', get_openvpn_data),
    ('POST', '/setup/wireguard', get_wireguard_data),
    ('POST', '/setup/finalize', finalize)
)
