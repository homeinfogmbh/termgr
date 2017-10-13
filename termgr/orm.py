"""ORM models for termgr"""

from peewee import DoesNotExist, Model, PrimaryKeyField, CharField,\
    BooleanField, ForeignKeyField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from peeweeplus import MySQLDatabase
from homeinfo.crm import Company
from terminallib import Terminal

from termgr.config import config

__all__ = ['PermissionError', 'User', 'ACL']


class PermissionError(Exception):
    """Indicates error during permission handling"""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class TermgrModel(Model):
    """Terminal manager basic Model"""

    id = PrimaryKeyField()

    class Meta:
        database = MySQLDatabase(
            config['db']['db'],
            host=config['db']['host'],
            user=config['db']['user'],
            passwd=config['db']['passwd'],
            closing=True)
        schema = database.database


class User(TermgrModel):
    """A generic abstract user"""

    company = ForeignKeyField(Company, db_column='company')
    name = CharField(64)
    pwhash = CharField(255)
    enabled = BooleanField()
    annotation = CharField(255, null=True)
    root = BooleanField(default=False)

    passwd_hasher = PasswordHasher()

    def __str__(self):
        """Returns the user's name"""
        return self.name

    @classmethod
    def authenticate(cls, name, passwd):
        """Authenticate with name and hashed password"""
        if passwd:
            try:
                user = cls.get(cls.name == name)
            except DoesNotExist:
                return False
            else:
                try:
                    cls.passwd_hasher.verify(user.pwhash, passwd)
                except VerifyMismatchError:
                    return False
                else:
                    if user.enabled:
                        return user
                    else:
                        return False
        else:
            return False

    @property
    def passwd(self):
        """Returns the password hash"""
        return self.pwhash

    @passwd.setter
    def passwd(self, passwd):
        """Creates a new password hash"""
        self.pwhash = self.__class__.passwd_hasher.hash(passwd)

    def permissions(self, terminal):
        """Returns permissions on terminal"""
        return ACL.get(
            (ACL.user == self) &
            (ACL.terminal == terminal))

    def permit(self, terminal, read=None, administer=None, setup=None):
        """Set permissions"""
        if self.root:
            raise PermissionError('Cannot set permissions for root users')
        else:
            try:
                permissions = self.permissions(terminal)
            except DoesNotExist:
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
        """Validate permissions

        XXX: None means "don't care"!
        """
        if read is None and administer is None and setup is None:
            raise PermissionError('No permissions selected')
        elif not self.enabled:
            return False
        elif self.root:
            return True
        else:
            try:
                permissions = self.permissions(terminal)
            except DoesNotExist:
                return False
            else:
                if read is not None:
                    if permissions.read != read:
                        return False

                if administer is not None:
                    if permissions.administer != administer:
                        return False

                if setup is not None:
                    if permissions.setup != setup:
                        return False

                return True


class ACL(TermgrModel):
    """Many-to-many mapping in-between administrators
    and terminals with certain permissions
    """

    user = ForeignKeyField(User, db_column='user')
    terminal = ForeignKeyField(Terminal, db_column='terminal')
    # Permissions
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    def __int__(self):
        """Returns the permissions value"""
        return 4 * self.read + 2 * self.administer + self.setup

    def __repr__(self):
        """Returns the permissions as a string"""
        return str(int(self))

    def __str__(self):
        """Returns the permissions as an alternative string"""
        return ''.join((
            'r' if self.read else '-',
            'a' if self.administer else '-',
            's' if self.setup else '-'))

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)
