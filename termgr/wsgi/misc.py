"""Miscellaneous endpoints."""

from flask import Response, request

from his import authenticated, authorized, require_json
from hwdb import SystemOffline, OpenVPN, System
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

    key = f'{tid.strip()}.{cid.strip()}'

    try:
        system = System.select().join(OpenVPN).where(OpenVPN.key == key).get()
    except System.DoesNotExist:
        return JSONMessage('No such system.', status=404)

    return JSON({'system': system.id})


ROUTES = [
    ('GET', '/screenshot/<int:system>', screenshot),
    ('POST', '/idmap', idmap)
]
