"""Controller for terminal setup management"""

from homeinfolib.wsgi import WsgiController
from ..db.terminal import Terminal
from ..lib.openvpn import OpenVPNPackage
from ..lib.pacman import PacmanConfig

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['SetupController']


class SetupController(WsgiController):
    """Controller for terminal setup automation"""

    def __init__(self):
        """Initialize request path"""
        super().__init__('setup')

    def _run(self, qd):
        """Interpret query dictionary"""
        cid_str = qd.get('cid')
        if cid_str is None:
            pass
        else:
            try:
                cid = int(cid_str)
            except:
                pass
            else:
                tid_str = qd.get('tid')
                if tid_str is None:
                    pass
                else:
                    try:
                        tid = int(tid_str)
                    except:
                        pass
                    else:
                        term = Terminal.by_ids(cid, tid)
                        if term is not None:
                            action = qd.get('action')
                            if action is None:
                                pass
                            else:
                                return self._handle(term, action)
                        else:
                            pass

    def _handle(self, term, action):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        status = '200 OK'
        if action == 'vpn_data':
            mgr = OpenVPNPackage(term)
            try:
                response_body = mgr.get()
            except:
                result = None
            if response_body is not None:
                content_type = 'application/x-gzip'
                charset = None
            else:
                status = '500 Internal Server Error'
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No OpenVPN configuration found for terminal',
                                '.'.join([str(term.cid), str(term.tid)])])
                response_body = msg.encode(encoding=charset)
        elif action == 'repo_config':
            mgr = PacmanConfig(term)
            try:
                result = mgr.get()
            except:
                result = None
            if result is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body.encode(encoding=charset)
            else:
                status = '500 Internal Server Error'
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(term.cid), str(term.tid)])])
                response_body = msg.encode(encoding=charset)
        else:
            status = '501 Not Implemented'
            content_type = 'text/plain'
            charset = 'utf-8'
            msg = ''.join(['Method "', action, '" is not implemented'])
            response_body = msg.encode(encoding=charset)
        return (status, content_type, charset, response_body)
