"""Library for terminal htpasswd management"""

from homeinfolib.passwd import genhtpw, HtpasswdFile
from ..config import htpasswd
from .abc import TerminalAware

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['HtpasswdEntry']


class HtpasswdEntry(TerminalAware):
    """Restricted HOMEINFO repository manager"""

    def get(self):
        """Returns the htpasswd entry tuple"""
        return (self.idstr, self.htpasswd)

    def generate(self):
        """Returns the pacman repository configuration"""
        passwd = genhtpw()
        self.terminal.htpasswd = passwd
        try:
            self.terminal.isave()
        except:
            return False
        else:
            htpasswd_file = HtpasswdFile(htpasswd['FILE'])
            user_name = self.idstr
            htpasswd_file.update(user_name, passwd)
            return passwd

    def revoke(self):
        """Returns the pacman repository configuration"""
        htpasswd_file = HtpasswdFile(htpasswd['FILE'])
        d = htpasswd_file.delete(self.idstr)
        self.terminal.htpasswd = None
        try:
            self.terminal.isave()
        except:
            return False
        else:
            return True if d else False
