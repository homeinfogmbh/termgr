"""Library for terminal OpenVPN management."""

from pathlib import Path
from tarfile import open as TarFile
from tempfile import TemporaryFile, NamedTemporaryFile
from zipfile import ZipFile
from typing import IO, Tuple

from hwdb import OpenVPN


__all__ = ['package']


KEY_FILE = '{}.key'
CRT_FILE = '{}.crt'
CA_FILE = 'ca.crt'
CONFIG_FILE = 'terminals{}'
CFG_TEMP = Path('/usr/share/terminals/openvpn.conf.temp')
KEYS_DIR = Path('/usr/lib/terminals/keys')
CA_FILE_PATH = KEYS_DIR / CA_FILE
MTU = 'tun-mtu {}\n'


def get_key(openvpn: OpenVPN) -> str:
    """Returns the key name."""

    return openvpn.key or str(openvpn.id)


def get_mtu(openvpn: OpenVPN) -> str:
    """Returns the respective MTU value."""

    if openvpn.mtu is not None:
        return MTU.format(openvpn.mtu)

    return ''


def get_configuration(key_file: Path, crt_file: Path, mtu: str) -> str:
    """Returns the rendered client configuration file."""

    with CFG_TEMP.open('r') as template:
        template = template.read()

    return template.format(crtfile=crt_file, keyfile=key_file, mtu=mtu)


def create_zip_file(openvpn: OpenVPN, file: IO):
    """ZIPs OpenVPN files for Windows devices."""

    key = get_key(openvpn)
    key_file = KEY_FILE.format(key)
    crt_file = CRT_FILE.format(key)
    mtu = get_mtu(openvpn)
    key_file_path = KEYS_DIR / key_file
    crt_file_path = KEYS_DIR / crt_file
    configuration = get_configuration(key_file, crt_file, mtu)
    configuration = configuration.replace('\n', '\r\n')

    with ZipFile(file, mode='w') as zip_file:
        zip_file.write(str(key_file_path), arcname=key_file)
        zip_file.write(str(crt_file_path), arcname=crt_file)
        zip_file.write(str(CA_FILE_PATH), arcname=CA_FILE)

        with NamedTemporaryFile(mode='w+') as cfg:
            cfg.write(configuration)
            cfg.flush()
            zip_file.write(cfg.name, arcname=CONFIG_FILE.format('.ovpn'))


def create_tar_file(openvpn: OpenVPN, file: IO):
    """Tar OpenVPN files for POSIX devices."""

    key = get_key(openvpn)
    key_file = KEY_FILE.format(key)
    crt_file = CRT_FILE.format(key)
    mtu = get_mtu(openvpn)
    key_file_path = KEYS_DIR / key_file
    crt_file_path = KEYS_DIR / crt_file
    configuration = get_configuration(key_file, crt_file, mtu)

    with TarFile(mode='w', fileobj=file) as tar_file:
        tar_file.add(str(key_file_path), arcname=key_file)
        tar_file.add(str(crt_file_path), arcname=crt_file)
        tar_file.add(str(CA_FILE_PATH), arcname=CA_FILE)

        with NamedTemporaryFile(mode='w+') as cfg:
            cfg.write(configuration)
            cfg.flush()
            tar_file.add(cfg.name, arcname=CONFIG_FILE.format('.conf'))


def package(openvpn: OpenVPN, windows: bool = False) -> Tuple[bytes, str]:
    """Packages the files for the specified client."""

    key = get_key(openvpn)

    with TemporaryFile(mode='w+b') as tmp:
        if windows:
            create_zip_file(openvpn, tmp)
            filename = f'{key}.zip'
        else:
            create_tar_file(openvpn, tmp)
            filename = f'{key}.tar'

        tmp.flush()
        tmp.seek(0)
        return (tmp.read(), filename)
