"""Controller for terminal setup management"""

from homeinfolib.wsgi import WsgiController
from termgr.db.terminal import Terminal

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
        if action == 'info':
            result = term.info
            if result is not None:
                content_type = 'text/plain'
                charset = 'utf-8'
                response_body = result.encode(encoding=charset)
            else:
                status = '500 Internal Server Error'
                content_type = 'text/plain'
                charset = 'utf-8'
                msg = ' '.join(['No terminal information for terminal',
                                '.'.join([str(term.cid), str(term.tid)])])
                response_body = msg.encode(encoding=charset)
        elif action == 'vpn_data':
            response_body = term.vpn_data
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
            result = term.repo_config
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
