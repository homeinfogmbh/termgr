"""Terminal administration."""

from hipster.sync import Synchronizer
from wsgilib import JSON

from termgr.ctrl import TerminalsController
from termgr.wsgi.common import DATA, authenticated, authorized

__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
SSH_TIMEOUT_KEYWORDS = (b'Timeout', b'not responding.')
CONTROLLER = TerminalsController()
KEY_FILE = '/home/termgr/.ssh/digsig'


@authenticated
@authorized(administer=True)
def deploy(terminal):
    """Deploys the respective terminal."""

    try:
        DATA.json['undeploy']
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

    try:
        DATA.json['disable']
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
    elif CONTROLLER.pacman(terminal):
        return ('Package manager is currently running.', 503)

    response = CONTROLLER.reboot(terminal)

    if response:
        return 'Rebooted terminal.'
    elif response.exit_code == 255:     # Timeout.
        if all(keyword in response.stderr for keyword in SSH_TIMEOUT_KEYWORDS):
            return ('Probably rebooted terminal.', 202)

    return ('Failed to reboot terminal.', 500)


@authenticated
@authorized(administer=True)
def sync(terminal):
    """Synchronizes the respective terminal."""

    with Synchronizer(keyfile=KEY_FILE) as synchronizer:
        result = synchronizer.sync(terminal)

    if result:
        return 'Terminal synchronizeed.'

    return JSON([str(collector) for collector in result], status=500)


ROUTES = (
    ('POST', '/administer/deploy', deploy, 'manage_deployment'),
    ('POST', '/administer/application', application, 'manage_application'),
    ('POST', '/administer/reboot', reboot, 'reboot_terminal'),
    ('POST', '/administer/sync', sync, 'sync_terminal'))
