"""Terminal administration."""

from flask import request

from wsgilib import JSON

from termgr.ctrl import TerminalController
from termgr.wsgi.common import authenticated, authorized

__all__ = ['ROUTES']


SYSTEMCTL = '/usr/bin/systemctl'
DIGSIG_APP = 'application.service'


@authenticated
@authorized(administer=True)
def deploy(terminal):
    """Deploys the respective terminal."""

    try:
        request.args['undeploy']
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
        request.args['disable']
    except KeyError:
        result = TerminalController(terminal).sudo(
            SYSTEMCTL, 'enable', DIGSIG_APP)

        if result:
            message = 'Digital signage application enabled.'
            status = 200
        else:
            message = 'Could not enable digital signage application.'
            status = 500
    else:
        result = TerminalController(terminal).sudo(
            SYSTEMCTL, 'disable', DIGSIG_APP)

        if result:
            message = 'Digital signage application disabled.'
            status = 200
        else:
            message = 'Could not disable digital signage application.'
            status = 500

    return JSON({'message': message, 'result': result.to_dict()},
                status=status)


@authenticated
@authorized(administer=True)
def reboot(terminal):
    """Reboots the respective terminal."""

    result = TerminalController(terminal).sudo('/usr/bin/reboot')

    if result:
        message = 'Rebooted terminal.'
        status = 200
    else:
        message = 'Probably rebooted terminal.'
        status = 202

    return JSON({'message': message, 'result': result.to_dict()},
                status=status)


ROUTES = (
    ('POST', '/administer/deploy', deploy, 'deploy_terminal'),
    ('POST', '/administer/activate', application, 'activate_application'),
    ('POST', '/administer/reboot', reboot, 'reboot_terminal'))
