"""Wireguard configuration."""

from terminallib.orm.wireguard import NETWORK, SERVER

from termgr.config import CONFIG


__all__ = ['get_wireguard_config']


def get_routes():
    """Yields configured routes."""

    yield {
        'destination': str(NETWORK),
        'gateway': str(SERVER),
        'gateway_onlink': True
    }

    # Read additional routes.
    for route in CONFIG['WireGuard']['routes'].split(','):
        destination, gateway = route.strip().split('via')
        yield {
            'destination': destination.strip(),
            'gateway': gateway.strip(),
            'gateway_onlink': True
        }


def get_wireguard_config(system):
    """Returns a JSON-ish WireGuard configuration
    for the specified system.
    """

    return {
        'ipaddress': str(system.wireguard.ipv4address) + '/32',
        'server_pubkey': CONFIG['WireGuard']['pubkey'],
        'psk': CONFIG['WireGuard'].get('psk'),
        'pubkey': system.wireguard.pubkey,
        'endpoint': CONFIG['WireGuard']['endpoint'],
        'routes': tuple(get_routes()),
        'persistent_keepalive': CONFIG.getint(
            'WireGuard', 'persistent_keepalive')
    }
