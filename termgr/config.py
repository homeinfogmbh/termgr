"""Terminal setup configuration."""

from functools import cache, partial
from logging import getLogger

from configlib import load_config


__all__ = ["LOG_FORMAT", "LOGGER", "SYSTEMD_NETWORKD", "get_config"]


LOG_FORMAT = "[%(levelname)s] %(name)s: %(message)s"
LOGGER = getLogger("termgr")
SYSTEMD_NETWORKD = "systemd-networkd"
get_config = partial(cache(load_config), "termgr.conf")
