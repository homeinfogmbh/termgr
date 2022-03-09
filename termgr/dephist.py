"""CLI tool to list deployment histories."""

from argparse import ArgumentParser, Namespace
from logging import INFO, basicConfig, getLogger
from sys import stdout

from peewee import Expression, Field

from his import account
from hwdb import deployment, system

from termgr.config import LOG_FORMAT
from termgr.orm import DeploymentHistory


__all__ = ['main']


LOGGER = getLogger('dephist')


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser('Deployment history utility.')
    parser.add_argument(
        '-S', '--system', type=system, metavar='system',
        help='lists the deployment history of the given system'
    )
    parser.add_argument(
        '-D', '--deployment', type=deployment, metavar='deployment',
        help='lists the deployment history of the given deployment'
    )
    parser.add_argument(
        '-a', '--accounts', type=account, nargs='+', metavar='account',
        help='filters for deployments performed by the given accounts'
    )
    parser.add_argument(
        '-d', '--desc', action='store_true', help='sort descending'
    )
    return parser.parse_args()


def get_condition(args: Namespace) -> Expression | bool:
    """Returns the select condition."""

    if args.deployment:
        condition = DeploymentHistory.new_deployment == args.deployment
    else:
        condition = DeploymentHistory.system == args.system

    if args.accounts:
        condition &= DeploymentHistory.account << args.accounts

    return condition


def get_ordering(descending: bool) -> Field:
    """Returns the ordering."""

    if descending:
        return DeploymentHistory.timestamp.desc()

    return DeploymentHistory.timestamp


def main() -> int:
    """Runs the script and returns a return code."""

    args = get_args()
    basicConfig(level=INFO, format=LOG_FORMAT)

    if args.system is None and args.deployment is None:
        LOGGER.error('Must specify either system or deployment.')
        return 1

    condition = get_condition(args)
    order = get_ordering(args.desc)

    if stdout.isatty():
        print('\t'.join(f'\033[1m{field}\033[0m'
              for field in DeploymentHistory.FIELDS))

    for record in DeploymentHistory.select(cascade=True).where(
            condition).order_by(order):
        print(record, flush=True)

    return 0
