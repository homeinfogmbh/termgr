"""Manage terminal address control lists."""

from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, getLogger
from pathlib import Path

from his import Account
from mdb import Customer
from syslib import script
from terminallib import System

from termgr.config import LOG_FORMAT
from termgr.orm import CustomerAdministrator, SystemAdministrator
from termgr.permissions import grant_system
from termgr.permissions import revoke_system
from termgr.permissions import grant_customer
from termgr.permissions import revoke_customer


__all__ = ['main']


LOGGER = getLogger(Path(__file__).name)


def get_account(name):
    """Returns the respective account."""

    try:
        return Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise ValueError(f'No such account: "{name}".')


def get_customer(cid):
    """Returns the respective system."""

    try:
        return Customer[int(cid)]
    except Customer.DoesNotExist:
        raise ValueError(f'No such customer: "{cid}".')


def get_system(ident):
    """Returns the respective system."""

    try:
        return System[int(ident)]
    except System.DoesNotExist:
        raise ValueError(f'No such system: "{ident}')


def get_args():
    """"Returns the CLI arguments."""

    parser = ArgumentParser(description='Terminal permissions manager.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging')
    subparsers = parser.add_subparsers(dest='mode')
    list_parser = subparsers.add_parser('list', help='list permissions')
    list_parser.add_argument(
        'account', nargs='*', type=get_account, metavar='account',
        help="the administrator's HIS account")
    list_parser.add_argument(
        '-c', '--customers', action='store_true',
        help='list customer related permissions')
    list_parser.add_argument(
        '-s', '--systems', action='store_true',
        help='list system related permissions')
    grant_parser = subparsers.add_parser('grant', help='grant permissions')
    grant_parser.add_argument(
        'account', nargs='+', type=get_account, metavar='account',
        help="the administrator's HIS account")
    grant_parser.add_argument(
        '-c', '--customer', nargs='*', type=get_customer, metavar='customer',
        help='grant permissions to deploy for these customers')
    grant_parser.add_argument(
        '-s', '--system', nargs='*', type=get_system, metavar='system',
        help='grant permissions to administer these system')
    revoke_parser = subparsers.add_parser('revoke', help='revoke permissions')
    revoke_parser.add_argument(
        'account', nargs='+', type=get_account, metavar='account',
        help="the administrator's HIS account")
    revoke_parser.add_argument(
        '-c', '--customer', nargs='*', type=get_customer, metavar='customer',
        help='revoke permissions to deploy for these customers')
    revoke_parser.add_argument(
        '-s', '--system', nargs='*', type=get_system, metavar='system',
        help='revoke permissions to administer these system')
    revoke_parser.add_argument(
        '--all', action='store_true', help='revokes all permissions')
    return parser.parse_args()


def list_(args):
    """Lists permissions."""

    accounts = args.account or list(Account)

    if args.customers:
        for customer_admin in CustomerAdministrator.select().where(
                CustomerAdministrator.account << accounts):
            print(f'{customer_admin.account.name}:',
                  customer_admin.customer_id)

    if args.systems:
        for system_admin in SystemAdministrator.select().where(
                SystemAdministrator.account << accounts):
            print(f'{system_admin.account.name}:',
                  system_admin.system_id)


def grant(args):
    """Grants permissions."""

    for account in args.account:
        if args.customer:
            for customer in args.customer:
                LOGGER.debug(
                    'Granting %s permissions on %i.', account, customer.id)
                grant_customer(account, customer)

        if args.system:
            for system in args.system:
                LOGGER.debug(
                    'Granting %s permissions on #%i.', account, system.id)
                grant_system(account, system)


def revoke(args):
    """Revokes permissions."""

    if args.all:
        for customer_admin in CustomerAdministrator.select().where(
                CustomerAdministrator.account << args.account):
            customer_admin.delete_instance()

        for system_admin in SystemAdministrator.select().where(
                SystemAdministrator.account << args.account):
            system_admin.delte_intance()
    else:
        for account in args.account:
            if args.customer:
                for customer in args.customer:
                    LOGGER.debug(
                        'Revoking permissions of %s on %i.', account,
                        customer.id)
                    revoke_customer(account, customer)

            if args.system:
                for system in args.system:
                    LOGGER.debug(
                        'Revoking permissions of %s on #%i.', account,
                        system.id)
                    revoke_system(account, system)


@script
def main():
    """Runs the ACL client."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)

    if args.mode == 'list':
        list_(args)
    elif args.mode == 'grant':
        grant(args)
    elif args.mode == 'revoke':
        revoke(args)
