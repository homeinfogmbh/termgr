"""ORM models for termgr."""

from peewee import Model, PrimaryKeyField, CharField, BooleanField, \
    ForeignKeyField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from homeinfo.crm import Company
from peeweeplus import MySQLDatabase
from terminallib import Terminal

from termgr.config import CONFIG

__all__ = [
    'AuthenticationError',
    'PermissionsError',
    'User',
    'ACL']


_PASSWORD_HASHER = PasswordHasher()


class AuthenticationError(Exception):
    """Indicates an error during authentication process."""

    pass


class PermissionsError(Exception):
    """Indicates error during permission handling."""

    pass


class TermgrModel(Model):
    """Terminal manager basic Model."""

    id = PrimaryKeyField()

    class Meta:
        database = MySQLDatabase(
            CONFIG['db']['db'],
            host=CONFIG['db']['host'],
            user=CONFIG['db']['user'],
            passwd=CONFIG['db']['passwd'],
            closing=True)
        schema = database.database


class User(TermgrModel):
    """A generic abstract user."""

    company = ForeignKeyField(
        Company, db_column='company', on_update='CASCADE', on_delete='CASCADE')
    name = CharField(64)
    pwhash = CharField(255)
    enabled = BooleanField()
    annotation = CharField(255, null=True)
    root = BooleanField(default=False)

    def __str__(self):
        """Returns the user's name."""
        return self.name

    @classmethod
    def authenticate(cls, name, passwd):
        """Authenticate with name and password."""
        if passwd:
            try:
                user = cls.get(cls.name == name)
            except cls.DoesNotExist:
                raise AuthenticationError()

            try:
                _PASSWORD_HASHER.verify(user.pwhash, passwd)
            except VerifyMismatchError:
                raise AuthenticationError()

            if user.enabled:
                return user

        raise AuthenticationError()

    def passwd(self, passwd):
        """Creates a new password hash."""
        self.pwhash = _PASSWORD_HASHER.hash(passwd)

    passwd = property(None, passwd)

    def permissions(self, terminal):
        """Returns permissions on terminal."""
        return ACL.get((ACL.user == self) & (ACL.terminal == terminal))

    def permit(self, terminal, read=None, administer=None, setup=None):
        """Set permissions."""
        if self.root:
            raise PermissionsError('Cannot set permissions for root users.')

        try:
            permissions = self.permissions(terminal)
        except ACL.DoesNotExist:
            permissions = ACL()
            permissions.user = self
            permissions.terminal = terminal

        if read is not None:
            permissions.read = read

        if administer is not None:
            permissions.administer = administer

        if setup is not None:
            permissions.setup = setup

        if permissions.read or permissions.administer or permissions.setup:
            permissions.save()
        else:
            permissions.delete_instance()

    def authorize(self, terminal, read=None, administer=None, setup=None):
        """Validate permissions.
        None means "don't care"!
        """
        if all(permission is None for permission in (read, administer, setup)):
            raise PermissionsError('No permissions selected.')
        elif not self.enabled:
            return False
        elif self.root:
            return True

        if read is None:
            read_expr = True
        else:
            read_expr = ACL.read == read

        if administer is None:
            administer_expr = True
        else:
            administer_expr = ACL.administer == administer

        if setup is None:
            setup_expr = True
        else:
            setup_expr = ACL.setup == setup

        try:
            ACL.get((ACL.user == self) & (ACL.terminal == terminal)
                    & read_expr & administer_expr & setup_expr)
        except ACL.DoesNotExist:
            return False

        return True


class ACL(TermgrModel):
    """Many-to-many mapping in-between administrators
    and terminals with certain permissions.
    """

    user = ForeignKeyField(
        User, db_column='user', on_update='CASCADE', on_delete='CASCADE')
    terminal = ForeignKeyField(
        Terminal, db_column='terminal', on_update='CASCADE',
        on_delete='CASCADE')
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    def __int__(self):
        """Returns the permissions value."""
        return 4 * self.read + 2 * self.administer + self.setup

    def __repr__(self):
        """Returns the permissions as a string."""
        return '{0:#0{1}o}'.format(int(self), 5)

    def __str__(self):
        """Returns the permissions as an alternative string."""
        return ''.join((
            'r' if self.read else '-',
            'a' if self.administer else '-',
            's' if self.setup else '-'))

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)
