"""Terminal setup configuration."""

from configlib import INIParser

__all__ = ['config']

CONFIG = INIParser('/etc/termgr.conf')
