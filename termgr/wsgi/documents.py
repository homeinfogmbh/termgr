"""Document download."""

from pathlib import Path
from typing import Union

from his import authenticated, authorized
from wsgilib import Binary, JSONMessage


__all__ = ['ROUTES']


BASEDIR = Path('/usr/local/share/sysmon2')
HIDSL_ISO = 'HIDSL-*-x86_64.iso'
HIDSL_ARM_IMAGE = 'HIDSL-arm-raspi4-*.tar.lzop'
MANUAL = BASEDIR / 'Installationsanleitung_DDB.pdf'


@authenticated
@authorized('termgr')
def get_hidsl_iso() -> Union[Binary, JSONMessage]:
    """Returns the latest HIDSL ISO."""

    for path in sorted(BASEDIR.glob(HIDSL_ISO), reverse=True):
        with path.open('rb') as file:
            return Binary(file.read())

    return JSONMessage('File not found.', status=404)


@authenticated
@authorized('termgr')
def get_hidsl_arm_image() -> Union[Binary, JSONMessage]:
    """Returns the latest HIDSL ARM image."""

    for path in sorted(BASEDIR.glob(HIDSL_ARM_IMAGE), reverse=True):
        with path.open('rb') as file:
            return Binary(file.read())

    return JSONMessage('File not found.', status=404)


@authenticated
@authorized('termgr')
def get_ddb_manual() -> Binary:
    """Returns the DDB manual."""

    with MANUAL.open('rb') as file:
        return Binary(file.read())


ROUTES = [
    ('GET', '/documents/hidsl-iso', get_hidsl_iso),
    ('GET', '/documents/hidsl-arm-image', get_hidsl_arm_image),
    ('GET', '/documents/ddb-manual', get_ddb_manual)
]
