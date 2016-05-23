"""ORM models for termgr"""

from hashlib import sha256
from uuid import uuid4

from peewee import DoesNotExist, Model, PrimaryKeyField, CharField,\
BooleanField, ForeignKeyField

from homeinfo.peewee import MySQLDatabase

from homeinfo.terminals.orm import Terminal

from .config import CONFIG

__all__ = ['PermissionError', 'User', 'Permissions']


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
            CONFIG.db['db'],
            host=CONFIG.db['host'],
            user=CONFIG.db['user'],
            passwd=CONFIG.db['passwd'],
            closing=True)
        schema = database.database


class User(TermgrModel):
    """A generic abstract user"""

    name = CharField(64)
    pwhash = CharField(64)
    salt = CharField(36)
    enabled = BooleanField()
    annotation = CharField(255, null=True)
    root = BooleanField(default=False)

    @classmethod
    def authenticate(cls, name, passwd):
        """Authenticate with name and hashed password"""
        if passwd:
            try:
                user = cls.get(cls.name == name)
            except DoesNotExist:
                return False
            else:
                if user.passwd and passwd:
                    pwstr = passwd + user.salt
                    pwhash = sha256(pwstr.encode()).hexdigest()
                    if user.pwhash == pwhash:
                        if user.enabled:
                            return user
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            return False

    @property
    def passwd(self):
        """Returns the password hash"""
        return self.pwhash

    @passwd.setter
    def passwd(self, passwd, save=True):
        """Creates a new password hash"""
        salt = str(uuid4())
        pwstr = passwd + salt
        pwhash = sha256(pwstr.encode()).hexdigest()
        self.salt = salt
        self.pwhash = pwhash

        if save:
            self.save()

    def permissions(self, terminal):
        """Returns permissions on terminal"""
        return Permissions.get(
            (Permissions.user == self) &
            (Permissions.terminal == terminal))

    def permit(self, terminal, read=None, administer=None, setup=None):
        """Set permissions"""
        if self.root:
            raise PermissionError('Cannot set permissions for root users')
        elif read is False and administer is False and setup is False:
            # Remove all permissions
            for permissions in Permissions.select().where(
                    (Permissions.user == self) &
                    (Permissions.terminal == terminal)):
                permissions.delete_instance()
        else:
            try:
                permissions = self.permissions(terminal)
            except DoesNotExist:
                permissions = Permissions()
                permissions.user = self
                permissions.terminal = terminal

            if read is not None:
                permissions.read = read

            if administer is not None:
                permissions.administer = administer

            if setup is not None:
                permissions.setup = setup

            permissions.save()

    def authorize(self, terminal, read=False, administer=None, setup=None):
        """Validate permissions"""
        if read is None and administer is None and setup is None:
            raise PermissionError('No permissions selected')
        elif self.root:
            return True
        else:
            try:
                permissions = self.permissions(terminal)
            except DoesNotExist:
                raise Exception('DEBUG1')
                return False
            else:
                if read is not None:
                    if permissions.read != read:
                        raise Exception('DEBUG2')
                        return False

                if administer is not None:
                    if permissions.administer != administer:
                        raise Exception('DEBUG3')
                        return False

                if setup is not None:
                    if permissions.setup != setup:
                        raise Exception('DEBUG4')
                        return False

                return True


class Permissions(TermgrModel):
    """Many-to-many mapping in-between administrators and terminals"""

    user = ForeignKeyField(User, db_column='user')

    # Actual privileges
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    terminal = ForeignKeyField(Terminal, db_column='terminal')
