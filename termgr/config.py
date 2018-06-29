"""Terminal setup configuration."""

from configlib import INIParser

__all__ = ['CONFIG', 'LOG_FORMAT']


CONFIG = INIParser('/etc/termgr.conf')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
