"""Remote terminal controller."""

from logging import getLogger
from subprocess import CalledProcessError

from terminallib import RemoteController


__all__ = ['SystemController', 'SystemsController']


RESOLUTION_CMD = 'export DISPLAY=:0 \\; xrandr | grep " connected"'
SUDO = '/usr/bin/sudo'
SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
ADMIN_USER = 'homeinfo'
REBOOT_COMMAND = (SYSTEMCTL, 'reboot')
REBOOT_OPTIONS = {'ServerAliveInterval': 5, 'ServerAliveCountMax': 3}
LOGGER = getLogger('Controller')


class SystemController(RemoteController):
    """Does stuff on remote system."""

    def __init__(self, system, user='termgr'):
        """Sets the respective system and logger."""
        super().__init__(user, system)

    @property
    def resolution(self):
        """Returns the display resolution."""
        return self.execute(RESOLUTION_CMD, shell=True)

    def check_pacman(self):
        """Determines if pacman is (probably) running."""
        try:
            return self.sudo('/usr/bin/test', '-f ', '/var/lib/pacman/db.lck')
        except CalledProcessError:
            return False

    def sudo(self, cmd, *args):
        """Execute a command with sudo."""
        return self.execute(SUDO, cmd, *args)

    def identify(self, *args):
        """Lets the terminal beep."""
        return self.execute('/usr/bin/beep', *args)

    def systemctl(self, *args):
        """Issues a systemctl command."""
        return self.sudo(SYSTEMCTL, *args)

    def reboot(self):
        """Reboots the terminal."""
        with self.extra_options(REBOOT_OPTIONS):
            return self.sudo(*REBOOT_COMMAND)

    def update(self):
        """Downloads package updates."""
        return self.systemctl('start', 'pacman-update.service')

    def upgrade(self):
        """Performs a system upgrade."""
        return self.systemctl('start', 'pacman-upgrade.service')

    def unlock(self):
        """Removes the pacman lockfile."""
        if self.execute('/usr/bin/pidof', 'pacman'):
            LOGGER.error('Pacman is still running on %s.', self.system)
            return False

        return self.sudo('/usr/bin/rm', '-f ', '/var/lib/pacman/db.lck')

    def enable_application(self):
        """Enables the application."""
        return self.sudo(SYSTEMCTL, 'enable', '--now', DIGSIG_APP)

    def disable_application(self):
        """Disables the application."""
        return self.sudo(SYSTEMCTL, 'disable', '--now', DIGSIG_APP)

    def check_login(self, user=ADMIN_USER):
        """Checks whether the respective user is logged in."""
        try:
            return self.execute('/usr/bin/loginctl', 'user-status', user)
        except CalledProcessError:
            return False


class SystemsController:
    """Processes several terminals in parallel."""

    def __init__(self, user='termgr'):
        """Sets terminals, user and logger."""
        self.user = user

    def __getattr__(self, attr):
        """Delegates to the respective controller."""
        return lambda terminal: getattr(self._controller(terminal), attr)()

    def _controller(self, terminal):
        """Returns a controller for the respective terminal."""
        return SystemController(terminal, user=self.user)

    def chkres(self, terminal):
        """Checks the resolution."""
        return self._controller(terminal).resolution
