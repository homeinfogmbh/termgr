"""Terminal controller commands"""

from itertools import chain

from homeinfo.terminals.ctrl import RemoteController

from .tui import printterm

__all__ = [
    'TerminalCommand',
    'RebootCommand',
    'PackageManagerCommand',
    'CheckInitcpioConfig',
    'CheckPacmanConfig',
    'Commands']


TERMGR_USER = 'termgr'

SUDO = '/usr/bin/sudo'
PACMAN = '/usr/bin/pacman'
REBOOT = '/usr/bin/reboot'
REMOVE = '/usr/bin/rm'
GREP = '/usr/bin/grep'


class TerminalCommand():
    """Execute command on terminal"""

    def __init__(self, cmd, *args, user=None):
        self.cmd = cmd
        self.args = args
        self.user = 'termgr' if user is None else user

    def __call__(self, terminal, user=None):
        user = self.user if user is None else user
        remote_controller = self.remote_controller(user, terminal)
        return remote_controller.execute(self.cmd, *self.args)

    def __iter__(self):
        yield self.cmd

        for arg in self.args:
            yield arg

    def __repr__(self):
        return ' '.join(self)

    def remote_controller(self, user, terminal):
        """Get a RemoteController for the
        respective user and terminal
        """
        return RemoteController(user, terminal)


class RebootCommand(TerminalCommand):
    """Controller to reboot terminal"""

    def __init__(self):
        super().__init__(SUDO, REBOOT)

    def remote_controller(self, user, terminal):
        """Get a RemoteController for the
        respective user and terminal
        """
        remote_controller = RemoteController(user, terminal)
        remote_controller.ssh_custom_opts = {
            'ServerAliveInterval': 1,
            'ServerAliveCountMax': 2}
        return remote_controller


class PackageManagerCommand(TerminalCommand):
    """Automatically uses the package manager"""

    BASE_PKGS = ['openvpn', 'openssh', 'wget', 'beep']

    def __init__(self, packages, *args, user=None):
        self.packages = packages

        if packages:
            args = [a for a in chain(args, packages)]
        else:
            args = args

        super().__init__(SUDO, PACMAN, '--noconfirm', *args, user=user)


class CheckInitcpioConfig():
    """Checks settings inside the /etc/mkinitcpio.conf"""

    MODULES = TerminalCommand(GREP, '^MODULES=', '/etc/mkinitcpio.conf')
    HOOKS = TerminalCommand(GREP, '^HOOKS=', '/etc/mkinitcpio.conf')
    COMPRESSION = TerminalCommand(
        GREP, '^COMPRESSION=', '/etc/mkinitcpio.conf')

    def __init__(self, modules=False, hooks=False, compression=False):
        self.modules = modules
        self.hooks = hooks
        self.compression = compression

    def __call__(self, terminal, user=None):
        if self.modules:
            printterm(terminal, self.MODULES(terminal, user=user))

        if self.hooks:
            printterm(terminal, self.HOOKS(terminal, user=user))

        if self.compression:
            printterm(terminal, self.COMPRESSION(terminal, user=user))


class CheckPacmanConfig():
    """Checks settings inside the /etc/pacman.conf"""

    SIG_LEVEL = TerminalCommand(GREP, '^SigLevel', '/etc/pacman.conf')

    def __init__(self, siglevel=False):
        self.siglevel = siglevel

    def __call__(self, terminal, user=None):
        if self.siglevel:
            printterm(terminal, self.SIG_LEVEL(terminal, user=user))


class Commands():
    """Commonly used commands"""

    @staticmethod
    def INSTALL_PKGS(*packages):
        return PackageManagerCommand(packages, '-S')

    CLEANUP = PackageManagerCommand(None, '-Sc')
    UPDATE = PackageManagerCommand(None, '-Sy')
    STAGE = PackageManagerCommand(None, '-Syuw')
    UPGRADE = PackageManagerCommand(None, '-Su')
    UNLOCK = TerminalCommand(SUDO, REMOVE, '-f ', '/var/lib/pacman/db.lck')
    CHKRES = TerminalCommand('export DISPLAY=:0 \; xrandr | grep " connected"')
    REBOOT = RebootCommand()
