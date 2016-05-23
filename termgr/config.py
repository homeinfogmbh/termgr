"""Terminal setup configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['CONFIG']


class TermgrConfig(Configuration):
    """Configuration parser enhancement"""

    @property
    def db(self):
        self.load()
        return self['db']

    @property
    def pacman(self):
        self.load()
        return self['pacman']

    @property
    def ssh(self):
        self.load()
        return self['ssh']

    @property
    def screenshot(self):
        self.load()
        return self['screenshot']


CONFIG = TermgrConfig('/etc/termgr.conf')
