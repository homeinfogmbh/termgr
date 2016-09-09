"""Controller for terminal setup"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import WsgiResponse, Error, JSON, InternalServerError, \
    handler, RequestHandler, WsgiApp
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

    def _handle(self, terminal, action, client_version=None):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        status = 200

        if action == 'location':
            if client_version is None:
                if terminal.location is not None:
                    location = str(terminal.location)
                else:
                    location = '!!!UNCONFIGURED!!!'

                if location is not None:
                    content_type = 'text/plain'
                    charset = 'utf-8'
                    response_body = location.encode(encoding=charset)
                else:
                    msg = 'No location configured for terminal: {0}'.format(
                        terminal)
                    return InternalServerError(msg)
            elif client_version == '3.0':
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
            else:
                return Error(
                    'Version: {} is not supported.'.format(client_version),
                    status=400)
        elif action == 'vpn_data':
            packager = OpenVPNPackager(terminal)
            response_body = None

            try:
                response_body = packager.package()
            except FileNotFoundError:
                msg = 'OpenVPN configuration template file not found'
                return InternalServerError(msg)
            except PermissionError:
                msg = 'Not allowed to read OpenVPN configuration template file'
                return InternalServerError(msg)
            else:
                content_type = 'application/x-gzip'
                charset = None
        elif action == 'repo_config':
            pacman_cfg = PacmanConfig(terminal)
            result = None

            try:
                result = pacman_cfg.get()
            except FileNotFoundError:
                msg = 'Pacman config template file not found'
                return InternalServerError(msg)
            except PermissionError:
                msg = 'Not allowed to read pacman config template file'
                return InternalServerError(msg)
            else:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = result.encode(encoding=charset)
        else:
            msg = 'Action "{0}" is not implemented'.format(action)
            return Error(msg, status=501)

        return WsgiResponse(
            status, content_type, response_body, charset=charset, cors=True)


@handler(SetupControllerRequestHandler)
class SetupController(WsgiApp):
    """Controller for terminal setup automation"""

    DEBUG = True

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)
