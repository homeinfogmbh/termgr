"""Library for terminal OpenVPN management"""

from posix import system
from posixpath import join, isfile, basename
from tempfile import NamedTemporaryFile
import tarfile
from ..config import openvpn
from .abc import TerminalAware
from .err import KeygenError, UnconfiguredError

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['OpenVPNKeyMgr', 'OpenVPNConfig', 'OpenVPNPackage']


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
        return join(self.key_dir, openvpn['CA_FILE'])

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
            else:
                return True
        else:
            return False    # Already exists

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
    def servers(self):
        """List of remote servers"""
        return '\n'.join((s.strip() for s in openvpn['SERVERS'].split(',')))

    def _render_caption(self, config, host_name):
        """Renders the openvpn-config file's caption / header"""
        template_caption = '(template)'
        host_name_caption = ''.join(['(', host_name, ')'])
        len_diff = len(host_name_caption) - len(template_caption)
        if len_diff > 0:
            search_fill = ''.join((' ' for _ in range(0, len_diff)))
            replace_fill = ''
        elif len_diff < 0:
            search_fill = ''
            replace_fill = ''.join((' ' for _ in range(0, -len_diff)))
        else:
            search_fill = ''
            replace_fill = ''
        config = config.replace(template_caption + search_fill,
                                host_name_caption + replace_fill)
        config = config.replace('<servers>', self.servers)
        return config

    def _render(self, config):
        """Returns the rendered configuration file"""
        host_name = self.idstr
        config = self._render_caption(config, host_name)
        config = config.replace('<ca>', openvpn['CA_FILE'])
        config = config.replace('<host_name>', host_name)
        config = config.replace('<cipher>', openvpn['CIPHER'])
        config = config.replace('<auth>', openvpn['AUTH'])
        return config

    def get(self):
        """Get the OpenVPN"""
        with open(openvpn['CONFIG_TEMP'], 'r') as cfg_temp:
            config = cfg_temp.read()
        return self._render(config)


class OpenVPNPackage(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    def _pack(self, files, config_name):
        """Packs a tar.gz file"""
        with NamedTemporaryFile('w+b', suffix='.tar.gz') as tmp:
            with tarfile.open(mode='w:gz', fileobj=tmp) as tar:
                tar.add(files['ca'], basename(files['ca']))
                tar.add(files['key'], basename(files['key']))
                tar.add(files['crt'], basename(files['crt']))
                tar.add(files['cfg'], config_name)
            tmp.seek(0)
            tar_data = tmp.read()
        return tar_data

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
            with NamedTemporaryFile('w+') as cfg:
                cfg.write(config)
                cfg.seek(0)
                files = {'ca': ca_path,
                         'key': key_path,
                         'crt': crt_path,
                         'cfg': cfg.name}
                config_name = '.'.join([openvpn['CONFIG_NAME'], 'conf'])
                tar_data = self._pack(files, config_name)
            return tar_data
