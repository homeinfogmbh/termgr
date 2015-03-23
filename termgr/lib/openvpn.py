"""Library for terminal OpenVPN management"""

from posix import system
from tempfile import NamedTemporaryFile
from tarfile import TarFile
from os.path import join, isfile
from ..config import openvpn
from .abc import TerminalAware

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['KeygenError', 'OpenVPNKeygen',
           'OpenVPNConfig', 'OpenVPNPackage']


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class OpenVPNKeygen(TerminalAware):
    """Manages OpenVPN keys and configuration"""

    @property
    def host_name(self):
        """Returns the appropriate host name"""
        return self.idstr

    @property
    def key_dir(self):
        """Returns the VPN keys' directory"""
        return join(openvpn['EASY_RSA_DIR'], 'keys')

    @property
    def ca_file(self):
        """Returns the CA file's name"""
        return openvpn['CA_FILE']

    @property
    def crt_file(self):
        """Returns the client certificate's file name"""
        return '.'.join([self.host_name, 'crt'])

    @property
    def key_file(self):
        """Returns the key file's name"""
        return '.'.join([self.host_name, 'key'])

    @property
    def ca_path(self):
        """Returns the full path to the CA's file"""
        return join(self.key_dir, self.ca_file)

    @property
    def crt_path(self):
        """Returns the full path to the client's certificate file"""
        return join(self.key_dir, self.crt_file)

    @property
    def key_path(self):
        """Returns the full path to the client's key file"""
        return join(self.key_dir, self.key_file)

    @property
    def _key_exists(self):
        """Checks if keys have already been generated"""
        if isfile(self.crt_path) and isfile(self.key_path):
            return True
        else:
            return False

    def _build_key(self):
        """Generates a new key for the terminal"""
        host_name = self.idstr
        build_script = openvpn['BUILD_SCRIPT']  # ./build-key-auto
        cmd = ' '.join([build_script, openvpn['EASY_RSA_DIR'], host_name])
        return not system(cmd)

    def generate(self):
        """Returns the public key"""
        if not self._key_exists:
            if not self._build_key():
                raise KeygenError('Cannot build openVPN key')
        return self._tar_file

    def revoke(self):
        """Revokes a terminal's key"""
        if self._key_exists:
            pass    # TODO: implement

    def get(self):
        """Returns the public / private key pair"""
        if (isfile(self.ca_path)
                and isfile(self.key_path)
                and isfile(self.crt_path)):
            return (self.ca_path, self.key_path, self.crt_path)
        else:
            return False


class OpenVPNConfig(TerminalAware):
    """Class that renders an OpenVPN configuration
    for the respective terminal
    """

    def get(self):
        """Get the OpenVPN"""
        host_name = self.idstr
        with open(openvpn['CONFIG_TEMP'], 'r') as cfg_temp:
            config = cfg_temp.read()
        config = config.replace('<host_name>', host_name)
        config = config.replace('(template)', '(rendered)')
        if self.further_servers:
            config = config.replace(';<further_servers>', self.further_servers)
        return config


class OpenVPNPackage(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    @property
    def get(self):
        """Packs the key into a ZIP compressed file"""
        host_name = self.idstr
        with open(openvpn['CONFIG_TEMP'], 'r') as cfg_temp:
            config_temp = cfg_temp.read()
        config = config_temp.replace('<host_name>', host_name)
        config_name = openvpn['CONFIG_NAME']
        with NamedTemporaryFile('wb', suffix='.tar.gz') as tmp:
            with TarFile(mode='w|gz', fileobj=tmp) as tar:
                with NamedTemporaryFile('w') as cfg:
                    cfg.write(config)
                    tar.add(cfg.name, '.'.join([config_name, 'conf']))
                tar.add(self.ca_path, join(config_name, self.ca_file))
                tar.add(self.crt_path, join(config_name, self.crt_file))
                tar.add(self.key_path, join(config_name, self.key_file))
            with open(tmp.name, 'rb') as tar_tmp:
                tar_data = tar_tmp.read()
        return tar_data
