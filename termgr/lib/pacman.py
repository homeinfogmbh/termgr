"""Library for terminal pacman.conf management"""

from homeinfolib.system import run
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


class Pacman(TerminalAware):
    """Wrapper for remote pacman access"""

    @property
    def _refresh_cmd(self):
        """Returns the refresh command"""
        return [pacman['BINARY'], pacman['REFRESH_CMD']]

    @property
    def _update_cmd(self):
        """Returns the refresh command"""
        return [pacman['BINARY'], pacman['UPDATE_CMD']]

    def refresh(self):
        """Refresh repository"""
        _, _, exit_code = run(self._refresh_cmd)
        return True if not exit_code else False

    @property
    def updates(self):
        """Yields available updates"""
        stdout, _, _ = run(self._update_cmd)
        out_str = stdout.decode()
        for line in out_str.split('\n'):
            line = line.strip()
            try:
                pkg, old_ver, _, new_ver = line.split(' ')
            except ValueError:
                continue
            else:
                yield (pkg, old_ver, new_ver)
