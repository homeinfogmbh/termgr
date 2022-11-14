"""Terminal administration."""

from typing import Optional

from flask import request
from peewee import OperationalError

from hipster.orm import Queue
from his import ACCOUNT, authenticated, authorized
from hwdb import SystemOffline, ApplicationMode, Deployment, System
from wsgilib import JSON

from termgr.notify import notify
from termgr.orm import DeploymentHistory
from termgr.wsgi.common import depadmin, deploy, get_address, sysadmin


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
def set_application(system: System) -> tuple[str, int]:
    """Set the running digital signage application."""

    mode = request.json.get('mode')

    if mode is not None:
        try:
            mode = ApplicationMode[mode]
        except KeyError:
            return 'Invalid application mode.', 400

    try:
        response = system.application(mode)
    except SystemOffline:
        return 'System is offline.', 400

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

    Queue.enqueue(system, priority=True, force=True)
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
@sysadmin
def set_serial_number(system: System) -> tuple[str, int]:
    """Set the serial number of the given system."""

    try:
        system.serial_number = request.json['serialNumber']
    except KeyError:
        return 'No serial number provided.', 400
    except TypeError:
        return 'Invalid serial number provided.', 400

    try:
        system.save()
    except OperationalError as error:
        return f'Could not set new serial number: {error}', 400

    return 'Serial number updated.', 200


@authenticated
@authorized('termgr')
@depadmin
def set_lpt_address(deployment: Deployment) -> tuple[str, int]:
    """Set the LPT address of the given deployment."""

    try:
        deployment.lpt_address = get_address(request.json)
    except TypeError:
        return 'Invalid address provided.', 400

    deployment.save()
    return 'LPT address updated.', 200


ROUTES = [
    ('POST', '/administer/deploy', deploy_),
    ('POST', '/administer/fit', fit),
    ('POST', '/administer/application', set_application),
    ('POST', '/administer/reboot', reboot),
    ('POST', '/administer/sync', sync),
    ('POST', '/administer/beep', beep),
    ('POST', '/administer/serial-number', set_serial_number),
    ('POST', '/administer/lpt-address/<int:deployment>', set_lpt_address)
]
