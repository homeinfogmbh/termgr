"""Terminal administration."""

from logging import getLogger

from hipster.appctl import ApplicationHandler
from hipster.sync import Synchronizer
from wsgilib import JSON

from termgr.ctrl import closed_by_remote_host, TerminalsController
from termgr.wsgi.common import get_json, authenticated, authorized

__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
CONTROLLER = TerminalsController()
DIGSIG_KEY_FILE = '/home/termgr/.ssh/digsig'
APPCTL = ApplicationHandler(keyfile=DIGSIG_KEY_FILE)
LOGGER = getLogger(__file__)


@authenticated
@authorized(administer=True)
def deploy(terminal):
    """Deploys the respective terminal."""

    json = get_json()

    try:
        json['undeploy']
    except KeyError:
        if terminal.deploy():
            return 'Terminal deployed.'

        return 'Terminal already deployed.'

    if terminal.undeploy():
        return 'Terminal un-deployed.'

    return 'Terminal is not deployed.'


@authenticated
@authorized(administer=True)
def application(terminal):
    """Activates and deactivates terminals."""

    json = get_json()

    try:
        json['disable']
    except KeyError:
        if CONTROLLER.enable_application(terminal):
            return 'Digital signage application enabled.'

        return ('Could not enable digital signage application.', 500)

    if CONTROLLER.disable_application(terminal):
        return 'Digital signage application disabled.'

    return ('Could not disable digital signage application.', 500)


@authenticated
@authorized(administer=True)
def reboot(terminal):
    """Reboots the respective terminal."""

    if CONTROLLER.check_login(terminal):
        return ('Admin user is currently logged in.', 503)

    if CONTROLLER.pacman(terminal):
        return ('Package manager is currently running.', 503)

    response = CONTROLLER.reboot(terminal)

    if response:
        return 'Rebooted terminal.'

    if response.exit_code == 255 and closed_by_remote_host(response):
        return ('Probably rebooted terminal.', 202)

    LOGGER.warning(
        'Unknown SSH error: %s (%i).', response.stderr.decode(),
        response.exit_code)
    return ('Failed to reboot terminal.', 500)


@authenticated
@authorized(administer=True)
def sync(terminal):
    """Synchronizes the respective terminal."""

    with Synchronizer(keyfile=DIGSIG_KEY_FILE) as synchronizer:
        result = synchronizer.sync(terminal)

    if result:
        APPCTL.restart(terminal)
        return 'Terminal synchronizeed.'

    return JSON([str(collector) for collector in result], status=500)


ROUTES = (
    ('POST', '/administer/deploy', deploy, 'manage_deployment'),
    ('POST', '/administer/application', application, 'manage_application'),
    ('POST', '/administer/reboot', reboot, 'reboot_terminal'),
    ('POST', '/administer/sync', sync, 'sync_terminal'))
