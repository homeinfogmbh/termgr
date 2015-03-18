"""Library for terminal setup management"""

from homeinfolib.passwd import genhtpw, HtpasswdFile
from ..db.terminal import Terminal
from ..config import htpasswd, pacman

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['SetupController']


class TerminalManager():
    """Manages terminals"""

    def __init__(self, cid, tid):
        """Sets user name and password"""
        self._cid = cid
        self._tid = tid

    @property
    def terminal(self):
        """Returns the appropriate terminal"""
        return Terminal.by_ids(self._cid, self._tid)

    @property
    def idstr(self):
        """Returns a unique string identifier"""
        return '.'.join([str(self._tid), str(self._cid)])


class DatabaseManager(TerminalManager):
    """Manages terminal database records"""

    @classmethod
    def add(self, cid, tid):
        """Adds a new terminal"""
        pass

    def delete(self):
        """Deletes the terminal"""
        pass

    def lockdown(self):
        """Lockdown terminal"""
        pass

    def unlock(self):
        """Unlock terminal"""
        pass


class OpenVPNKeyManager(TerminalManager):
    """Manages OpenVPN Keys"""

    def _gen_key(self):
        """Generates a new key for the terminal"""
        host = self.idstr
        

    @property
    def public_key(self):
        """Returns the public key"""
        pass

    @property
    def private_key(self):
        """Returns the private key"""
        pass


class RepositoryManager(TerminalManager):
    """Restricted HOMEINFO repository manager"""

    def generate(self):
        """Returns the pacman repository configuration"""
        passwd = genhtpw()
        htpasswd_file = HtpasswdFile(htpasswd['FILE'])
        user_name = self.idstr
        htpasswd_file.update(user_name, passwd)
        with open(pacman['template'], 'r') as temp:
            pacman_conf = temp.read()
        pacman_conf.replace('<user_name>', user_name)
        pacman_conf.replace('<password>', passwd)
        return pacman_conf

    def revoke(self):
        """Returns the pacman repository configuration"""
        htpasswd_file = HtpasswdFile(htpasswd['FILE'])
        return htpasswd_file.delete(self.idstr)
