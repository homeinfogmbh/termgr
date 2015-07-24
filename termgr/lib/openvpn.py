"""Library for terminal OpenVPN management"""

from posixpath import join, isfile, basename
from tempfile import NamedTemporaryFile
import tarfile

from homeinfo.lib.system import run
from homeinfo.terminals.abc import TerminalAware
from homeinfo.terminals.config import terminals_config

from ..config import termgr_config
from .err import KeygenError, UnconfiguredError

__all__ = ['OpenVPNKeyMgr', 'OpenVPNConfig', 'OpenVPNPackager']


class OpenVPNKeyMgr(TerminalAware):
    """Manages OpenVPN keys and configuration"""

    @property
    def host_name(self):
        """Returns the appropriate host name"""
        return self.idstr

    @property
    def key_dir(self):
        """Returns the VPN keys' directory"""
        return terminals_config.openvpn['KEYS_DIR']

    @property
    def crt_file(self):
        """Returns the client certificate's file name"""
        return '{0}.crt'.format(self.host_name)

    @property
    def key_file(self):
        """Returns the key file's name"""
        return '{0}.key'.format(self.host_name)

    @property
    def ca_path(self):
        """Returns the full path to the CA's file"""
        return join(self.key_dir, terminals_config.openvpn['CA_FILE'])

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

    def generate(self):
        """Generates an OpenVPN key pair for the terminal"""
        build_script = '/usr/lib/terminals/build-key-terminal'
        key_file_name = '{0}.{1}'.format(
            self.terminal.tid, self.terminal.cid)
        key_file_path = join(terminals_config.openvpn['KEYS_DIR'], key_file_name)
        if isfile(key_file_path):
            raise KeygenError(
                'Keys already exist in: {0}'.format(key_file_name))
        else:
            return run(
                [build_script, terminals_config.openvpn['EASY_RSA_DIR'],
                 key_file_name])

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
                    raise UnconfiguredError(
                        'Missing client certificate: {0}'.format(
                            self.crt_path))
            else:
                raise UnconfiguredError(
                    'Missing client key: {0}'.format(self.key_path))
        else:
            raise UnconfiguredError(
                'Missing CA certificate: {0}'.format(self.ca_path))


class OpenVPNConfig(TerminalAware):
    """Class that renders an OpenVPN configuration
    for the respective terminal
    """

    @property
    def servers(self):
        """List of remote servers"""
        return '\n'.join(
            ('remote {0} {1}'.format(
                s.strip(), terminals_config.openvpn['PORT'])
             for s in termgr_config.openvpn['SERVERS'].split() if s.strip()))

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
        config = config.replace(
            template_caption + search_fill, host_name_caption + replace_fill)
        config = config.replace('<servers>', self.servers)
        return config

    def _render(self, config):
        """Returns the rendered configuration file"""
        host_name = self.idstr
        config = self._render_caption(config, host_name)
        config = config.replace('<ca>', terminals_config.openvpn['CA_FILE'])
        config = config.replace('<host_name>', host_name)
        config = config.replace('<cipher>', terminals_config.openvpn['CIPHER'])
        config = config.replace('<auth>', terminals_config.openvpn['AUTH'])
        return config

    def get(self):
        """Get the OpenVPN"""
        with open('/usr/share/terminals/openvpn.conf.temp', 'r') as temp:
            template = temp.read()
        return self._render(template)


class OpenVPNPackager(TerminalAware):
    """Class that packs an OpenVPN package for the respective
    terminal containing both, the respective OpenVPN keys and
    certificates, as well as its configuration
    """

    def _pack(self, files):
        """Packs a tar.gz file"""
        config_name = '{0}.conf'.format(terminals_config.openvpn['CONFIG_NAME'])
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
                cfg.seek(0)  # Read file from beginning
                files = {
                    'ca': ca_path,
                    'key': key_path,
                    'crt': crt_path,
                    'cfg': cfg.name}
                tar_data = self._pack(files)
            return tar_data
