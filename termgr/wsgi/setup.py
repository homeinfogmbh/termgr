"""Controller for terminal setup."""

from os.path import basename

from flask import request

from wsgilib import JSON, Binary

from termgr.openvpn import OpenVPNPackager
from termgr.wsgi.common import get_user, get_terminal, get_action

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


def get_location(terminal, client_version):
    """Returns the terminal's location."""

    if client_version is None or client_version < 4:
        return legacy_location(terminal)

    if terminal.location:
        return terminal.location.to_dict()

    return {}


def openvpn_data(terminal, windows=False):
    """Returns OpenVPN configuration."""

    packager = OpenVPNPackager(terminal)

    try:
        data, filename = packager.package(windows=windows)
    except FileNotFoundError as error:
        return ('Missing file: {}'.format(basename(error.filename)), 500)
    except PermissionError as error:
        return ('Cannot access file: {}'.format(basename(error.filename)), 500)

    return Binary(data, filename=filename)


def get_setup_data():
    """Returns the respective setup data."""

    user = get_user()

    try:
        client_version = float(request.args.get('client_version'))
    except TypeError:
        client_version = None
    except ValueError:
        return ('Invalid client version.', 400)

    windows = bool(request.args.get('windows'))
    terminal = get_terminal()

    if user.authorize(terminal, setup=True):
        action = get_action()

        if action == 'terminal_information':
            return JSON(terminal.to_dict())
        if action == 'location':
            return JSON(get_location(terminal, client_version))
        elif action == 'vpn_data':
            return openvpn_data(terminal, windows=windows)

        return ('Action not implemented.', 400)

    return ('Not authorized.', 403)


def post_setup_data():
    """Posts setup data."""

    user = get_user()
    terminal = get_terminal()

    if user.authorize(terminal, setup=True):
        action = get_action()

        if action == 'serial_number':
            try:
                serial_number = request.get_data().decode()
            except ValueError:
                return ('No serial number specified.', 400)

            terminal.serial_number = serial_number
            terminal.save()
            return 'Set serial number to "{}".'.format(serial_number)

        return ('Action not implemented.', 400)

    return ('Not authorized.', 403)


ROUTES = (('/', 'GET', get_setup_data), ('/', 'POST', post_setup_data))
