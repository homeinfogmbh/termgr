"""Authorization checks."""

from termgr.orm import ACL, DefaultACL


__all__ = ['PermissionsError', 'permissions', 'permit', 'authorize']


class PermissionsError(Exception):
    """Indicates error during permission handling."""

    pass


def permissions(account, terminal):
    """Returns permissions on terminal."""

    try:
        # Per-terminal ACLs override default ACLs.
        return ACL.get((ACL.account == account) & (ACL.terminal == terminal))
    except ACL.DoesNotExist:
        try:
            return DefaultACL.get(
                (DefaultACL.account == account)
                & (DefaultACL.customer == terminal.customer)
                & (DefaultACL.class_ == terminal.class_))
        except DefaultACL.DoesNotExist:
            return None


def permit(account, terminal, *, read=None, administer=None, setup=None):
    """Set permissions."""

    if account.root:
        raise PermissionsError('Cannot set permissions for root accounts.')

    try:
        DefaultACL.get(
            (DefaultACL.account == account)
            & (DefaultACL.customer == terminal.customer)
            & (DefaultACL.class_ == terminal.class_))
    except DefaultACL.DoesNotExist:
        acl = ACL.add(
            account, terminal, read=read, administer=administer, setup=setup)
        acl.commit()


def authorize(account, terminal, *, read=None, administer=None, setup=None):
    """Validate permissions. None means "don't care"!"""

    if all(permission is None for permission in (read, administer, setup)):
        raise PermissionsError('No permissions selected.')

    if not account.can_login:
        return False

    if account.root:
        return True

    # Per-terminal ACLs override default ACLs.
    if ACL.authorize(account, terminal, read=read, administer=administer,
                     setup=setup):
        return True

    return DefaultACL.authorize(
        account, terminal.customer, terminal.class_, read=read,
        administer=administer, setup=setup)
