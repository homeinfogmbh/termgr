"""Library for terminal OpenVPN management"""

from os.path import join

from homeinfo.terminals.abc import TerminalAware

__all__ = ['UnconfiguredError', 'OpenVPNPackager']


class OpenVPNPackager(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    ARCDIR = '/usr/lib/terminals/keys'

    def __call__(self):
        """Packs the key into a ZIP compressed file"""
        keyname = self.terminal.vpn.key or str(self.terminal)
        tarname = '{0}.tar'.format(keyname)
        tarpath = join(self.ARCDIR, tarname)
        with open(tarpath, 'rb') as tar_file:
            return tar_file.read()
