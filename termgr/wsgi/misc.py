"""Miscellaneous endpoints."""

from flask import Response

from his import authenticated, authorized
from hwdb import SystemOffline, System
from wsgilib import Binary

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


ROUTES = [('GET', '/screenshot/<int:system>', screenshot)]
