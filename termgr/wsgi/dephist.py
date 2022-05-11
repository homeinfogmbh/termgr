"""Deployment history listing."""

from his import authenticated, authorized
from hwdb import System
from wsgilib import JSON

from termgr.orm import DeploymentHistory
from termgr.wsgi.common import sysadmin


__all__ = ['ROUTES']


@authenticated
@authorized('termgr')
@sysadmin
def get_deployment_history(system: System) -> JSON:
    """Return the deployment history of the given deployment."""

    return JSON([
        dephist.to_json(shallow=True)
        for dephist in DeploymentHistory.select(cascade=True).where(
            DeploymentHistory.system == system
        )
    ])


ROUTES = [
    ('GET', '/deployment-history/<int:system>', get_deployment_history)
]
