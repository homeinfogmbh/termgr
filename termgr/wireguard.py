"""Wireguard configuration."""

from pathlib import Path
from subprocess import check_call

from terminallib import System, WireGuard
from terminallib.orm.wireguard import NETWORK, SERVER

from termgr.common import SystemdUnit
from termgr.config import CONFIG, LOGGER


__all__ = ['get_wireguard_config', 'write_units', 'update_wireguard']


NETDEV_UNIT_FILE = Path('/etc/systemd/network/terminals.netdev')
NETWORK_UNIT_FILE = Path('/etc/systemd/network/terminals.network')


def get_systems():
    """Yields WireGuard enabled systems."""

    return System.select().join(WireGuard).where(~ (WireGuard.pubkey >> None))


def get_configured_routes():
    """Yields the configured routes."""

    for route in CONFIG['WireGuard']['routes'].split(','):
        destination, gateway = route.strip().split('via')
        yield {
            'destination': destination.strip(),
            'gateway': gateway.strip(),
            'gateway_onlink': True
        }


def get_netdev_items():
    """Returns the server netdev."""

    unit = SystemdUnit()
    unit.add_section('NetDev')
    unit['NetDev']['Name'] = CONFIG['WireGuard']['devname']
    unit['NetDev']['Kind'] = 'wireguard'
    unit['NetDev']['Description'] = CONFIG['WireGuard']['description']
    unit.add_section('WireGuard')
    unit['WireGuard']['ListenPort'] = CONFIG['WireGuard']['port']
    unit['WireGuard']['PrivateKey'] = CONFIG['WireGuard']['private_key']
    yield unit

    psk = CONFIG['WireGuard'].get('psk')
    allowed_ips = [route['destination'] for route in get_configured_routes()]

    for system in get_systems():
        unit = SystemdUnit()
        unit.add_section('WireGuardPeer')
        unit['WireGuardPeer']['PublicKey'] = system.wireguard.pubkey

        if psk:
            unit['WireGuardPeer']['PresharedKey'] = psk

        my_ips = [str(system.wireguard.ipv4address) + '/32'] + allowed_ips
        unit['WireGuardPeer']['AllowedIPs'] = ', '.join(my_ips)
        yield unit


def write_netdev():
    """Writes the netdev configuration."""

    with NETDEV_UNIT_FILE.open('w') as netdev:
        for unit in get_netdev_items():
            unit.write(netdev)


def get_network_unit():
    """Returns a network unit."""

    unit = SystemdUnit()
    unit.add_section('Match')
    unit['Match']['Name'] = CONFIG['WireGuard']['devname']
    unit.add_section('Network')
    unit['Network']['Address'] = str(SERVER) + '/32'
    bind_carrier = CONFIG['WireGuard'].get('bind_carrier')

    if bind_carrier:
        unit['Network']['BindCarrier'] = bind_carrier

    unit.add_section('Route')
    unit['Route']['Destination'] = str(NETWORK)
    unit['Route']['Gateway'] = str(SERVER)
    return unit


def write_network():
    """Writes the network configuration."""

    unit = get_network_unit()

    with NETWORK_UNIT_FILE.open('w') as network:
        unit.write(network)


def write_units():
    """Write unit files."""

    LOGGER.info('Writing netdev file.')
    write_netdev()
    LOGGER.info('Writing network file.')
    write_network()


def update_wireguard():
    """Updates the network units via sudo."""

    return check_call(('/usr/bin/sudo', '/usr/local/bin/termgr', 'mkwg'))


def get_client_routes():
    """Yields configured routes."""

    yield {
        'destination': str(NETWORK),
        'gateway': str(SERVER),
        'gateway_onlink': True
    }
    yield from get_configured_routes()


def get_wireguard_config(system):
    """Returns a JSON-ish WireGuard configuration
    for the specified system.
    """

    endpoint = CONFIG['WireGuard']['endpoint']
    port = CONFIG.getint('WireGuard', 'port')
    return {
        'ipaddress': str(system.wireguard.ipv4address) + '/32',
        'server_pubkey': CONFIG['WireGuard']['pubkey'],
        'psk': CONFIG['WireGuard'].get('psk'),
        'pubkey': system.wireguard.pubkey,
        'endpoint': f'{endpoint}:{port}',
        'routes': list(get_client_routes()),
        'persistent_keepalive': CONFIG.getint(
            'WireGuard', 'persistent_keepalive')
    }
