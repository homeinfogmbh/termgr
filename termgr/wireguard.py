"""Wireguard configuration."""
from ipaddress import ip_address
from ipaddress import ip_network
from tempfile import NamedTemporaryFile
from typing import NamedTuple

from hwdb import WIREGUARD_NETWORK, WIREGUARD_SERVER, System, WireGuard
from wgtools import clear_peers, set as wg_set

from termgr.config import CONFIG
from termgr.types import IPAddress, IPNetwork


__all__ = ['get_wireguard_config', 'update_peers']


WG = ('/usr/bin/sudo', '/usr/bin/wg')


class Route(NamedTuple):
    """Represents a route."""

    destination: IPNetwork
    gateway: IPAddress
    gateway_onlink: bool

    @classmethod
    def from_string(cls, string):
        """Creates the route from a string representation."""
        destination, gateway = map(str.strip, string.split('via'))
        return cls(ip_network(destination), ip_address(gateway), True)

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'destination': str(self.destination),
            'gateway': str(self.gateway),
            'gateway_onlink': self.gateway_onlink
        }


def get_systems():
    """Yields WireGuard enabled systems."""

    return System.select().join(WireGuard).where(~(WireGuard.pubkey >> None))


def get_configured_routes():
    """Yields the configured routes."""

    for route in CONFIG['WireGuard']['routes'].split(','):
        yield Route.from_string(route.strip())


def get_client_routes():
    """Yields configured routes."""

    yield Route(WIREGUARD_NETWORK, WIREGUARD_SERVER, True)
    yield from get_configured_routes()


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
        'routes': [route.to_json() for route in get_client_routes()],
        'persistent_keepalive': CONFIG.getint(
            'WireGuard', 'persistent_keepalive')
    }


def _add_peers(psk=None):
    """Adds all terminal peers with the respective psk."""

    common_ips = [str(route.destination) for route in get_configured_routes()]
    peers = {}

    for system in get_systems():
        allowed_ips = [str(system.wireguard.ipv4address) + '/32'] + common_ips
        peers[system.wireguard.pubkey] = {'allowed-ips': allowed_ips}

        if psk:
            peers[system.wireguard.pubkey]['preshared-key'] = psk

    if peers:
        wg_set(CONFIG['WireGuard']['devname'], peers=peers, _wg=WG)


def add_peers():
    """Adds all terminal network peers."""

    psk = CONFIG['WireGuard'].get('psk')

    if psk:
        with NamedTemporaryFile('w+') as tmp:
            tmp.write(psk)
            tmp.flush()
            return _add_peers(psk=tmp.name)

    return _add_peers()


def update_peers():
    """Adds a peer to the terminals network."""

    clear_peers(CONFIG['WireGuard']['devname'], _wg=WG)
    add_peers()
