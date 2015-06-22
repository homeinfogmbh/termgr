"""Terminal setup configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['TermgrConfig']


class TermgrConfig(Configuration):
    """Configuration parser enhancement"""

    def __init__(self, file):
        """Initializes the main configuration file parser"""
        super().__init__()
        self._file = file

    def __enter__(self):
        """Loads the configuration"""
        self.load()
        return self

    def __exit__(self, *_):
        """Exists the with statement"""
        pass

    def load(self):
        """Reads the configuration file"""
        return self.read(self._file)

    @property
    def monitoring(self):
        return self['monitoring']

    @property
    def openvpn(self):
        return self['openvpn']

    @property
    def pacman(self):
        return self['pacman']

    @property
    def ssh(self):
        return self['ssh']

    @property
    def screenshot(self):
        return self['screenshot']

termgr_config = TermgrConfig('/etc/termgr.conf')
