"""Library for terminal OpenVPN management"""

from os.path import join

from homeinfo.terminals.abc import TerminalAware
from homeinfo.terminals.orm import VPNUnconfiguredError

__all__ = ['OpenVPNPackager']


class OpenVPNPackager(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    ARCDIR = '/usr/lib/terminals/keys'

    def package(self):
        """Packs the key into a ZIP compressed file"""
        if self.terminal.vpn is not None:
            keyname = self.terminal.vpn.key or str(self.terminal)
            tarname = '{}.tar'.format(keyname)
            tarpath = join(self.ARCDIR, tarname)

            with open(tarpath, 'rb') as tar_file:
                return tar_file.read()
        else:
            raise VPNUnconfiguredError(str(self.terminal))
