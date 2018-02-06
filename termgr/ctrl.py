"""Remote terminal controller."""

from fancylog import Logger
from terminallib import RemoteController


__all__ = ['TerminalsController', 'TerminalController']


REBOOT_OPTIONS = {
    'ServerAliveInterval': 5,
    'ServerAliveCountMax': 3}


class TerminalsController:
    """Processes several terminals in parallel."""

    def __init__(self, user=None):
        """Sets terminals, user and logger."""
        self.user = user
        self.logger = Logger(self.__class__.__name__)

    def _controller(self, terminal):
        """Returns a controller for the respective terminal."""
        return TerminalController(terminal, user=self.user, logger=self.logger)

    def reboot(self, terminal):
        """Rboots a terminal."""
        return self._controller(terminal).reboot()

    def cleanup(self, terminal):
        """Cleans up package chache."""
        return self._controller(terminal).cleanup()

    def update(self, terminal):
        """Updates packages."""
        return self._controller(terminal).update()

    def stage(self, terminal):
        """Stage packages."""
        return self._controller(terminal).stage()

    def upgrade(self, terminal):
        """Stage packages."""
        return self._controller(terminal).upgrade()

    def unlock(self, terminal):
        """Unlocks the package manager."""
        return self._controller(terminal).unlock()

    def chkres(self, terminal):
        """Checks the resolution."""
        return self._controller(terminal).resolution

    def install(self, *pkgs, asexplicit=False):
        """Installs software packages."""
        def install(terminal):
            """Proxies the package installation."""
            return self._controller(terminal).install(
                *pkgs, asexplicit=asexplicit)

        return install


class TerminalController(RemoteController):
    """Does stuff on remote terminals."""

    def __init__(self, terminal, user=None, logger=None):
        """Sets the respective terminal and logger."""
        super().__init__(user or 'termgr', terminal, logger=logger)

    @property
    def resolution(self):
        """Returns the display resolution."""
        return self.execute('export DISPLAY=:0 \\; xrandr | grep " connected"')

    def sudo(self, cmd, *args):
        """Execute a command with sudo."""
        return self.execute('/usr/bin/sudo', cmd, *args)

    def pacman(self, *args):
        """Issues a pacman command."""
        return self.sudo('/usr/bin/pacman', '--noconfirm', *args)

    def reboot(self):
        """Reboots the terminal."""
        with self.extra_options(REBOOT_OPTIONS):
            return self.sudo('/usr/bin/reboot')

    def cleanup(self):
        """Cleanup local package cache."""
        return self.pacman('-Sc')

    def update(self):
        """Update package databases."""
        return self.pacman('-Sy')

    def stage(self):
        """Stage current packages."""
        return self.pacman('-Suw')

    def upgrade(self):
        """Performs a system upgrade."""
        return self.pacman('-Su')

    def install(self, *pkgs, asexplicit=False):
        """Installs software packages."""
        if asexplicit:
            return self.pacman('-S', '--asexplicit', *pkgs)

        return self.pacman('-S', *pkgs)

    def remove(self, *pkgs, cascade=False, nosave=False,
               recursive=False, unneeded=False):
        """Removes packages."""
        options = []

        if cascade:
            options.append('--cascade')

        if nosave:
            options.append('--nosave')

        if recursive:
            options.append('--recursive')

        if unneeded:
            options.append('--unneeded')

        for pkg in pkgs:
            options.append(str(pkg))

        return self.pacman(options, '-R', *options)

    def unlock(self):
        """Removes the pacman lockfile."""
        if self.execute('/usr/bin/pidof', 'pacman'):
            self.logger.error('Pacman is still running on {}.'.format(
                self.terminal))
            return False

        return self.sudo('/usr/bin/rm', '-f ', '/var/lib/pacman/db.lck')
