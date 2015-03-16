"""Library for terminal setup management"""

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['SetupController']


class DatabaseManager():
    """Manages terminal database records"""

    def __init__(self, cid, tid):
        """Sets user name and password"""
        self._cid = cid
        self._tid = tid

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


class OpenVPNKeyManager():
    """Manages OpenVPN Keys"""

    def __init__(self, cid, tid):
        """Sets user name and password"""
        self._cid = cid
        self._tid = tid

    @property
    def public_key(self):
        """Returns the public key"""
        pass

    @property
    def private_key(self):
        """Returns the private key"""
        pass


class RepositoryManager():
    """Restricted HOMEINFO repository manager"""

    def __init__(self, cid, tid):
        """Sets user name and password"""
        self._cid = cid
        self._tid = tid

    @property
    def entry(self):
        """Returns the pacman repository configuration"""
        pass
