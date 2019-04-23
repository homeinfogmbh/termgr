"""Terminal administration."""

from logging import getLogger

from flask import request

from hipster.ctrl import SyncController
from hipster.sync import Synchronizer
from his import authenticated
from mdb import Address
from terminallib import Connection, Type, Deployment, System
from wsgilib import JSON

from termgr.ctrl import closed_by_remote_host
from termgr.ctrl import SystemController
from termgr.ctrl import SystemsController
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
        if CONTROLLER.enable_application(system):
            return 'Digital signage application enabled.'

        return ('Could not enable digital signage application.', 500)

    if CONTROLLER.disable_application(system):
        return 'Digital signage application disabled.'

    return ('Could not disable digital signage application.', 500)


@authenticated
@admin
def reboot_system(system):
    """Reboots the respective system."""

    administration = CONTROLLER.check_login(system)

    if administration:
        return (str(administration), 503)
        return ('Admin account is currently logged in.', 503)

    if CONTROLLER.pacman_running:
        return ('Package manager is currently running.', 503)

    response = CONTROLLER.reboot(system)

    if response:
        return 'Rebooted system.'

    if response.exit_code == 255 and closed_by_remote_host(response):
        return ('Probably rebooted system.', 202)

    LOGGER.warning(
        'Unknown SSH error: %s (%i).', response.stderr.decode(),
        response.exit_code)
    return ('Failed to reboot system.', 500)


@authenticated
@admin
def sync_system(system):
    """Synchronizes the respective system."""

    with Synchronizer(keyfile=DIGSIG_KEY_FILE) as synchronizer:
        result = synchronizer.sync(system)

    if result:
        ctrl = SyncController(system, keyfile=DIGSIG_KEY_FILE)
        ctrl.restart()
        return 'Terminal synchronized.'

    return JSON([str(collector) for collector in result], status=500)


@authenticated
@admin
def beep_system(system):
    """Identifies the respective system by beep test."""

    if SystemController(system).identify():
        return 'Display should have beeped.'

    return ('Could not get display to beep.', 500)


ROUTES = (
    ('POST', '/administer/deploy', deploy_system),
    ('POST', '/administer/application', toggle_application),
    ('POST', '/administer/reboot', reboot_system),
    ('POST', '/administer/sync', sync_system),
    ('POST', '/administer/beep', beep_system)
)
