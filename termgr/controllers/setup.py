"""Controller for terminal setup"""

from homeinfo.lib.wsgi import WsgiController, WsgiResponse, Error,\
    InternalServerError
from homeinfo.terminals.db import Terminal, SetupOperator

from ..lib.openvpn import OpenVPNPackager
from ..lib.pacman import PacmanConfig
from ..lib.err import UnconfiguredError

__all__ = ['SetupController']


class SetupController(WsgiController):
    """Controller for terminal setup automation"""

    DEBUG = True

    def _run(self):
        """Interpret query dictionary"""
        user_name = self.qd.get('user_name')
        if not user_name:
            return Error('No user name specified', status=400)
        passwd = self.qd.get('passwd')
        if not passwd:
            return Error('No password specified', status=400)
        operator = SetupOperator.authenticate(user_name, passwd)
        if operator:
            cid_str = self.qd.get('cid')
            if cid_str is None:
                return Error('No customer ID specified', status=400)
            else:
                try:
                    cid = int(cid_str)
                except ValueError:
                    return Error('Invalid customer ID', status=400)
                tid_str = self.qd.get('tid')
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
                            action = self.qd.get('action')
                            if action is None:
                                return Error('No action specified', status=400)
                            else:
                                return self._handle(terminal, action)
                        else:
                            return Error('Unauthorized', status=401)
                    else:
                        return Error('No such terminal', status=404)
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
                response_body = packager.get()
            except UnconfiguredError:
                msg = ('No OpenVPN configuration found for terminal: '
                       '{0}'.format(terminal))
                return InternalServerError(msg)
            except (FileNotFoundError, PermissionError):
                msg = 'Unable to read OpenVPN configuration template'
                return InternalServerError(msg)
            else:
                content_type = 'application/x-gzip'
                charset = None
        elif action == 'repo_config':
            pacman_cfg = PacmanConfig(terminal)
            result = None
            try:
                result = pacman_cfg.get()
            except (FileNotFoundError, PermissionError):
                msg = 'Could not open pacman config template'
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
