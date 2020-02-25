"""Terminal setup configuration."""

from logging import getLogger

from configlib import loadcfg


__all__ = ['CONFIG', 'LOG_FORMAT', 'LOGGER', 'SYSTEMD_NETWORKD']


CONFIG = loadcfg('termgr.conf')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger('termgr')
SYSTEMD_NETWORKD = 'systemd-networkd'
