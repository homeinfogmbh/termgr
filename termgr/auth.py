"""Authorization checks."""

from termgr.orm import SystemAdministrator, CustomerAdministrator


__all__ = ['chkadmin', 'chksetup', 'chkdeploy']


def chkadmin(account, system):
    """Checks whether the respective stakeholder may administer the system."""

    if not account.can_login:
        return False

    if account.root:
        return True

    try:
        SystemAdministrator.get(
            (SystemAdministrator.system == system)
            & (SystemAdministrator.account == account))
    except SystemAdministrator.DoesNotExist:
        return False

    return True


def chksetup(account, system):
    """Checks whether the respective customer may setup the system."""

    if not account.can_login:
        return False

    if account.root:
        return True

    if system.manufacturer is not None:
        return account.customer == system.manufacturer

    return False


def chkdeploy(account, system, customer):
    """Checks whether the given account may deploy
    systems for the respective customer.
    """

    if account is None or customer is None:
        return False

    # Check whether the account may deploy for the target customer.
    try:
        CustomerAdministrator.get(
            (CustomerAdministrator.customer == customer)
            & (CustomerAdministrator.account == account))
    except CustomerAdministrator.DoesNotExist:
        return False

    deployment = system.deployment

    # Check whether the account may deploy for the current customer.
    if deployment is None:
        return True

    try:
        CustomerAdministrator.get(
            (CustomerAdministrator.customer == deployment.customer)
            & (CustomerAdministrator.account == account))
    except CustomerAdministrator.DoesNotExist:
        return False

    return True
