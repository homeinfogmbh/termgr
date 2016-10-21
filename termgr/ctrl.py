"""Remote terminal controller"""

from homeinfo.lib.log import Logger, LogLevel, TTYAnimation
from homeinfo.lib.system import Parallelization
from homeinfo.terminals.ctrl import RemoteController


__all__ = ['TerminalController']


class TerminalsController():
    """Processes several terminals in parallel"""

    def __init__(self, terminals, user=None):
        """Sets terminals, user and logger"""
        self.terminals = list(terminals)
        self.user = user
        self.logger = Logger(self.__class__.__name__, level=LogLevel.NONE)

    def _reboot(self, terminal):
        """Proxy a single terminal reboot"""
        return TerminalController(
            terminal, user=self.user, logger=self.logger).reboot()

    def _cleanup(self, terminal):
        """Proxy a single terminal cleanup"""
        return TerminalController(
            terminal, user=self.user, logger=self.logger).cleanup()

    def _update(self, terminal):
        """Proxy a single terminal upgrade"""
        return TerminalController(
            terminal, user=self.user, logger=self.logger).update()

    def reboot(self):
        """Reboots all terminals"""
        with Parallelization(
                self._reboot, self.terminals, single=True) as para:
            with TTYAnimation(para, refresh=3):
                para.wait()

    def cleanup(self):
        """Updates all terminals"""
        with Parallelization(
                self._cleanup, self.terminals, single=True) as para:
            with TTYAnimation(para, refresh=3):
                para.wait()

    def update(self):
        """Updates all terminals"""
        with Parallelization(
                self._update, self.terminals, single=True) as para:
            with TTYAnimation(para, refresh=3):
                para.wait()


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
