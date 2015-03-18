"""Library for htpasswd entry management"""

from string import ascii_letters, digits
from random import choice
from ..config import htpasswd

__date__ = "18.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['Htpasswd']


class Htpasswd():
    """Wraps a terminal to manage htpasswd entries for it"""

    def __init__(self, terminal):
        """Sets the resprctive terminal"""
        self._terminal = terminal

    @property
    def _records(self):
        """Returns the terminal's htpasswd entry"""
        with open(htpasswd['FILE'], 'r') as f:
            for line in f.readlines():
                user_name, passwd_hash = line.strip().split(':')
                yield (user_name, passwd_hash)

    def _store(self, records):
        """Store records"""
        result = True
        with open(htpasswd['FILE'], 'w') as f:
            for record in records:
                record += '\n'
                result = f.write(record) and result

    @property
    def htpasswds(self):
        """Returns all htpasswd entries for the respctive terminal"""
        for user_name, passwd_hash in self._records:
            if user_name == repr(self._terminal):
                yield passwd_hash

    @property
    def htpasswd(self):
        """Returns the first htpasswd entry for the respctive terminal"""
        for passwd_hash in self.htpasswds:
            return passwd_hash

    @htpasswd.setter
    def htpasswd(self, passwd_hash):
        """Sets the htpasswd entry for the terminal"""
        self.purge()    # Remove all existing entries for this terminal
        entry = ':'.join([repr(self._terminal), passwd_hash, '\n'])
        with open(htpasswd['FILE'], 'w') as f:
            f.write(entry)

    def remove(self, htpasswd):
        """remove a certain htpasswd entry for the respective terminal"""
        return self._store([(user_name, passwd_hash)
                            for user_name, passwd_hash in self._records
                            if user_name == repr(self._terminal)
                            and passwd_hash != htpasswd])

    def purge(self):
        """Remove all entries for the respective terminal"""
        return self._store([(user_name, passwd_hash)
                            for user_name, passwd_hash in self._records
                            if user_name == repr(self._terminal)])

    def _randomize(self, length=16):
        """Create a random htpasswd hash"""
        pool = ascii_letters + digits
        result = ''
        while len(result) < length:
            result += choice(pool)
        return result
