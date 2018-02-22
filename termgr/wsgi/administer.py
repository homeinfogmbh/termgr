"""Terminal administration."""

from flask import request

from wsgilib import JSON, Error

from termgr.ctrl import TerminalsController
from termgr.wsgi.common import DATA, authenticated, authorized

__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'
CONTROLLER = TerminalsController()


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

    response = CONTROLLER.reboot(terminal)

    if response:
        return ('Rebooted terminal: {}/{}.'.format(
            response, response.exit_code), 200)

    return ('Probably rebooted terminal.', 202)


ROUTES = (
    ('POST', '/administer/deploy', deploy, 'deploy_terminal'),
    ('POST', '/administer/application', application, 'activate_application'),
    ('POST', '/administer/reboot', reboot, 'reboot_terminal'))
