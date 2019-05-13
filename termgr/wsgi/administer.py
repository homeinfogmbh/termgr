"""Terminal administration."""

from logging import getLogger
from subprocess import CalledProcessError

from flask import request

from hipster.sync import sync
from his import authenticated
from mdb import Address
from terminallib import SystemOffline, Connection, Type, Deployment, System

from termgr.ctrl import SystemController, SystemsController
from termgr.wsgi.common import get_address, admin, deploy

__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
CONTROLLER = SystemsController()
DIGSIG_KEY_FILE = '/home/termgr/.ssh/digsig'
REDEPLOY_TEMP = 'System has been deployed and system #{} has been undeployed.'
LOGGER = getLogger(__file__)


@authenticated
@deploy
def deploy_system(system, customer):
    """Deploys the respective system."""

    address = get_address()
    address = Address.add_by_address(address)
    address.save()

    try:
        typ = Type(request.json['type'])
    except KeyError:
        return ('No type specified.', 400)
    except ValueError:
        return ('Invalid type specified.', 400)

    try:
        connection = Connection(request.json['connection'])
    except KeyError:
        return ('No connection specified.', 400)
    except ValueError:
        return ('Invalid connection specified.', 400)

    select = (
        (Deployment.address == address)
        & (Deployment.customer == customer)
        & (Deployment.type == typ)
        & (Deployment.connection == connection))
    weather = request.json.get('weather')

    if weather is None:
        select &= Deployment.weather >> None
    else:
        select &= Deployment.weather == weather

    annotation = request.json.get('annotation')

    if annotation is None:
        select &= Deployment.annotation >> None
    else:
        select &= Deployment.annotation == annotation

    try:
        deployment = Deployment.get(select)
    except Deployment.DoesNotExist:
        deployment = Deployment(
            customer=customer,
            address=address,
            type=typ,
            connection=connection,
            weather=weather,
            annotation=annotation)
        deployment.save()

    try:
        current_system = System.get(System.deployment == deployment)
    except System.DoesNotExist:
        current_system = None
    else:
        current_system.relocate(None)

    system.relocate(deployment)

    if current_system is None:
        return 'System has been deployed.'

    return REDEPLOY_TEMP.format(current_system.id)


@authenticated
@admin
def toggle_application(system):
    """Activates and deactivates the
    digital signage application on the system.
    """

    try:
        request.json['disable']
    except KeyError:
        mode = 'enable'
        function = CONTROLLER.enable_application
    else:
        mode = 'disable'
        function = CONTROLLER.disable_application

    try:
        function(system)
    except SystemOffline:
        return ('System is offline.', 400)
    except CalledProcessError:
        return (f'Could not {mode} digital signage application.', 500)

    return f'Digital signage application {mode}d.'


@authenticated
@admin
def reboot_system(system):
    """Reboots the respective system."""

    if CONTROLLER.check_login(system):
        return ('Admin account is currently logged in.', 503)

    if CONTROLLER.check_pacman(system):
        return ('Package manager is currently running.', 503)

    try:
        CONTROLLER.reboot(system)
    except SystemOffline:
        return ('System is offline.', 400)
    except CalledProcessError:
        return ('Failed to reboot system.', 500)

    return 'Probably rebooted system.'


@authenticated
@admin
def sync_system(system):
    """Synchronizes the respective system."""

    if sync(system):
        return 'Terminal synchronized.'

    return ('Could not synchronize system.', 500)


@authenticated
@admin
def beep_system(system):
    """Identifies the respective system by beep test."""

    try:
        SystemController(system).identify()
    except SystemOffline:
        return ('System is offline.', 400)
    except CalledProcessError:
        return ('Could not get display to beep.', 500)

    return 'Display should have beeped.'


ROUTES = (
    ('POST', '/administer/deploy', deploy_system),
    ('POST', '/administer/application', toggle_application),
    ('POST', '/administer/reboot', reboot_system),
    ('POST', '/administer/sync', sync_system),
    ('POST', '/administer/beep', beep_system)
)
