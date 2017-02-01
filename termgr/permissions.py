"""Permissions and access control handling"""

__all__ = ['PermissionsParser']


class PermissionsParser():
    """Manages permissions on terminals"""

    def __init__(self, s):
        """Parse permissions string"""
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

        self.read = read
        self.administer = administer
        self.setup = setup

    def __iter__(self):
        """Yields the permissions fields"""
        yield self.read
        yield self.administer
        yield self.setup

    def __getitem__(self, index):
        """Returns the permissions field at index"""
        if index == 0:
            return self.read
        elif index == 1:
            return self.administer
        elif index == 2:
            return self.setup
        elif index == 3:
            raise KeyError('No 3rd permission field')
        else:
            raise KeyError('No {}th permission field'.format(index))
