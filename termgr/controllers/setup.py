"""Controller for terminal setup."""

from os.path import basename

from wsgilib import OK, Error, JSON, InternalServerError, Binary

from termgr.openvpn import OpenVPNPackager
from .abc import TermgrHandler

__all__ = ['SetupHandler']


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

    return JSON(location)


def get_location(terminal, client_version):
    """Returns the terminal's location."""

    if client_version is None or client_version < 4:
        return legacy_location(terminal)

    if terminal.location:
        return JSON(terminal.location.to_dict())

    return JSON({})


def openvpn_data(terminal, windows=False):
    """Returns OpenVPN configuration."""

    packager = OpenVPNPackager(terminal)

    try:
        data, filename = packager.package(windows=windows)
    except FileNotFoundError as file_not_found:
        return InternalServerError('Missing file: {}'.format(basename(
            file_not_found.filename)))
    except PermissionError as permission_error:
        return InternalServerError('Cannot access file: {}'.format(basename(
            permission_error.filename)))
    else:
        return Binary(data, filename=filename)


class SetupHandler(TermgrHandler):
    """Handles requests for the SetupController"""

    @property
    def client_version(self):
        """Returns the client version."""
        try:
            client_version = self.query['client_version']
        except KeyError:
            return None
        else:
            try:
                return float(client_version)
            except ValueError:
                raise Error('Invalid client version.', status=400) from None

    @property
    def action(self):
        """Returns the action."""
        try:
            return self.query['action']
        except KeyError:
            raise Error('No action specified.', status=400) from None

    @property
    def windows(self):
        """Returns the windows format flag."""
        return bool(self.query.get('windows'))

    def get(self):
        """Process GET request."""
        user = self.user

        if user:
            terminal = self.terminal

            if user.authorize(terminal, setup=True):
                action = self.action

                if action == 'location':
                    return get_location(terminal, self.client_version)
                elif action == 'vpn_data':
                    return openvpn_data(terminal, windows=self.windows)

                msg = 'Action "{}" is not implemented.'.format(action)
                return Error(msg, status=400)

            return Error('Unauthorized.', status=401)

        return Error('Invalid credentials.', status=401)

    def post(self):
        """Handle POST requests."""
        user = self.user

        if user:
            terminal = self.terminal

            if user.authorize(terminal, setup=True):
                try:
                    serial_number = self.query['serial_number']
                except KeyError:
                    return Error('No serial number specified.')
                else:
                    terminal.serial_number = serial_number
                    terminal.save()
                    return OK('Set serial number to "{}".'.format(
                        serial_number))

            return Error('Unauthorized.', status=401)

        return Error('Invalid credentials.', status=401)
