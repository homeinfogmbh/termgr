"""Permissions and access control handling"""

from json import dumps
from itertools import chain

from homeinfo.terminals.orm import Terminal

from termgr.orm import Permissions

__all__ = ['PermissionsParser', 'UserPermissions']


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


class UserPermissions():
    """Retrieves, sorts and formats permissions for a respective user"""

    def __init__(self, user):
        """Sets the respective user"""
        self.user = user

    def __repr__(self):
        """Returns an unambiguous representation
        of the user's permissions
        """
        return dumps(self.permission_groups(human_readable=False))

    def __str__(self):
        """Returns a human readable representation
        of the user's permissions
        """
        return dumps(self.permission_groups(human_readable=True), indent=2)

    @property
    def permissions(self):
        """Order permissions of the respective user in a dictionary"""

        permissions = {}

        for permission in Permissions.select().where(
                Permissions.user == self.user):
            cid = permission.terminal.customer.id
            tid = permission.terminal.tid

            try:
                tids = permissions[cid]
            except KeyError:
                permissions[cid] = tids = {}

            try:
                permission_ = tids[tid]
            except KeyError:
                tids[tid] = permission
            else:
                if permission > permission_:
                    tids[tid] = permission

        return permissions

    def permission_groups(self, human_readable=True):
        """Formats the respective permissions dictionary"""
        d = self.permissions
        permission_groups = {}

        # Group by permissions
        for cid in d:
            tids = d[cid]

            for tid in sorted(tids):
                permission = tids[tid]

                if human_readable:
                    perm = str(permission)
                else:
                    perm = repr(permission)

                try:
                    cids_ = permission_groups[perm]
                except KeyError:
                    cids_ = permission_groups[perm] = {}

                try:
                    tid_ranges = cids_[cid]
                except KeyError:
                    tid_ranges = cids_[cid] = []

                # Derive TID ranges like [<start>, <end>]
                for tid_range in tid_ranges:
                    if tid_range[-1] == tid - 1:
                        if len(tid_range) == 1:
                            tid_range.append(tid)
                        else:
                            tid_range[-1] = tid

                        break
                else:
                    tid_ranges.append([tid])

        # Format TID ranges
        for permission in permission_groups:
            cids = permission_groups[permission]

            for cid in cids:
                tid_ranges = cids[cid]

                all_tids = set(
                    terminal.tid for terminal in
                    Terminal.select().where(Terminal.customer == cid))
                my_tids = set(chain(*tid_ranges))

                if all_tids == my_tids:
                    str_ranges = 'all'
                else:
                    str_ranges = []

                    for tid_range in tid_ranges:
                        if len(tid_range) == 2:
                            str_range = '{start}-{end}'.format(
                                start=tid_range[0], end=tid_range[-1])
                        elif len(tid_range) == 1:
                            str_range = str(tid_range[0])
                        else:
                            raise ValueError(
                                'Unexpected TID range: {}'.format(tid_range))

                        str_ranges.append(str_range)

                cids[cid] = str_ranges

        return permission_groups
