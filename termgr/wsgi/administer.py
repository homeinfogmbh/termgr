"""Terminal administration."""

from functools import partial

from flask import Response, request

from hipster.orm import Queue
from his import ACCOUNT, authenticated, authorized
from hwdb import SystemOffline, Deployment, System

from termgr.notify import notify
from termgr.orm import DeploymentHistory
from termgr.wsgi.common import admin, deploy


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@deploy
def deploy_(system: System, new_deployment: Deployment) -> Response:
    """Deploys the respective system."""

    exclusive = request.json.get('exclusive', False)
    fitted = request.json.get('exclusive', False)

    for system_, old_deployment in system.deploy(
            new_deployment, exclusive=exclusive, fitted=fitted):
        DeploymentHistory.add(ACCOUNT, system_, old_deployment)

    notify()
    return 'System has been deployed.'


@authenticated
@authorized('termgr')
@admin
def fit(system: System) -> Response:
    """Marks a system as fitted."""

    system.fitted = fitted = request.json.get('fitted', False)
    system.save()
    text = 'fitted' if fitted else 'unfitted'
    return f'System has been {text}.'


@authenticated
@authorized('termgr')
@admin
def toggle_application(system: System) -> Response:
    """Activates and deactivates the digital signage application
    on the system and marks the system as fitted / non-fitted.
    """

    state = request.json.get('state', False)
    function = partial(system.application, state)
    system.fitted = state

    try:
        response = function()
    except SystemOffline:
        return ('System is offline.', 400)

    system.save()
    return (response.text, response.status_code)


@authenticated
@authorized('termgr')
@admin
def reboot(system: System) -> Response:
    """Reboots the respective system."""

    try:
        response = system.reboot()
    except SystemOffline:
        return ('System is offline.', 400)

    if response is None:
        return 'Probably rebooted system.'

    return (response.text, response.status_code)


@authenticated
@authorized('termgr')
@admin
def sync(system: System) -> Response:
    """Synchronizes the respective system."""

    Queue.enqueue(system)
    return ('Synchronization queued.', 202)


@authenticated
@authorized('termgr')
@admin
def beep(system: System) -> Response:
    """Identifies the respective system by beep test."""

    try:
        response = system.beep()
    except SystemOffline:
        return ('System is offline.', 400)

    return (response.text, response.status_code)


ROUTES = (
    ('POST', '/administer/deploy', deploy_),
    ('POST', '/administer/fit', fit),
    ('POST', '/administer/application', toggle_application),
    ('POST', '/administer/reboot', reboot),
    ('POST', '/administer/sync', sync),
    ('POST', '/administer/beep', beep)
)
