"""Library for terminal pacman.conf management"""

from ..config import pacman
from .abc import TerminalAware

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['PacmanConfig']


class PacmanConfig(TerminalAware):
    """Renders the pacman.conf file for a terminal"""

    @property
    def htpasswd(self):
        """Returns the respective terminal's htpasswd entry"""
        return self.terminal.htpasswd

    def get(self):
        """Returns the rendered configuration file"""
        if self.htpasswd:
            with open(pacman['TEMPLATE'], 'r') as temp:
                pacman_conf = temp.read()
            pacman_conf.replace('<user_name>', self.idstr())
            pacman_conf.replace('<password>', self.htpasswd)
            return pacman_conf
        else:
            return None
