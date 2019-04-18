"""Controller for terminal setup."""

from os.path import basename

from flask import request

from his import authenticated
from wsgilib import Error, JSON, Binary

from termgr.openvpn import package
from termgr.wsgi.common import setup

__all__ = ['ROUTES']


@authenticated
@setup
def get_system_info(system):
    """Returns the system information."""

    return JSON(system.to_json(cascade=True, brief=True))


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
def set_serial_number(system):
    """Posts setup data."""

    try:
        serial_number = request.json['sn']
    except KeyError:
        raise Error('No serial number specified.')

    system.serial_number = serial_number or None  # Delete iff empty.
    system.save()
    return 'Set serial number to "{}".'.format(system.serial_number)


ROUTES = (
    ('POST', '/setup/info', get_system_info),
    ('POST', '/setup/openvpn', get_openvpn_data),
    ('POST', '/setup/sn', set_serial_number)
)
