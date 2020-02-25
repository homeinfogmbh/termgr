"""Command line interface."""

from argparse import ArgumentParser
from logging import INFO, basicConfig
from os import geteuid
from subprocess import check_call
from sys import exit    # pylint: disable=W0622

from termgr.config import LOG_FORMAT, LOGGER, SYSTEMD_NETWORKD
from termgr.wireguard import update_units


__all__ = ['main']


def get_args():
    """Returns parsed command line arguments."""

    parser = ArgumentParser(description='Terminal manager')
    subparsers = parser.add_subparsers(dest='action')
    subparsers.add_parser('mkwg', help='write WireGuard configuration')
    return parser.parse_args()


def main():
    """Runs the CLI program."""

    args = get_args()
    basicConfig(level=INFO, format=LOG_FORMAT)

    if args.action == 'mkwg':
        if geteuid() != 0:
            LOGGER.error('You need to be root to run this script.')
            exit(1)

        LOGGER.info('Updating WireGuard configuration.')
        update_units()
        LOGGER.info('Restarting %s.', SYSTEMD_NETWORKD)
        check_call(('/bin/systemctl', 'restart', SYSTEMD_NETWORKD))
