"""Authorization checks."""

from his import ACCOUNT

from termgr.orm import SystemAdministrator, CustomerAdministrator


__all__ = ['chkadmin', 'chksetup', 'chkdeploy']


def chkadmin(system):
    """Checks whether the respective stakeholder may administer the system."""

    if not ACCOUNT.can_login:
        return False

    if ACCOUNT.root:
        return True

    try:
        SystemAdministrator.get(
            (SystemAdministrator.system == system)
            & (SystemAdministrator.account == ACCOUNT.id))
    except SystemAdministrator.DoesNotExist:
        return False

    return True


def chksetup(system):
    """Checks whether the respective customer may setup the system."""

    if not ACCOUNT.can_login:
        return False

    if ACCOUNT.root:
        return True

    if system.manufacturer is not None:
        return ACCOUNT.customer == system.manufacturer

    return False


def chkdeploy(system, deployment):
    """Checks whether the given account may deploy
    systems for the respective customer.
    """

    if not chkadmin(system):
        return False

    if ACCOUNT.root:
        return True

    # Check whether the account may deploy for the target customer.
    try:
        CustomerAdministrator.get(
            (CustomerAdministrator.customer == deployment.customer)
            & (CustomerAdministrator.account == ACCOUNT.id))
    except CustomerAdministrator.DoesNotExist:
        return False

    # Check whether the account may deploy for the current customer.
    if system.deployment is None:
        return True

    try:
        CustomerAdministrator.get(
            (CustomerAdministrator.customer == system.deployment.customer)
            & (CustomerAdministrator.account == ACCOUNT.id))
    except CustomerAdministrator.DoesNotExist:
        return False

    return True
