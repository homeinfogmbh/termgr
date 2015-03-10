"""Abstract base classes for controllers"""


__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['Controller']


class Controller():
    """Controller for terminal setup automation"""

    BASE_NAME = 'terminals'

    def __init__(self, query_string, df='%Y-%m-%dT%H:%M:%S'):
        """Initialize request path"""
        self._query_string = query_string
        self._date_format = df

    @property
    def _path(self):
        """Returns the path"""
        return '/'.join([self.BASE_NAME, self._name])

    def run(self):
        """Interpret query dictionary"""
        self._run(self._query_string)
