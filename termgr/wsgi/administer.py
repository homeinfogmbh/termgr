"""Terminal administration."""

from typing import Optional

from flask import request

from hipster.orm import Queue
from his import ACCOUNT, authenticated, authorized
from hwdb import SystemOffline, Deployment, System
from mdb import Address
from wsgilib import JSON

from termgr.notify import notify
from termgr.orm import DeploymentHistory
from termgr.wsgi.common import depadmin, sysadmin, deploy


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@deploy
def deploy_(system: System, deployment: Optional[Deployment]) -> JSON:
    """Deploys the respective system."""

    exclusive = request.json.get('exclusive', False)
    fitted = request.json.get('fitted', False)

    for sys, old, _ in system.deploy(
            deployment, exclusive=exclusive, fitted=fitted):
        DeploymentHistory.add(ACCOUNT.id, sys, old)

    notify()
    return JSON({
        'system': system.id,
        'deployment': None if deployment is None else deployment.id,
        'address': None if deployment is None else str(deployment.address),
        'exclusive': exclusive,
        'fitted': fitted
    })


@authenticated
@authorized('termgr')
@sysadmin
def fit(system: System) -> str:
    """Marks a system as fitted."""

    system.fitted = fitted = request.json.get('fitted', False)
    system.save()
    text = 'fitted' if fitted else 'unfitted'
    return f'System has been {text}.'


@authenticated
@authorized('termgr')
@sysadmin
def toggle_application(system: System) -> tuple[str, int]:
    """Activates and deactivates the digital signage application."""

    try:
        response = system.application(request.json.get('state', False))
    except SystemOffline:
        return 'System is offline.', 400

    system.save()
    return response.text, response.status_code


@authenticated
@authorized('termgr')
@sysadmin
def reboot(system: System) -> tuple[str, int]:
    """Reboots the respective system."""

    try:
        response = system.reboot()
    except SystemOffline:
        return 'System is offline.', 400

    if response is None:
        return 'Probably rebooted system.', 200

    return response.text, response.status_code


@authenticated
@authorized('termgr')
@sysadmin
def sync(system: System) -> tuple[str, int]:
    """Synchronizes the respective system."""

    Queue.enqueue(system)
    return 'Synchronization queued.', 202


@authenticated
@authorized('termgr')
@sysadmin
def beep(system: System) -> tuple[str, int]:
    """Identifies the respective system by beep test."""

    try:
        response = system.beep()
    except SystemOffline:
        return 'System is offline.', 400

    return response.text, response.status_code


@authenticated
@authorized('termgr')
@depadmin
def set_lpt_address(deployment: Deployment) -> tuple[str, int]:
    """Set the LPT address of the given deployment."""

    try:
        address = Address.add(*request.json)
    except TypeError:
        return 'Invalid address provided.', 400

    if address.id is None:
        address.save()

    deployment.lpt_address = address
    deployment.save()
    return 'LPT address updated.', 200


@authenticated
@authorized('termgr')
@depadmin
def get_deployment_history(deployment: Deployment) -> tuple[str, int]:
    """Return the deployment history of the given deployment."""

    return 'Not implemented.', 400


ROUTES = (
    ('POST', '/administer/deploy', deploy_),
    ('POST', '/administer/fit', fit),
    ('POST', '/administer/application', toggle_application),
    ('POST', '/administer/reboot', reboot),
    ('POST', '/administer/sync', sync),
    ('POST', '/administer/beep', beep),
    ('POST', '/administer/lpt-address/<int:deployment>', beep)
)
