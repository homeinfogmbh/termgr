"""Library for terminal OpenVPN management"""

from pathlib import Path
from tempfile import TemporaryFile, NamedTemporaryFile
from contextlib import suppress

import tarfile

from homeinfo.terminals.abc import TerminalAware

__all__ = ['OpenVPNPackager']


KEY_FILE = '{}.key'
CRT_FILE = '{}.crt'
CA_FILE = 'ca.crt'
CONFIG_FILE_POSIX = 'terminals.conf'
CONFIG_FILE_WINDOWS = 'terminals.ovpn'
CFG_TEMP = '/usr/share/terminals/openvpn.conf.temp'
KEYS_DIR = Path('/usr/lib/terminals/keys')
CA_FILE_PATH = KEYS_DIR.joinpath(CA_FILE)
MTU = 'tun-mtu {}\n'


class OpenVPNPackager(TerminalAware):
    """Packs client keys"""

    @property
    def key(self):
        """Returns the terminal's key name"""
        with suppress(AttributeError):
            if self.terminal.vpn.key is not None:
                return self.terminal.vpn.key

        return str(self.terminal)

    @property
    def key_file(self):
        """Returns the respective key file"""
        return KEY_FILE.format(self.key)

    @property
    def crt_file(self):
        """Returns the respective certificate file"""
        return CRT_FILE.format(self.key)

    @property
    def mtu(self):
        """Returns the respective MTU value"""
        if self.terminal.vpn is not None:
            if self.terminal.vpn.mtu is not None:
                return MTU.format(self.terminal.vpn.mtu)

        return ''

    @property
    def keyfile_path(self):
        """Returns the absolute path to the key file"""
        return KEYS_DIR.joinpath(self.keyfile)

    @property
    def crtfile_path(self):
        """Returns the absolute path to the certificate file"""
        return KEYS_DIR.joinpath(self.crtfile)

    @property
    def configuration(self):
        """Returns the rendered client configuration file"""
        with open(CFG_TEMP, 'r') as template:
            template = template.read()

        return template.format(
            crtfile=self.crtfile,
            keyfile=self.keyfile,
            mtu=self.mtu)

    def package(self, windows=False):
        """Packages the files for the specified client"""
        with TemporaryFile(mode='w+b') as tmp:
            with tarfile.open(mode='w', fileobj=tmp) as archive:
                archive.add(str(self.keyfile_path), arcname=self.key_file)
                archive.add(str(self.crtfile_path), arcname=self.crt_file)
                archive.add(str(CA_FILE_PATH), arcname=CA_FILE)

                with NamedTemporaryFile(mode='w+') as cfg:
                    if windows:
                        cfg.write(self.configuration.replace('\n', '\r\n'))
                        arcname = CONFIG_FILE_WINDOWS
                    else:
                        cfg.write(self.configuration)
                        arcname = CONFIG_FILE_POSIX

                    cfg.seek(0)
                    archive.add(cfg.name, arcname=arcname)

            tmp.seek(0)
            return tmp.read()
