"""Remote terminal controller."""

from fancylog import Logger
from terminallib import RemoteController


__all__ = ['TerminalController', 'TerminalsController']


REBOOT_OPTIONS = {'ServerAliveInterval': 5, 'ServerAliveCountMax': 3}
RESOLUTION_CMD = 'export DISPLAY=:0 \\; xrandr | grep " connected"'
SUDO = '/usr/bin/sudo'
PACMAN = '/usr/bin/pacman'
SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'


class TerminalController(RemoteController):
    """Does stuff on remote terminals."""

    def __init__(self, terminal, user='termgr', logger=None):
        """Sets the respective terminal and logger."""
        super().__init__(user, terminal, logger=logger)

    @property
    def resolution(self):
        """Returns the display resolution."""
        return self.execute(RESOLUTION_CMD, shell=True)

    def sudo(self, cmd, *args):
        """Execute a command with sudo."""
        return self.execute(SUDO, cmd, *args)

    def identify(self, *args):
        """Lets the terminal beep."""
        return self.sudo('/usr/bin/beep', *args)

    def pacman(self, *args):
        """Issues a pacman command."""
        return self.sudo(PACMAN, '--noconfirm', *args)

    def reboot(self):
        """Reboots the terminal."""
        if self.execute('/usr/bin/test', '-x', '/usr/bin/reboot'):
            with self.extra_options(REBOOT_OPTIONS):
                return self.sudo('/usr/bin/reboot')

        return self.sudo(SYSTEMCTL, 'isolate', 'reboot.target')

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

    def enable_application(self):
        """Enables the application."""
        print('DEBUG:', 'Calling enable_application.', flush=True)
        result = self.sudo(SYSTEMCTL, 'enable', '--now', DIGSIG_APP)
        print('DEBUG:', result, flush=True)
        return result

    def disable_application(self):
        """Disables the application."""
        return self.sudo(SYSTEMCTL, 'disable', '--now', DIGSIG_APP)


class TerminalsController:
    """Processes several terminals in parallel."""

    def __init__(self, user='termgr'):
        """Sets terminals, user and logger."""
        self.user = user
        self.logger = Logger(self.__class__.__name__)

    def __getattr__(self, attr):
        """Delegates to the respective controller."""
        return lambda terminal: getattr(self._controller(terminal), attr)

    def _controller(self, terminal):
        """Returns a controller for the respective terminal."""
        return TerminalController(terminal, user=self.user, logger=self.logger)

    def chkres(self, terminal):
        """Checks the resolution."""
        return self._controller(terminal).resolution
