"""Terminal setup configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['TermgrConfig']


class TermgrConfig(Configuration):
    """Configuration parser enhancement"""

    @property
    def monitoring(self):
        self.load()
        return self['monitoring']

    @property
    def openvpn(self):
        self.load()
        return self['openvpn']

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

termgr_config = TermgrConfig('/etc/termgr.conf')
