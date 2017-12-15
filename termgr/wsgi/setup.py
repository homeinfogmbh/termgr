"""Controller for terminal setup."""

from os.path import basename

from flask import request

from wsgilib import Error, JSON, Binary

from termgr.openvpn import OpenVPNPackager
from termgr.wsgi.common import DATA, get_user, get_terminal, get_action

__all__ = ['ROUTES']


def legacy_location(terminal):
    """Returns terminal location data for legacy client versions."""

    location = {}

    if terminal.location is not None:
        address = terminal.location.address
        annotation = terminal.location.annotation
        location['street'] = str(address.street)
        location['house_number'] = str(address.house_number)
        location['zip_code'] = str(address.zip_code)
        location['city'] = str(address.city)

        if annotation:
            location['annotation'] = str(annotation)

    return location


def get_location(terminal):
    """Returns the terminal's location."""

    if terminal.location:
        return terminal.location.to_dict()

    return {}


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


def legacy_setup_terminal():
    """Returns the respective setup data."""

    user = get_user(legacy=True)
    terminal = get_terminal()
    windows = bool(request.args.get('windows'))

    if user.authorize(terminal, setup=True):
        action = get_action()

        if action == 'terminal_information':
            return JSON(terminal.to_dict())
        elif action == 'location':
            return JSON(get_location(terminal))
        elif action == 'vpn_data':
            return openvpn_data(terminal, windows=windows)

        raise Error('Action not implemented.')

    raise Error('Not authorized.', status=403)


def setup_terminal(action):
    """Posts setup data."""

    user = get_user()
    terminal = get_terminal()
    windows = bool(request.args.get('windows'))

    if user.authorize(terminal, setup=True):
        if action == 'terminal_information':
            return JSON(terminal.to_dict())
        elif action == 'location':
            return JSON(get_location(terminal))
        elif action == 'vpn_data':
            return openvpn_data(terminal, windows=windows)
        elif action == 'serial_number':
            try:
                serial_number = DATA.json['serial_number']
            except KeyError:
                raise Error('No serial number specified.')

            terminal.serial_number = serial_number
            terminal.save()
            return 'Set serial number to "{}".'.format(serial_number)

        raise Error('Action not implemented.')

    raise Error('Not authorized.', status=403)


ROUTES = (
    ('/setup', 'GET', legacy_setup_terminal),
    ('/setup/<action>', 'POST', setup_terminal))
