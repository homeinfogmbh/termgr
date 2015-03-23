"""Abstract base classes for terminal setup management"""

__date__ = "23.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalAware']


class TerminalAware():
    """Manages terminals"""

    def __init__(self, terminal):
        """Sets user name and password"""
        self.terminal = terminal

    @property
    def cid(self):
        """Returns the customer identifier"""
        return self.terminal.cid

    @property
    def tid(self):
        """Returns the terminal identifier"""
        return self.terminal.tid

    @property
    def idstr(self):
        """Returns a unique string identifier"""
        return '.'.join([str(self.tid), str(self.cid)])
