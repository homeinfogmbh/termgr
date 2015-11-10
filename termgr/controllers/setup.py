"""Controller for terminal setup"""

from homeinfo.lib.wsgi import WsgiApp, WsgiResponse, Error,\
    InternalServerError
from homeinfo.terminals.db import Terminal, SetupOperator

from ..lib.openvpn import UnconfiguredError, OpenVPNPackager
from ..lib.pacman import PacmanConfig

__all__ = ['SetupController']


class SetupController(WsgiApp):
    """Controller for terminal setup automation"""

    DEBUG = True

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)

    def get(self, environ):
        """Interpret query dictionary"""
        query_string = self.query_string(environ)
        qd = self.qd(query_string)
        user_name = qd.get('user_name')
        if not user_name:
            return Error('No user name specified', status=400)
        passwd = qd.get('passwd')
        if not passwd:
            return Error('No password specified', status=400)
        operator = SetupOperator.authenticate(user_name, passwd)
        if operator:
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
                    terminal = Terminal.by_ids(cid, tid, deleted=False)
                    if terminal is not None:
                        if operator.authorize(terminal):
                            action = qd.get('action')
                            if action is None:
                                return Error('No action specified', status=400)
                            else:
                                return self._handle(terminal, action)
                        else:
                            return Error('Unauthorized', status=401)
                    else:
                        return Error('No such terminal', status=400)
        else:
            return Error('Invalid credentials', status=401)

    def _handle(self, terminal, action):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        status = 200
        if action == 'location':
            location = terminal.address
            if location is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = location.encode(encoding=charset)
            else:
                msg = 'No location configured for terminal: {0}'.format(
                    terminal)
                return InternalServerError(msg)
        elif action == 'vpn_data':
            packager = OpenVPNPackager(terminal)
            response_body = None
            try:
                response_body = packager()
            except UnconfiguredError:
                msg = ('No OpenVPN configuration found for terminal: '
                       '{0}'.format(terminal))
                return InternalServerError(msg)
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
