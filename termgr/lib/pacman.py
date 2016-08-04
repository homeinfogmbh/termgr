"""Library for terminal pacman.conf management"""

from homeinfo.terminals.abc import TerminalAware
from homeinfo.terminals.config import config
from homeinfo.terminals.ctrl import RemoteController

from ..config import CONFIG


__all__ = ['PacmanConfig']


class PacmanConfig(TerminalAware):
    """Renders the pacman.conf file for a terminal"""

    def get(self):
        """Returns the rendered configuration file"""
        with open('/usr/share/terminals/pacman.conf.temp', 'r') as temp:
            pacman_conf = temp.read()

        pacman_conf = pacman_conf.format(
            addr=config.net['IPV4ADDR'],
            port=config.net['HTTP_PRIV_PORT'])

        return pacman_conf


class Pacman(TerminalAware):
    """Wrapper for remote pacman access"""

    def __init__(self, terminal):
        """Initializes the remote controller"""
        super().__init__(terminal)
        self._remote = RemoteController(terminal)

    @property
    def _refresh_cmd(self):
        """Returns the refresh command"""
        return [CONFIG.pacman['BINARY'],
                CONFIG.pacman['REFRESH_CMD']]

    @property
    def _update_cmd(self):
        """Returns the refresh command"""
        return [CONFIG.pacman['BINARY'],
                CONFIG.pacman['UPDATE_CMD']]

    def refresh(self):
        """Refresh repository"""
        _, _, exit_code = self._remote.execute(self._refresh_cmd)
        return True if not exit_code else False

    @property
    def updates(self):
        """Yields available updates"""
        stdout, stderr, exit_code = self._remote.execute(self._update_cmd)

        if exit_code == 0:
            try:
                out_str = stdout.decode()
            except:
                pass    # TODO: handle error
            else:
                for line in out_str.split('\n'):
                    line = line.strip()

                    try:
                        pkg, old_ver, _, new_ver = line.split(' ')
                    except ValueError:
                        continue
                    else:
                        yield (pkg, old_ver, new_ver)

        elif exit_code == 1:
            pass    # TODO: No updates available
        else:
            print(stderr.decode())    # TODO: Error!
