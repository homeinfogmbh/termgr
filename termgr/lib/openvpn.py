"""Library for terminal OpenVPN management"""

from os.path import join
from tempfile import TemporaryFile, NamedTemporaryFile
from contextlib import suppress

import tarfile

from homeinfo.terminals.abc import TerminalAware

__all__ = ['OpenVPNPackager']


class OpenVPNPackager(TerminalAware):
    """Packs client keys"""

    KEYFILE = '{}.key'
    CRTFILE = '{}.crt'
    CA_FILE = 'ca.crt'
    CONFIG_FILE = 'terminals.conf'
    CFG_TEMP = '/usr/share/terminals/openvpn.conf.temp'
    KEYS_DIR = '/usr/lib/terminals/keys'

    @property
    def key(self):
        """Returns the terminal's key name"""
        with suppress(AttributeError):
            if self.terminal.vpn.key is not None:
                return self.terminal.vpn.key

        return str(self.terminal)

    @property
    def keyfile(self):
        """Returns the respective key file"""
        return self.KEYFILE.format(self.key)

    @property
    def crtfile(self):
        """Returns the respective certificate file"""
        return self.CRTFILE.format(self.key)

    @property
    def mtu(self):
        """Returns the respective MTU value"""
        with suppress(AttributeError):
            return self.terminal.vpn.mtu

    @property
    def keyfile_path(self):
        """Returns the absolute path to the key file"""
        return join(self.KEYS_DIR, self.keyfile)

    @property
    def crtfile_path(self):
        """Returns the absolute path to the certificate file"""
        return join(self.KEYS_DIR, self.crtfile)

    @property
    def cafile_path(self):
        """Returns the absolute path to the CA file"""
        return join(self.KEYS_DIR, self.CA_FILE)

    @property
    def mtu_(self):
        """Returns the respective MTU option"""
        mtu = self.mtu

        if mtu is not None:
            return '{}\n'.format(mtu)
        else:
            return ''

    @property
    def configuration(self):
        """Returns the rendered client configuration file"""
        with open(self.CFG_TEMP, 'r') as config_template_file:
            config_template = config_template_file.read()

        return config_template.format(
            crtfile=self.crtfile,
            keyfile=self.keyfile,
            mtu=self.mtu_)

    def package(self):
        """Packages the files for the specified client"""
        with TemporaryFile(mode='w+b') as tmp:
            with tarfile.open(mode='w', fileobj=tmp) as archive:
                archive.add(self.keyfile_path, arcname=self.keyfile)
                archive.add(self.crtfile_path, arcname=self.crtfile)
                archive.add(self.cafile_path, arcname=self.CA_FILE)

                with NamedTemporaryFile(mode='w+') as cfg:
                    cfg.write(self.configuration)
                    cfg.seek(0)
                    archive.add(cfg.name, arcname=self.CONFIG_FILE)

            tmp.seek(0)
            return tmp.read()
