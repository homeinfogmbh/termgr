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

    def _run(self):
        """Interpret query dictionary"""
        cid_str = self._query_dict.get('cid')
        if cid_str is None:
            pass
        else:
            try:
                cid = int(cid_str)
            except:
                pass
            else:
                tid_str = self._query_dict.get('tid')
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
                            action = self._query_dict.get('action')
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
        status = 200
        if action == 'vpn_data':
            mgr = OpenVPNPackage(term)
            try:
                response_body = mgr.get()
            except:
                response_body = None
            if response_body is not None:
                content_type = 'application/x-gzip'
                charset = None
            else:
                status = 500
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No OpenVPN configuration found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
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
                status = 500
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                response_body = msg.encode(encoding=charset)
        else:
            status = 501
            content_type = 'text/plain'
            charset = 'utf-8'
            msg = ''.join(['Method "', action, '" is not implemented'])
            response_body = msg.encode(encoding=charset)
        return (status, content_type, charset, response_body)
