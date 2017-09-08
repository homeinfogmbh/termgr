"""Library for terminal OpenVPN management"""

from contextlib import suppress
from pathlib import Path
from tarfile import open as tarfile_open
from tempfile import TemporaryFile, NamedTemporaryFile
from zipfile import ZipFile

from homeinfo.terminals.abc import TerminalAware

__all__ = ['OpenVPNPackager']


KEY_FILE = '{}.key'
CRT_FILE = '{}.crt'
CA_FILE = 'ca.crt'
CONFIG_FILE = 'terminals{}'
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
    def key_file_path(self):
        """Returns the absolute path to the key file"""
        return KEYS_DIR.joinpath(self.key_file)

    @property
    def crt_file_path(self):
        """Returns the absolute path to the certificate file"""
        return KEYS_DIR.joinpath(self.crt_file)

    @property
    def configuration(self):
        """Returns the rendered client configuration file"""
        with open(CFG_TEMP, 'r') as template:
            template = template.read()

        return template.format(
            crtfile=self.crt_file,
            keyfile=self.key_file,
            mtu=self.mtu)

    def zip_file(self, file):
        """ZIPs OpenVPN files for Windows devices."""
        with ZipFile(file, mode='w') as zip_file:
            zip_file.write(str(self.key_file_path), arcname=self.key_file)
            zip_file.write(str(self.crt_file_path), arcname=self.crt_file)
            zip_file.write(str(CA_FILE_PATH), arcname=CA_FILE)

            with NamedTemporaryFile(mode='w+') as cfg:
                cfg.write(self.configuration.replace('\n', '\r\n'))
                cfg.seek(0)
                zip_file.write(cfg.name, arcname=CONFIG_FILE.format('.ovpn'))

    def tar_file(self, file):
        """Tar OpenVPN files for POSIX devices."""
        with tarfile_open(mode='w', fileobj=file) as archive:
            archive.add(str(self.key_file_path), arcname=self.key_file)
            archive.add(str(self.crt_file_path), arcname=self.crt_file)
            archive.add(str(CA_FILE_PATH), arcname=CA_FILE)

            with NamedTemporaryFile(mode='w+') as cfg:
                cfg.write(self.configuration)
                cfg.seek(0)
                archive.add(cfg.name, arcname=CONFIG_FILE.format('.conf'))

    def package(self, windows=False):
        """Packages the files for the specified client"""
        with TemporaryFile(mode='w+b') as tmp:
            if windows:
                self.zip_file(tmp)
            else:
                self.tar_file(tmp)

            tmp.seek(0)
            return tmp.read()
