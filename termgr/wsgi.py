"""Main WSGI handler"""

from datetime import datetime
from .controllers import controllers

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['WSGI']


class WSGI():
    """Controller for terminal setup automation"""

    PARAM_SEP = '&'
    ASS_SEP = '='
    LIST_SEP = ','

    def __init__(self, path_info, query_string):
        """Initialize request path"""
        self._path_info = path_info
        self._query_string = query_string

    @property
    def _query_dict(self):
        """Converts a query string into a query dictionary"""
        result = {}
        for param_data in self._query_string.split(self.PARAM_SEP):
            fragments = param_data.split(self.ASS_SEP)
            param, value = fragments[0], self.ASS_SEP.join(fragments[1:])
            result[param] = self._cast(value)
        return result

    def _cast(self, s):
        """Cast a string for certain data types"""
        if s is None:
            return None
        elif self.LIST_SEP in s:
            result = []
            for elem in s.split(self.LIST_SEP):
                result.append(self._cast(elem))
            return result
        else:
            try:
                i = int(s)
            except ValueError:
                try:
                    f = float(s)
                except ValueError:
                    try:
                        d = datetime.strptime(s, self._date_format)
                    except ValueError:
                        sl = s.lower()
                        if sl == 'true':
                            return True
                        elif sl == 'false':
                            return False
                        else:
                            return s
                    else:
                        return d
                else:
                    return f
            else:
                return i

    def run(self):
        """Interpret path info"""
        controller = controllers.get(self._path_info)
        if controller is None:
            msg = ' '.join(['Invalid path:', self._path_info])
            status = '400 Bad Request'
            charset = 'utf-8'
            response_body = msg.encode(encoding=charset)
            content_type = 'text/plain'
        else:
            try:
                result = controller(self._query_dict).run()
            except:
                msg = 'Internal Server Error'
                status = '500 Internal Server Error'
                charset = 'utf-8'
                response_body = msg.encode(encoding=charset)
                content_type = 'text/plain'
            else:
                try:
                    status, response_body, content_type, charset = result
                except (ValueError, TypeError):
                    msg = 'Internal Server Error'
                    status = '500 Internal Server Error'
                    charset = 'utf-8'
                    response_body = msg.encode(encoding=charset)
                    content_type = 'text/plain'
        return (status, response_body, content_type, charset)
