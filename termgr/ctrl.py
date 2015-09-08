"""Remote terminal controller"""

from homeinfo.terminals.db import Terminal, Class
from homeinfo.terminals.ctrl import RemoteController

from .lib.openvpn import OpenVPNKeyMgr


__all__ = ['OfflineError', 'TerminalManager']


class OfflineError(Exception):
    """Indicates that a terminal is offline"""

    def __init__(self, terminal):
        """Sets the respective terminal"""
        self.terminal = terminal


class TerminalManager(RemoteController):
    """Terminal manager class"""

    def __init__(self, terminal, keyfile=None, white_list=None, bl=None):
        """Initializes the manager"""
        super().__init__(
            'termgr', terminal, keyfile=keyfile,
            white_list=white_list, bl=bl)

    def __bool__(self):
        """Returns the terminal's status"""
        return self.terminal.status

    @classmethod
    def add(cls, cid, class_, address=None, tid=None, domain=None):
        """Adds a terminal with optional pre-configured address and TID"""
        tid = Terminal.gen_tid(cid, desired=tid)
        class_ = Class.get(Class.id == class_)
        terminal = Terminal()
        terminal.customer = cid
        terminal.tid = tid
        terminal.class_ = class_
        terminal.domain = domain if domain is not None else 1
        terminal.ipv4addr = Terminal.gen_ipv4addr()
        terminal.virtual_display = None
        terminal.location = address
        terminal.deleted = None
        terminal.save()
        key_manager = OpenVPNKeyMgr(terminal)
        key_manager.generate()

    def upgrade(self):
        """Upgrades the respective terminal"""
        if self:
            return self.execute(
                '/usr/bin/sudo', '/usr/bin/pacman', '-Syu', '--noconfirm')
        else:
            raise OfflineError(self.terminal)

    def unlock_pacman_db(self):
        """Removes pacman's database lockfile"""
        if self:
            return self.execute(
                '/usr/bin/sudo', '/usr/bin/rm', '-f', '/var/lib/pacman/db.lck')
        else:
            raise OfflineError(self.terminal)

    def reboot(self):
        """Reboots the terminal"""
        if self:
            return self.execute('/usr/bin/sudo', '/usr/bin/reboot')
        else:
            raise OfflineError(self.terminal)
