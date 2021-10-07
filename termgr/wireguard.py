"""Wireguard configuration."""
from ipaddress import ip_address
from ipaddress import ip_network
from tempfile import NamedTemporaryFile
from typing import Iterator, NamedTuple, Optional

from peewee import ModelSelect

from hwdb import WIREGUARD_NETWORK, WIREGUARD_SERVER, System
from wgtools import clear_peers, set as wg_set

from termgr.config import CONFIG
from termgr.types import IPAddress, IPNetwork


__all__ = ['get_wireguard_config', 'update_peers']


WG = '/usr/local/bin/sudowg'


class Route(NamedTuple):
    """Represents a route."""

    destination: IPNetwork
    gateway: IPAddress
    gateway_onlink: bool

    @classmethod
    def from_string(cls, string: str):
        """Creates the route from a string representation."""
        destination, gateway = map(str.strip, string.split('via'))
        return cls(ip_network(destination), ip_address(gateway), True)

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {
            'destination': str(self.destination),
            'gateway': str(self.gateway),
            'gateway_onlink': self.gateway_onlink
        }


def get_systems() -> ModelSelect:
    """Yields WireGuard enabled systems."""

    condition = ~(System.pubkey >> None)
    condition &= ~(System.ipv6address >> None)
    return System.select(cascade=True).where(condition)


def get_configured_routes() -> Iterator[Route]:
    """Yields the configured routes."""

    for route in CONFIG['WireGuard']['routes'].split(','):
        yield Route.from_string(route.strip())


def get_client_routes() -> Iterator[Route]:
    """Yields configured routes."""

    yield Route(WIREGUARD_NETWORK, WIREGUARD_SERVER, True)
    yield from get_configured_routes()


def get_wireguard_config(system: System) -> dict:
    """Returns a JSON-ish WireGuard configuration
    for the specified system.
    """

    return {
        'ipaddress': str(system.ipv6address) + '/128',
        'server': str(WIREGUARD_SERVER),
        'peers': [
            {
                'pubkey': CONFIG.get('WireGuard', 'pubkey'),
                'psk': CONFIG.get('WireGuard', 'psk'),
                'endpoint': CONFIG.get('WireGuard', 'endpoint'),
                'routes': [route.to_json() for route in get_client_routes()],
                'persistent_keepalive': CONFIG.getint(
                    'WireGuard', 'persistent_keepalive')
            }
        ]
    }


def get_allowed_ips(system: System) -> Iterator[str]:
    """Yields allowed IP addresses."""

    yield str(system.ipv6address) + '/128'

    for route in get_configured_routes():
        yield str(route.destination)


def system_to_peer(system: System, *, psk: Optional[str] = None) -> dict:
    """Converts a system into a peer dict."""

    peer = {'allowed-ips': list(get_allowed_ips(system))}

    if psk:
        peer['preshared-key'] = psk

    return peer


def get_peers(psk: Optional[str] = None) -> dict:
    """Returns the peers dict."""

    peers = {}

    for system in get_systems():
        peers[system.pubkey] = system_to_peer(system, psk=psk)

    return peers


def _add_peers(psk: Optional[str] = None):
    """Adds all terminal peers with the respective psk."""

    wg_set(CONFIG.get('WireGuard', 'devname'), peers=get_peers(psk=psk),
           _wg=WG)


def add_peers():
    """Adds all terminal network peers."""

    if psk := CONFIG.get('WireGuard', 'psk'):
        with NamedTemporaryFile('w+') as tmp:
            tmp.write(psk)
            tmp.flush()
            return _add_peers(psk=tmp.name)

    return _add_peers()


def update_peers():
    """Adds a peer to the terminals network."""

    clear_peers(CONFIG.get('WireGuard', 'devname'), _wg=WG)
    add_peers()
