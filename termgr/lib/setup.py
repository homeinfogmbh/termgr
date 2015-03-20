"""Library for terminal setup management"""

from homeinfolib.passwd import genhtpw, HtpasswdFile
from ..db.terminal import Terminal
from ..config import htpasswd, pacman, openvpn
from posix import system
from tempfile import NamedTemporaryFile
from tarfile import TarFile
from os.path import join, isfile

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['KeygenError', 'DatabaseManager',
           'OpenVPNManager', 'RepositoryManager']


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class TerminalManager():
    """Manages terminals"""

    def __init__(self, cid, tid):
        """Sets user name and password"""
        self._cid = cid
        self._tid = tid

    @property
    def terminal(self):
        """Returns the appropriate terminal"""
        return Terminal.by_ids(self._cid, self._tid)

    @property
    def idstr(self):
        """Returns a unique string identifier"""
        return '.'.join([str(self._tid), str(self._cid)])


class DatabaseManager(TerminalManager):
    """Manages terminal database records"""

    @classmethod
    def add(self, cid, tid):
        """Adds a new terminal"""
        pass

    def delete(self):
        """Deletes the terminal"""
        pass

    def lockdown(self):
        """Lockdown terminal"""
        pass

    def unlock(self):
        """Unlock terminal"""
        pass


class OpenVPNManager(TerminalManager):
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
        """Returns tha CA file's name"""
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

    @property
    def _tar_file(self):
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


class RepositoryManager(TerminalManager):
    """Restricted HOMEINFO repository manager"""

    def generate(self):
        """Returns the pacman repository configuration"""
        passwd = genhtpw()
        htpasswd_file = HtpasswdFile(htpasswd['FILE'])
        user_name = self.idstr
        htpasswd_file.update(user_name, passwd)
        with open(pacman['template'], 'r') as temp:
            pacman_conf = temp.read()
        pacman_conf.replace('<user_name>', user_name)
        pacman_conf.replace('<password>', passwd)
        return pacman_conf

    def revoke(self):
        """Returns the pacman repository configuration"""
        htpasswd_file = HtpasswdFile(htpasswd['FILE'])
        return htpasswd_file.delete(self.idstr)
