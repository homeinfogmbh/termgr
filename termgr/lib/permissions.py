"""Permissions and access control handling"""

__all__ = ['parse']


def parse(s):
    """Parse permissions string

    Returns a tuple:
        (read, administer, setup)
    """
    binary = False

    # Check for binary string
    if len(s) == 3:
        for char in s:
            if char not in ['0', '1']:
                break
        else:
            binary = True
            permissions = s

    if not binary:
        try:
            permissions = int(s)
        except ValueError:
            revoke = None

            read = None
            administer = None
            setup = None

            if s.startswith('+'):
                revoke = False
                permissions = s[1:]
            elif s.startswith('–'):  # [AltGr] + [-]
                revoke = True
                permissions = s[1:]
            else:
                permissions = s
                read = False
                administer = False
                setup = False

            for permission in permissions:
                permission = permission.lower()

                if permission == 'r':
                    read = not revoke
                elif permission == 'a':
                    administer = not revoke
                elif permission == 's':
                    setup = not revoke
                else:
                    raise PermissionError(
                        'Invalid permission: {}'.format(permission))

        else:
            permissions = '{0:0>3}'.format(bin(permissions)[2:])
            binary = True

    if binary:
        read = permissions[0] == '1'
        administer = permissions[1] == '1'
        setup = permissions[2] == '1'

    return (read, administer, setup)
