"""Terminal setup configuration."""

from configlib import loadcfg


__all__ = ['CONFIG', 'LOG_FORMAT']


CONFIG = loadcfg('termgr.conf')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
