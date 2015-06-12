"""Terminal setup configuration"""

from configparser import ConfigParser

__all__ = ['monitoring', 'openvpn', 'pacman']

CONFIG_FILE = '/etc/termgr.conf'
config = ConfigParser()
config.read(CONFIG_FILE)

monitoring = config['monitoring']
openvpn = config['openvpn']
pacman = config['pacman']
