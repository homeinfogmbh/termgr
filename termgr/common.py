"""Common stuff."""

from configparser import ConfigParser


__all__ = ['SystemdUnit']


class SystemdUnit(ConfigParser):    # pylint: disable=R0901
    """A systemd unit."""

    def optionxform(self, optionstr):
        """Returns the option as stripped value."""
        if optionstr is None:
            return None

        return optionstr.strip()
