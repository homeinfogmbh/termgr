"""Controller for terminal setup"""

from homeinfo.lib.wsgi import WsgiApp, Error, OK, InternalServerError
from homeinfo.terminals.orm import AccessStats

__all__ = ['StatsController']


class StatsController(WsgiApp):
    """Controller for terminal statistics"""

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)
        self._tokens = []
        with open('/etc/termstats.tokens', 'r') as tokens:
            for line in tokens:
                line = line.strip()
                if not line:
                    # Skip empty lines
                    continue
                elif line.startswith('#'):
                    # Skip comments
                    continue
                else:
                    self._tokens.append(line)

    def get(self, environ):
        """Interpret query dictionary"""
        query_string = self.query_string(environ)
        qd = self.qd(query_string)
        token = qd.get('token')
        # Authenticate
        if token is not None and token in self._tokens:
            cid_str = qd.get('cid')
            try:
                cid = int(cid_str)
            except (TypeError, ValueError):
                return Error('Invalid customer ID', status=400)
            tid_str = qd.get('tid')
            if tid_str is None:
                tid = None
            else:
                try:
                    tid = int(tid_str)
                except (TypeError, ValueError):
                    return Error('Invalid terminal ID', status=400)
            vid_str = qd.get('vid')
            try:
                vid = int(vid_str)
            except (TypeError, ValueError):
                return Error('Invalid virtual ID', status=400)
            document = qd.get('document')
            if document is not None:
                if AccessStats.add(cid, vid, document, tid=tid):
                    return OK('Statistics entry added')
                else:
                    return InternalServerError(
                        'Could not add statistics record')
            else:
                return Error('No document specified', status=400)
        else:
            return Error('Not authenticated', status=401)
