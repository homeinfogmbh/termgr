"""Wireguard configuration."""

from ipaddress import ip_address, ip_network
from tempfile import NamedTemporaryFile
from typing import Iterable, Iterator, NamedTuple, Optional

from peewee import ModelSelect

from hwdb import WIREGUARD_NETWORK, WIREGUARD_SERVER, System
from wgtools import set as wg_set, show

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


def get_current_peers() -> set[str]:
    """Lists the current peers."""

    return set(show(CONFIG.get('WireGuard', 'devname'), _wg=WG).keys())


def get_active_peers(systems: Iterable[System]) -> dict:
    """Returns the active peers dict."""

    return {
        system.pubkey: {'allowed-ips': list(get_allowed_ips(system))}
        for system in systems
    }


def get_systems() -> ModelSelect:
    """Yields WireGuard enabled systems."""

    return System.select(cascade=True).where(
        (~(System.pubkey >> None))
        & (~(System.ipv6address >> None))
    )


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


def set_psk(peers: dict[str, dict], psk: Optional[str]) -> dict[str, dict]:
    """Sets the pre-shared key to the peers."""

    if not psk:
        return peers

    return {
        key: {**value, 'preshared-key': psk} for key, value in peers.items()
        if not value.get('remove')
    }


def set_peers(peers: dict[str, dict], psk: Optional[str] = None) -> None:
    """Adds all terminal peers with the respective psk."""

    wg_set(CONFIG.get('WireGuard', 'devname'), peers=set_psk(peers, psk),
           _wg=WG)


def add_peers(peers: dict[str, dict]) -> None:
    """Adds all terminal network peers."""

    if psk := CONFIG.get('WireGuard', 'psk'):
        with NamedTemporaryFile('w+') as tmp:
            tmp.write(psk)
            tmp.flush()
            return set_peers(peers, psk=tmp.name)

    return set_peers(peers)


def update_peers() -> None:
    """Adds a peer to the terminals network."""

    current_peers = get_current_peers()
    active_peers = get_active_peers(get_systems())
    delete_peers = {
        key: {'remove': True} for key in current_peers
        if key not in active_peers
    }
    new_peers = {
        key: value for key, value in active_peers.items()
        if key not in current_peers
    }
    return add_peers({**new_peers, **delete_peers})
