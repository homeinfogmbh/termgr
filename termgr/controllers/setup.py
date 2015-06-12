"""Controller for terminal setup"""

from homeinfo.lib.wsgi import WsgiController, WsgiResponse, Error,\
    InternalServerError
from homeinfo.terminals.db import Terminal, SetupOperator

from ..lib.openvpn import OpenVPNPackager
from ..lib.pacman import PacmanConfig

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
                except:
                    return Error('Invalid customer ID', status=400)
                tid_str = self.qd.get('tid')
                if tid_str is None:
                    return Error('No terminal ID specified', status=400)
                else:
                    try:
                        tid = int(tid_str)
                    except:
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
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(terminal.tid),
                                          str(terminal.cid)])])
                return InternalServerError(msg)
        elif action == 'vpn_data':
            packager = OpenVPNPackager(terminal)
            try:
                response_body = packager.get()
            except:
                response_body = None
            if response_body is not None:
                content_type = 'application/x-gzip'
                charset = None
            else:
                msg = ' '.join(['No OpenVPN configuration found for terminal',
                                '.'.join([str(terminal.tid),
                                          str(terminal.cid)])])
                return InternalServerError(msg)
        elif action == 'repo_config':
            pacman_cfg = PacmanConfig(terminal)
            try:
                result = pacman_cfg.get()
            except:
                result = None
            if result is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = result.encode(encoding=charset)
            else:
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(terminal.tid),
                                          str(terminal.cid)])])
                return InternalServerError(msg)
        else:
            msg = ''.join(['Method "', action, '" is not implemented'])
            return Error(msg, status=501)
        return WsgiResponse(status, content_type, response_body,
                            charset=charset, cors=True)
