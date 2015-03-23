"""Library for terminal OpenVPN management"""

from posix import system
from tempfile import NamedTemporaryFile
from tarfile import TarFile
from os.path import join, isfile, basename
from ..config import openvpn
from .abc import TerminalAware
from .err import KeygenError, UnconfiguredError

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['KeygenError', 'OpenVPNKeyMgr',
           'OpenVPNConfig', 'OpenVPNPackage']


class OpenVPNKeyMgr(TerminalAware):
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
        if isfile(self.ca_path):
            if isfile(self.key_path):
                if isfile(self.crt_path):
                    return (self.ca_path, self.key_path, self.crt_path)
                else:
                    raise UnconfiguredError(' '.join(['Missing',
                                                      self.crt_path]))
            else:
                raise UnconfiguredError(' '.join(['Missing', self.key_path]))
        else:
            raise UnconfiguredError(' '.join(['Missing', self.ca_path]))


class OpenVPNConfig(TerminalAware):
    """Class that renders an OpenVPN configuration
    for the respective terminal
    """

    @property
    def further_servers(self):
        """List of further servers"""
        return ''   # XXX: Unused

    def get(self):
        """Get the OpenVPN"""
        host_name = self.idstr
        with open(openvpn['CONFIG_TEMP'], 'r') as cfg_temp:
            config = cfg_temp.read()
        config = config.replace('<host_name>', host_name)
        config = config.replace('(template)', '(rendered)')
        config = config.replace(';<further_servers>', self.further_servers)
        return config


class OpenVPNPackage(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    def _pack(self, files, config_name):
        """Packs a tar.gz file"""
        with NamedTemporaryFile('wb', suffix='.tar.gz') as tmp:
            with TarFile(mode='w|gz', fileobj=tmp) as tar:
                tar.add(files['ca'], basename(files['ca']))
                tar.add(files['key'], basename(files['key']))
                tar.add(files['crt'], basename(files['crt']))
                tar.add(files['cfg'], config_name)
            with open(tmp.name, 'rb') as tar_tmp:
                return tar_tmp.read()

    def get(self):
        """Packs the key into a ZIP compressed file"""
        keymgr = OpenVPNKeyMgr(self.terminal)
        configmgr = OpenVPNConfig(self.terminal)
        try:
            ca_path, key_path, crt_path = keymgr.get()
        except UnconfiguredError:
            raise UnconfiguredError('OpenVPN key setup incomplete')
        else:
            config = configmgr.get()
            with NamedTemporaryFile('w') as cfg:
                cfg.write(config)
                files = {'ca': ca_path,
                         'key': key_path,
                         'crt': crt_path,
                         'cfg': cfg.name}
                config_name = '.'.join([openvpn['CONFIG_NAME'], 'conf'])
                return self._pack(files, config_name)
