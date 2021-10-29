"""Run post-transaction hooks."""

from subprocess import run

from termgr.wireguard import update_peers


__all__ = ['reload']


def reload(*hooks: str, wireguard: bool = False) -> None:
    """Reloads the WireGuard peers and DNS services."""

    hooks_cmd = ['/usr/bin/sudo', '/usr/local/bin/hwadm', 'run-hooks']

    if hooks:
        hooks_cmd += ['-H', *hooks]

    run(hooks_cmd, check=True)

    if wireguard:
        update_peers()
