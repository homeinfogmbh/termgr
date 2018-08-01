"""Controller for terminal setup."""

from os.path import basename

from flask import request

from wsgilib import Error, JSON, Binary

from termgr.openvpn import OpenVPNPackager
from termgr.wsgi.common import authenticated, authorized

__all__ = ['ROUTES']


def get_location(terminal):
    """Returns the terminal's location."""

    if terminal.address is None:
        return {}

    address = terminal.address.to_dict()

    if terminal.annotation:
        return {'address': address, 'annotation': annotation}

    return {'address': address}


def openvpn_data(terminal, windows=False):
    """Returns OpenVPN configuration."""

    packager = OpenVPNPackager(terminal)

    try:
        data, filename = packager.package(windows=windows)
    except FileNotFoundError as error:
        raise Error(
            'Missing file: {}'.format(basename(error.filename)), status=500)
    except PermissionError as error:
        raise Error(
            'Cannot access file: {}'.format(basename(error.filename)),
            status=500)

    return Binary(data, filename=filename)


@authenticated
@authorized(setup=True)
def setup_terminal(terminal, action):
    """Posts setup data."""

    windows = request.json.get('windows', False)

    if action == 'terminal_information':
        return JSON(terminal.to_dict())
    elif action == 'location':
        return JSON(get_location(terminal))
    elif action == 'vpn_data':
        return openvpn_data(terminal, windows=windows)
    elif action == 'serial_number':
        try:
            serial_number = request.json['serial_number']
        except KeyError:
            raise Error('No serial number specified.')

        terminal.serial_number = serial_number or None  # Delete iff empty.
        terminal.save()
        return 'Set serial number to "{}".'.format(terminal.serial_number)

    raise Error('Action not implemented.')


ROUTES = (('POST', '/setup/<action>', setup_terminal, 'setup_terminal'),)
