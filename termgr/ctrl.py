"""Remote terminal controller."""

from logging import getLogger

from terminallib import RemoteController


__all__ = [
    'closed_by_remote_host',
    'TerminalController',
    'TerminalsController']


REBOOT_OPTIONS = {'ServerAliveInterval': 5, 'ServerAliveCountMax': 3}
RESOLUTION_CMD = 'export DISPLAY=:0 \\; xrandr | grep " connected"'
SUDO = '/usr/bin/sudo'
PACMAN = '/usr/bin/pacman'
SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
ADMIN_USER = 'homeinfo'
REBOOT_COMMANDS = (
    ('/usr/bin/reboot',), (SYSTEMCTL, 'isolate', 'reboot.target'),
    (SYSTEMCTL, 'reboot'))


def closed_by_remote_host(process_result):
    """Checks whether the connection was closed by the remote host."""

    try:
        text = process_result.stderr.decode()
    except (AttributeError, ValueError):
        return False

    return 'Connection' in text and 'closed by remote host' in text


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
        """Issues a pacman command.

        If no arguments are given, it checks
        for a running pacman process.
        """
        if not args:
            return self.execute('/usr/bin/pidof', 'pacman')

        return self.sudo(PACMAN, '--noconfirm', *args)

    def reboot(self):
        """Reboots the terminal."""
        with self.extra_options(REBOOT_OPTIONS):
            for reboot_command in REBOOT_COMMANDS:
                result = self.sudo(*reboot_command)

                if result:
                    return result
                elif result.exit_code == 255:
                    if closed_by_remote_host(result):
                        return result

        return result

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
        result = self.sudo(SYSTEMCTL, 'enable', '--now', DIGSIG_APP)
        return result

    def disable_application(self):
        """Disables the application."""
        return self.sudo(SYSTEMCTL, 'disable', '--now', DIGSIG_APP)

    def check_login(self, user=ADMIN_USER):
        """Checks whether the respective user is logged in."""
        return self.execute('/usr/bin/loginctl', 'user-status', user)


class TerminalsController:
    """Processes several terminals in parallel."""

    def __init__(self, user='termgr'):
        """Sets terminals, user and logger."""
        self.user = user
        self.logger = getLogger(self.__class__.__name__)

    def __getattr__(self, attr):
        """Delegates to the respective controller."""
        return lambda terminal: getattr(self._controller(terminal), attr)()

    def _controller(self, terminal):
        """Returns a controller for the respective terminal."""
        return TerminalController(terminal, user=self.user, logger=self.logger)

    def chkres(self, terminal):
        """Checks the resolution."""
        return self._controller(terminal).resolution

    def install(self, *pkgs, asexplicit=False):
        """Callback for the sync command."""
        return lambda terminal: self._controller(terminal).install(
            *pkgs, asexplicit=asexplicit)
