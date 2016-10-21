"""Remote terminal controller"""

from homeinfo.lib.log import Logger, LogLevel
from homeinfo.terminals.ctrl import RemoteController


__all__ = ['TerminalController']


class TerminalsController():
    """Processes several terminals in parallel"""

    def __init__(self, user=None):
        """Sets terminals, user and logger"""
        self.user = user
        self.logger = Logger(self.__class__.__name__, level=LogLevel.DEBUG)

    def _controller(self, terminal):
        """Returns a controller for the respective terminal"""
        return TerminalController(terminal, user=self.user, logger=self.logger)

    @property
    def reboot(self):
        """Reboots the terminal"""
        def proxy(terminal):
            return self._controller(terminal).reboot()

        return proxy

    @property
    def cleanup(self):
        """Cleans up package chache"""
        def proxy(terminal):
            return self._controller(terminal).cleanup()

        return proxy

    @property
    def update(self, *pkgs):
        """Updates packages"""
        def proxy(terminal):
            return self._controller(terminal).update()

        return proxy

    @property
    def stage(self, *pkgs):
        """Stage packages"""
        def proxy(terminal):
            return self._controller(terminal).stage()

        return proxy

    @property
    def upgrade(self):
        """Stage packages"""
        def proxy(terminal):
            return self._controller(terminal).upgrade()

        return proxy

    @property
    def unlock(self):
        """Unlocks the package manager"""
        def proxy(terminal):
            return self._controller(terminal).unlock()

        return proxy

    @property
    def chkres(self):
        """Checks the resolution"""
        def proxy(terminal):
            return self._controller(terminal).resolution

        return proxy

    def install(self, *pkgs, asexplicit=False):
        """Installs software packages"""
        def proxy(terminal):
            return self._controller(terminal).upgrade(
                *pkgs, asexplicit=asexplicit)

        return proxy


class TerminalController(RemoteController):
    """Does stuff on remote terminals"""

    def __init__(self, terminal, user=None, logger=None):
        """Sets the respective terminal and logger"""
        user = 'termgr' if user is None else user
        super().__init__(user, terminal, logger=logger)

    @property
    def resolution(self):
        """Returns the display resolution"""
        return self.execute('export DISPLAY=:0 \; xrandr | grep " connected"')

    def sudo(self, cmd, *args):
        """Execute a command with sudo"""
        return self.execute('/usr/bin/sudo', cmd, *args)

    def pacman(self, *args):
        """Issues a pacman command"""
        return self.sudo('/usr/bin/pacman', '--noconfirm', *args)

    def reboot(self):
        """Reboots the terminal"""
        return self.sudo('/usr/bin/reboot')

    def cleanup(self):
        """Cleanup local package cache"""
        return self.pacman('-Sc')

    def update(self):
        """Update package databases"""
        return self.pacman('-Sy')

    def stage(self):
        """Stage current packages"""
        return self.pacman('-Suw')

    def upgrade(self):
        """Performs a system upgrade"""
        return self.pacman('-Su')

    def install(self, *pkgs, asexplicit=False):
        """Installs software packages"""
        if asexplicit:
            return self.pacman('-S', '--asexplicit', *pkgs)
        else:
            return self.pacman('-S', *pkgs)

    def remove(self, *pkgs, cascade=False, nosave=False,
               recursive=False, unneeded=False):
        """Removes packages"""
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
        """Removes the pacman lockfile"""
        if self.execute('/usr/bin/pidof', 'pacman'):
            self.logger.error('Pacman is still running on {}'.format(
                self.terminal))
        else:
            return self.sudo('/usr/bin/rm', '-f ', '/var/lib/pacman/db.lck')
