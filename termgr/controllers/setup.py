"""Controller for terminal setup."""

from os.path import basename
from peewee import DoesNotExist

from wsgilib import WsgiResponse, Error, JSON, InternalServerError, \
    RequestHandler
from homeinfo.terminals.orm import Terminal

from termgr.openvpn import OpenVPNPackager
from termgr.orm import User

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


def openvpn_data(terminal, logger=None):
    """Returns OpenVPN configuration."""

    packager = OpenVPNPackager(terminal, logger=logger)

    try:
        response_body = packager.package()
    except FileNotFoundError as file_not_found:
        return InternalServerError('Missing file: {}'.format(basename(
            file_not_found.filename)))
    except PermissionError as permission_error:
        return InternalServerError('Cannot access file: {}'.format(basename(
            permission_error.filename)))
    else:
        return WsgiResponse(
            200, 'application/x-gzip', response_body, charset=None)


class SetupHandler(RequestHandler):
    """Handles requests for the SetupController"""

    @property
    def user(self):
        """Returns the user."""
        user_name = self.query.get('user_name')

        if not user_name:
            raise Error('No user name specified', status=400) from None

        passwd = self.query.get('passwd')

        if not passwd:
            raise Error('No password specified', status=400) from None

        return User.authenticate(user_name, passwd)

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
    def cid(self):
        """Returns the customer ID."""
        try:
            cid = self.query['cid']
        except KeyError:
            raise Error('No customer ID specified', status=400) from None
        else:
            try:
                return int(cid)
            except ValueError:
                raise Error('Invalid customer ID', status=400) from None

    @property
    def tid(self):
        """Returns the terminal ID."""
        try:
            tid = self.query['tid']
        except KeyError:
            raise Error('No terminal ID specified', status=400) from None
        else:
            try:
                return int(tid)
            except ValueError:
                raise Error('Invalid terminal ID', status=400) from None

    @property
    def terminal(self):
        """Returns the appropriate terminal."""
        try:
            return Terminal.by_ids(self.cid, self.tid, deleted=False)
        except DoesNotExist:
            raise Error('No such terminal', status=400) from None

    @property
    def action(self):
        """Returns the action."""
        try:
            return self.query['action']
        except KeyError:
            raise Error('No action specified', status=400) from None

    def get(self):
        """Process GET request"""
        user = self.user

        if user:
            terminal = self.terminal

            if user.authorize(terminal, setup=True):
                action = self.action

                if action == 'location':
                    return get_location(terminal, self.client_version)
                elif action == 'vpn_data':
                    return openvpn_data(terminal, logger=self.logger)

                msg = 'Action "{}" is not implemented'.format(action)
                return Error(msg, status=400)

            return Error('Unauthorized', status=401)

        return Error('Invalid credentials', status=401)
