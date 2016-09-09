"""Controller for terminal setup"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import WsgiResponse, Error, OK, JSON, \
    InternalServerError, handler, RequestHandler, WsgiApp
from homeinfo.terminals.orm import Terminal, AddressUnconfiguredError

from termgr.lib.openvpn import OpenVPNPackager
from termgr.lib.pacman import PacmanConfig
from termgr.orm import User

__all__ = ['SetupController']


class SetupControllerRequestHandler(RequestHandler):
    """Handles requests for the SetupController"""

    def get(self):
        """Interpret query dictionary"""
        qd = self.query_dict
        client_version = qd.get('client_version')
        user_name = qd.get('user_name')

        if not user_name:
            return Error('No user name specified', status=400)

        passwd = qd.get('passwd')

        if not passwd:
            return Error('No password specified', status=400)

        user = User.authenticate(user_name, passwd)

        if user:
            cid_str = qd.get('cid')

            if cid_str is None:
                return Error('No customer ID specified', status=400)
            else:
                try:
                    cid = int(cid_str)
                except ValueError:
                    return Error('Invalid customer ID', status=400)

                tid_str = qd.get('tid')

                if tid_str is None:
                    return Error('No terminal ID specified', status=400)
                else:
                    try:
                        tid = int(tid_str)
                    except ValueError:
                        return Error('Invalid terminal ID', status=400)

                    try:
                        terminal = Terminal.by_ids(cid, tid, deleted=False)
                    except DoesNotExist:
                        return Error('No such terminal', status=400)
                    else:
                        if user.authorize(terminal, setup=True):
                            action = qd.get('action')

                            if action is None:
                                return Error('No action specified', status=400)
                            else:
                                return self._handle(
                                    terminal, action,
                                    client_version=client_version)
                        else:
                            return Error('Unauthorized', status=401)
        else:
            return Error('Invalid credentials', status=401)

    def _legacy_location(self, terminal):
        """Returns terminal location data for legacy client versions"""
        if terminal.location is not None:
            location = str(terminal.location)
        else:
            location = '!!!UNCONFIGURED!!!'

        return OK(location)

    def _json_location(self, terminal):
        """Returns terminal location data for
        new client versions in JSON format
        """
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

    def _openvpn_data(self, terminal):
        """Returns OpenVPN configuration"""
        packager = OpenVPNPackager(terminal)

        try:
            response_body = packager.package()
        except FileNotFoundError:
            msg = 'OpenVPN configuration template file not found'
            return InternalServerError(msg)
        except PermissionError:
            msg = 'Not allowed to read OpenVPN configuration template file'
            return InternalServerError(msg)
        else:
            return WsgiResponse(
                200, 'application/x-gzip',
                response_body, charset=None)

    def _handle(self, terminal, action, client_version=None):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        if action == 'location':
            if client_version is None:
                return self._legacy_location(terminal)
            elif client_version == '3.0':
                return self._json_location(terminal)
            else:
                msg = 'Version: {} is not supported.'.format(client_version)
                return Error(msg, status=400)
        elif action == 'vpn_data':
            return self._openvpn_data(terminal)
        else:
            msg = 'Action "{}" is not implemented'.format(action)
            return Error(msg, status=400)


@handler(SetupControllerRequestHandler)
class SetupController(WsgiApp):
    """Controller for terminal setup automation"""

    DEBUG = True

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)
