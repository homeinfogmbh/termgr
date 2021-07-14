"""Miscellaneous endpoints."""

from flask import Response, request

from his import ACCOUNT, authenticated, authorized, require_json
from hwdb import SystemOffline, OpenVPN, System
from termacls import can_administer_system
from wsgilib import Binary, JSON, JSONMessage

from termgr.wsgi.common import admin


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@admin
def screenshot(system: System) -> Response:
    """Identifies the respective system by beep test."""

    try:
        response = system.screenshot()
    except SystemOffline:
        return ('System is offline.', 400)

    if response.status_code == 200:
        return Binary(response.content)

    return ('Could not get screenshot.', 500)


@authenticated
@authorized('termgr')
@require_json(dict)
def idmap() -> Response:
    """Maps old to new IDs."""

    tid = request.json.get('tid')

    if tid is None:
        return JSONMessage('No TID specified.', status=400)

    cid = request.json.get('cid')

    if cid is None:
        return JSONMessage('No CID specified.', status=400)

    condition = OpenVPN.key == f'{tid.strip()}.{cid.strip()}'

    try:
        system = System.select(cascade=True).where(condition).get()
    except System.DoesNotExist:
        return JSONMessage('No such system.', status=404)

    if can_administer_system(ACCOUNT, system):
        return JSON({'system': system.id})

    return JSONMessage('No such system.', status=404)


ROUTES = [
    ('GET', '/screenshot/<int:system>', screenshot),
    ('POST', '/idmap', idmap)
]
