"""Terminals adminstration."""

from functools import partial
from logging import INFO, basicConfig, getLogger
from os import geteuid
from subprocess import run
from sys import exit    # pylint: disable=W0622

from his import Account
from mdb import Address, Company, Customer
from syslib import evaluate, script
from terminallib import TerminalConfigError
from terminallib import Deployment
from terminallib import OpenVPN
from terminallib import OperatingSystem
from terminallib import System
from terminallib import Type
from terminallib import WireGuard

from termgr.config import LOG_FORMAT
from termgr.notify import notify_todays_deployments


__all__ = ['main']


LOGGER = getLogger(__file__)
TERMGR_USER = 'termgr'
NAGIOSCFG_GEN = '/usr/local/bin/nagioscfg-gen'
BINDCFG_GEN = '/usr/local/bin/bindcfg-gen'
OPENVPNCFG_GEN = '/usr/local/bin/openvpncfg-gen'


def _get_accounts(accounts):
    """Yields the respective users."""

    for account in accounts:
        try:
            yield Account.get(Account.name == account)
        except Account.DoesNotExist:
            LOGGER.warning('No such account: %s.', account)


def _customer_by_name(name):
    """Returns a customer by its name."""

    select = (Company.name == name) | (Company.abbreviation == name)
    customer = Customer.select().join(Company).where(select).get()
    LOGGER.info('Found customer by name: %s.', customer)
    return customer


def _customer_by_id(ident):
    """Returns a customer by its ID."""

    return Customer[ident]


def _get_customer(string):
    """Returns the respecive customer."""

    if string is None:
        return None

    try:
        ident = int(string)
    except ValueError:
        function = partial(_customer_by_name, string)
    else:
        function = partial(_customer_by_id, ident)

    try:
        return function()
    except Customer.DoesNotExist:
        LOGGER.error('No such customer: %i.', string)
        exit(2)


def _get_type(string):
    """Returns the respective type."""

    if string is None:
        return None

    try:
        return Type(string)
    except ValueError:
        LOGGER.error('No such type: %i.', string)
        exit(2)


def _get_system(string):
    """Returns the respective system."""

    try:
        ident = int(string)
    except ValueError:
        LOGGER.error('Invalid system ID: %s.', string)
        exit(1)

    try:
        return System[ident]
    except System.DoesNotExist:
        LOGGER.error('No such system: %i.', ident)
        exit(2)


def update_config():
    """Fix stuff after operations."""

    print('Generating bind9 configuration', end='          ', flush=True)
    bind_ok = run(BINDCFG_GEN)
    evaluate(bind_ok)
    print('Generating OpenVPN host configurations', end='  ', flush=True)
    openvpn_ok = run(OPENVPNCFG_GEN)
    evaluate(openvpn_ok)
    print('Creating Nagios3 configurations', end='         ', flush=True)
    nagios_ok = run((NAGIOSCFG_GEN, '--restart'))
    evaluate(nagios_ok)

    if bind_ok and openvpn_ok and nagios_ok:
        exit(0)

    exit(1)


def add(options):
    """Adds a new system."""

    operating_system = options['--os']

    try:
        operating_system = OperatingSystem(operating_system)
    except ValueError:
        LOGGER.error('No such operating system: %s.', operating_system)
        exit(1)

    manufacturer = _get_customer(options['--manufacturer'])
    serial_number = options['--serial-number']
    model = options['--model']
    vpn_key = options['--key'] or None
    mtu = options['--mtu']

    if mtu is not None:
        try:
            mtu = int(mtu)
        except ValueError:
            LOGGER.error('Invalid MTU: %s.', mtu)
            exit(2)

    if vpn_key is not None:
        LOGGER.warning('Divergent OpenVPN key specified: "%s"!', vpn_key)

    try:
        openvpn = OpenVPN.generate(key=vpn_key, mtu=mtu)
    except TerminalConfigError as tce:
        LOGGER.error(tce)
        exit(3)

    try:
        wireguard = WireGuard.generate()
    except TerminalConfigError as tce:
        LOGGER.error(tce)
        exit(3)

    system = System(
        openvpn=openvpn, wireguard=wireguard, manufacturer=manufacturer,
        operating_system=operating_system, serial_number=serial_number,
        model=model)
    system.save()
    LOGGER.info('Added system: %i', system.id)
    exit(0)


def deploy(options):
    """Deploys a system."""

    system = _get_system(options['<id>'])
    customer = _get_customer(options['<customer>'])
    typ = _get_type(options['<type>'])
    street = options['<street>']
    house_number = options['<house_number>']
    zip_code = options['<zip_code>']
    city = options['<city>']
    address = Address.add_by_address((street, house_number, zip_code, city))
    address.save()
    select = Deployment.address == address

    if customer is not None:
        select &= Deployment.customer == customer

    if typ is not None:
        select &= Deployment.type == typ

    try:
        deployment = Deployment.get(select)
    except Deployment.DoesNotExist:
        deployment = Deployment(customer=customer, type=typ, address=address)
        deployment.save()

    if system.deploy(deployment):
        exit(0)

    exit(1)


def undeploy(options):
    """Removed deployment of terminals."""

    system = _get_system(options['<id>'])

    if system.deploy(None):
        exit(0)

    exit(1)


@script
def main(options):
    """Runs the terminal administration CLI."""

    basicConfig(level=INFO, format=LOG_FORMAT)

    if options['add']:
        add(options)
    elif options['deploy']:
        deploy(options)
    elif options['undeploy']:
        undeploy(options)
    elif options['reload']:
        if geteuid() != 0:
            LOGGER.error('You must be root to update the related services.')
            exit(3)

        update_config()
    elif options['notify']:
        notify_todays_deployments()

    exit(0)
