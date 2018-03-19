"""ORM models for termgr."""

from peewee import Model, PrimaryKeyField, CharField, BooleanField, \
    ForeignKeyField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from homeinfo.crm import Company, Customer
from peeweeplus import MySQLDatabase
from terminallib import Class, Terminal

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
        """Configures the database and schema."""
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
        Company, column_name='company', on_update='CASCADE',
        on_delete='CASCADE')
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

    def permit(self, terminal, *, read=None, administer=None, setup=None):
        """Set permissions."""
        if self.root:
            raise PermissionsError('Cannot set permissions for root users.')

        acl = ACL.add(
            self, terminal, read=read, administer=administer, setup=setup)
        acl.commit()

    def authorize(self, terminal, *, read=None, administer=None, setup=None):
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
        User, column_name='user', on_update='CASCADE', on_delete='CASCADE')
    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_update='CASCADE',
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

    @classmethod
    def add(cls, user, terminal, *, read=None, administer=None, setup=None):
        """Adds the respective ACL entry."""
        try:
            acl = cls.get((cls.user == user) & (cls.terminal == terminal))
        except cls.DoesNotExist:
            acl = cls()
            acl.user = user
            acl.terminal = terminal

        if read is not None:
            acl.read = read

        if administer is not None:
            acl.administer = administer

        if setup is not None:
            acl.setup = setup

        return acl

    def commit(self):
        """Commits the ACLs."""
        if self.read or self.administer or self.setup:
            return self.save()

        return self.delete_instance()


class DefaultACL(TermgrModel):
    """Represents default ACL settings for users."""

    user = ForeignKeyField(
        User, column_name='user', on_update='CASCADE', on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_update='CASCADE',
        on_delete='CASCADE')
    class_ = ForeignKeyField(
        Class, column_name='class', on_update='CASCADE', on_delete='CASCADE')
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    @classmethod
    def add(cls, user, customer, class_, *, read=False, administer=False,
            setup=False):
        """Adds new default ACLs."""
        try:
            acl = cls.get(
                (cls.user == user) & (cls.customer == customer)
                & (cls.class_ == class_))
        except cls.DoesNotExist:
            acl = cls()
            acl.user = user
            acl.customer = customer
            acl.class_ = class_

        if read is not None:
            acl.read = read

        if administer is not None:
            acl.administer = administer

        if setup is not None:
            acl.setup = setup

        return acl

    @classmethod
    def apply(cls, user=None):
        """Applies the default ACLs to the current terminals."""
        sel_expr = True if user is None else cls.user == user

        for default_acl in cls.select().where(sel_expr):
            for terminal in default_acl.terminals:
                acl = ACL.add(
                    default_acl.user, terminal, read=default_acl.read,
                    administer=default_acl.administer, setup=default_acl.setup)
                acl.commit()

    @property
    def terminals(self):
        """Yields the respective terminals
        associated with the default ACL entry.
        """
        return Terminal.select().where(
            (Terminal.customer == self.customer)
            & (Terminal.class_ == self.class_))

    def commit(self):
        """Commits the ACLs."""
        if self.read or self.administer or self.setup:
            return self.save()

        return self.delete_instance()


class WatchList(TermgrModel):
    """Mapping in-between users, customers and terminal
    classes to notify users about new terminals.
    """

    user = ForeignKeyField(
        User, column_name='user', on_update='CASCADE', on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_update='CASCADE',
        on_delete='CASCADE')
    class_ = ForeignKeyField(
        Class, column_name='class', on_update='CASCADE', on_delete='CASCADE')

    @classmethod
    def add(cls, user, customer, class_):
        """Adds new default ACLs."""
        try:
            return cls.get(
                (cls.user == user) & (cls.customer == customer)
                & (cls.class_ == class_))
        except cls.DoesNotExist:
            acl = cls()
            acl.user = user
            acl.customer = customer
            acl.class_ = class_
            return acl
