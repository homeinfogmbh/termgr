"""Library for terminal pacman.conf management"""

from ..config import pacman
from .abc import TerminalAware
from .htpasswd import HtpasswdEntry

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['PacmanConfig']


class PacmanConfig(TerminalAware):
    """Renders the pacman.conf file for a terminal"""

    def get(self):
        """Returns the rendered configuration file"""
        htpasswd_entry = HtpasswdEntry(self.terminal)
        user_name, password = htpasswd_entry.get()
        with open(pacman['TEMPLATE'], 'r') as temp:
            pacman_conf = temp.read()
        pacman_conf = pacman_conf.replace('<user_name>', user_name)
        pacman_conf = pacman_conf.replace('<password>', password)
        return pacman_conf
