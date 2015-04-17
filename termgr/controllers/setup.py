"""Controller for terminal setup"""

from homeinfolib.wsgi import WsgiController, WsgiResponse, Error,\
    InternalServerError
from terminallib.db import Terminal, SetupOperator
from terminallib.openvpn import OpenVPNPackager
from terminallib.pacman import PacmanConfig

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['SetupController']


class SetupController(WsgiController):
    """Controller for terminal setup automation"""

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
                    term = Terminal.by_ids(cid, tid)
                    if term is not None:
                        if operator.authorize(term):
                            action = self.qd.get('action')
                            if action is None:
                                return Error('No action specified', status=400)
                            else:
                                return self._handle(term, action)
                        else:
                            return Error('Unauthorized', status=401)
                    else:
                        return Error('No such terminal', status=404)
        else:
            return Error('Invalid credentials', status=401)

    def _handle(self, term, action):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        status = 200
        if action == 'location':
            location = term.address
            if location is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = location.encode(encoding=charset)
            else:
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                return InternalServerError(msg)
        elif action == 'vpn_data':
            packager = OpenVPNPackager(term)
            try:
                response_body = packager.get()
            except:
                response_body = None
            if response_body is not None:
                content_type = 'application/x-gzip'
                charset = None
            else:
                msg = ' '.join(['No OpenVPN configuration found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                return InternalServerError(msg)
        elif action == 'repo_config':
            pacman_cfg = PacmanConfig(term)
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
                                '.'.join([str(term.tid), str(term.cid)])])
                return InternalServerError(msg)
        else:
            msg = ''.join(['Method "', action, '" is not implemented'])
            return Error(msg, status=501)
        return WsgiResponse(status, content_type, response_body,
                            charset=charset, cors=True)
