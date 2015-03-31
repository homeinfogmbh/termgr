"""Controller for terminal setup management"""

from homeinfolib.wsgi import WsgiController
from ..db.terminal import Terminal
from ..lib.openvpn import OpenVPNPackager
from ..lib.pacman import PacmanConfig
from ..config import ssh

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
                                user = self._query_dict.get('user')
                                return self._handle(term, action, user=user)
                        else:
                            pass

    def _handle(self, term, action, user=None):
        """Handles an action for a certain
        customer id, terminal id and action
        """
        status = 200
        if action == 'location':
            location = term.location
            if location is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = location.encode(encoding=charset)
            else:
                status = 500
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                response_body = msg.encode(encoding=charset)
        elif action == 'pubkey':
            if user is not None:
                try:
                    with open(ssh['_'.join(['PUBLIC_KEY', user.upper()])],
                              'r') as pk:
                        pubkey = pk.read()
                except:
                    pubkey = None
            else:
                pubkey = None
            if pubkey is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = pubkey.encode(encoding=charset)
            else:
                status = 500
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No Repository configuration',
                                'found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                response_body = msg.encode(encoding=charset)
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
                status = 500
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No OpenVPN configuration found for terminal',
                                '.'.join([str(term.tid), str(term.cid)])])
                response_body = msg.encode(encoding=charset)
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
