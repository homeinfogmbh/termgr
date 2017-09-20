"""Terminal setup configuration"""

from configlib import INIParser

__all__ = ['config']

config = INIParser('/etc/termgr.conf')
