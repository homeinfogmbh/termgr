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
    def htid(self):
        """Returns the htpasswd-idstr with the '.' replaced by a'_'"""
        return self.idstr.replace('.', '_')

    @property
    def htpasswd_file(self):
        """Returns the htpasswd file"""
        return HtpasswdFile(htpasswd['FILE'])

    def get(self):
        """Returns the htpasswd entry tuple"""
        if self.htpasswd:
            return (self.htid, self.htpasswd)
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
            user_name = self.htid
            self.htpasswd_file.update(user_name, passwd)
            return passwd

    def revoke(self):
        """Returns the pacman repository configuration"""
        d = self.htpasswd_file.delete(self.htid)
        self.terminal.htpasswd = None
        try:
            self.terminal.isave()
        except:
            return False
        else:
            return True if d else False
