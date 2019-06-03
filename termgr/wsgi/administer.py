"""Terminal administration."""

from logging import getLogger
from subprocess import CalledProcessError

from flask import request

from hipster.orm import Queue
from his import ACCOUNT, authenticated
from terminallib import SystemOffline

from termgr.ctrl import SystemController, SystemsController
from termgr.notify import notify_todays_deployments
from termgr.orm import Deployments
from termgr.wsgi.common import admin, deploy


__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
CONTROLLER = SystemsController()
DIGSIG_KEY_FILE = '/home/termgr/.ssh/digsig'
REDEPLOY_TEMP = 'System has been deployed and system #{} has been undeployed.'
LOGGER = getLogger(__file__)


@authenticated
@deploy
def deploy_system(system, deployment):
    """Deploys the respective system."""

    exclusive = request.json.get('exclusive', False)
    system.deploy(deployment, exclusive=exclusive)
    Deployments.add(ACCOUNT, system, deployment)
    notify_todays_deployments()
    return 'System has been deployed.'


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

    Queue.enqueue(system)
    return ('Synchronization queued.', 202)


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
