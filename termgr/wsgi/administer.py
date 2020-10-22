"""Terminal administration."""

from functools import partial

from flask import request

from hipster.orm import Queue
from his import ACCOUNT, authenticated, authorized
from hwdb import SystemOffline

from termgr.notify import notify
from termgr.orm import Deployments
from termgr.wsgi.common import admin, deploy


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@deploy
def deploy_system(system, deployment):
    """Deploys the respective system."""

    exclusive = request.json.get('exclusive', False)
    fitted = request.json.get('exclusive', False)
    system.deploy(deployment, exclusive=exclusive, fitted=fitted)
    Deployments.add(ACCOUNT, system, deployment)
    notify()
    return 'System has been deployed.'


@authenticated
@authorized('termgr')
@admin
def fit_system(system):
    """Marks a system as fitted."""

    system.fitted = fitted = request.json.get('fitted', False)
    system.save()
    text = 'fitted' if fitted else 'unfitted'
    return f'System has been {text}.'


@authenticated
@authorized('termgr')
@admin
def toggle_application(system):
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
def reboot_system(system):
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
def sync_system(system):
    """Synchronizes the respective system."""

    Queue.enqueue(system)
    return ('Synchronization queued.', 202)


@authenticated
@authorized('termgr')
@admin
def beep_system(system):
    """Identifies the respective system by beep test."""

    try:
        response = system.beep()
    except SystemOffline:
        return ('System is offline.', 400)

    return (response.text, response.status_code)


ROUTES = (
    ('POST', '/administer/deploy', deploy_system),
    ('POST', '/administer/fit', fit_system),
    ('POST', '/administer/application', toggle_application),
    ('POST', '/administer/reboot', reboot_system),
    ('POST', '/administer/sync', sync_system),
    ('POST', '/administer/beep', beep_system)
)
