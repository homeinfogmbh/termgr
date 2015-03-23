"""Library for terminal htpasswd management"""

from homeinfolib.passwd import genhtpw, HtpasswdFile
from ..config import htpasswd
from .abc import TerminalAware
from .err import UnconfiguredError

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['HtpasswdEntry']


class HtpasswdEntry(TerminalAware):
    """Restricted HOMEINFO repository manager"""

    @property
    def htpasswd(self):
        """Returns the respective terminal's htpasswd entry"""
        return self.terminal.htpasswd

    @property
    def htpasswd_file(self):
        """Returns the htpasswd file"""
        return HtpasswdFile(htpasswd['FILE'])

    def get(self):
        """Returns the htpasswd entry tuple"""
        if self.htpasswd:
            return (self.idstr, self.htpasswd)
        else:
            raise UnconfiguredError('No htpasswd-password configured')

    def generate(self):
        """Returns the pacman repository configuration"""
        passwd = genhtpw()
        self.terminal.htpasswd = passwd
        try:
            self.terminal.isave()
        except:
            return False
        else:
            user_name = self.idstr
            self.htpasswd_file.update(user_name, passwd)
            return passwd

    def revoke(self):
        """Returns the pacman repository configuration"""
        d = self.htpasswd_file.delete(self.idstr)
        self.terminal.htpasswd = None
        try:
            self.terminal.isave()
        except:
            return False
        else:
            return True if d else False
