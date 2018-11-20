"""ORM models for termgr."""

from datetime import datetime

from peewee import ForeignKeyField, BooleanField, DateTimeField

from his import Account
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, ChangedConnection
from terminallib import Class, Terminal

from termgr.config import CONFIG

__all__ = [
    'ACL',
    'DefaultACL',
    'WatchList',
    'ReportedTerminal']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class TermgrModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:
        """Configures the database and schema."""
        database = DATABASE
        schema = database.database


class _ACLMixin:
    """ACL base interface."""

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


class ACL(_ACLMixin, TermgrModel):
    """Many-to-many mapping in-between administrators
    and terminals with certain permissions.
    """

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE')
    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_update='CASCADE',
        on_delete='CASCADE')
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    @classmethod
    def add(cls, account, terminal, *, read=None, administer=None, setup=None):
        """Adds the respective ACL entry."""
        try:
            acl = cls.get(
                (cls.account == account)
                & (cls.terminal == terminal))
        except cls.DoesNotExist:
            acl = cls()
            acl.account = account
            acl.terminal = terminal

        if read is not None:
            acl.read = read

        if administer is not None:
            acl.administer = administer

        if setup is not None:
            acl.setup = setup

        return acl

    @classmethod
    def authorize(cls, account, terminal, *, read=None, administer=None,
                  setup=None):
        """Authorize via per-terminal ACLs."""
        if read is None:
            read_expr = True
        else:
            read_expr = cls.read == read

        if administer is None:
            administer_expr = True
        else:
            administer_expr = cls.administer == administer

        if setup is None:
            setup_expr = True
        else:
            setup_expr = cls.setup == setup

        try:
            cls.get(
                (cls.account == account)
                & (cls.terminal == terminal)
                & read_expr
                & administer_expr & setup_expr)
        except cls.DoesNotExist:
            return False

        return True

    def commit(self):
        """Commits the ACLs."""
        if self.read or self.administer or self.setup:
            return self.save()

        return self.delete_instance()


class DefaultACL(_ACLMixin, TermgrModel):
    """Represents default ACL settings for users."""

    class Meta:
        """Sets the respective table name."""
        table_name = 'default_acl'

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_update='CASCADE',
        on_delete='CASCADE')
    class_ = ForeignKeyField(
        Class, column_name='class', on_update='CASCADE', on_delete='CASCADE')
    read = BooleanField(default=False)
    administer = BooleanField(default=False)
    setup = BooleanField(default=False)

    def __str__(self):
        """Suffixes string representation with default marker."""
        return super().__str__() + ' (default)'

    @classmethod
    def add(cls, account, customer, class_, *, read=None, administer=None,
            setup=None):
        """Adds new default ACLs."""
        try:
            acl = cls.get(
                (cls.account == account)
                & (cls.customer == customer)
                & (cls.class_ == class_))
        except cls.DoesNotExist:
            acl = cls()
            acl.account = account
            acl.customer = customer
            acl.class_ = class_

        acl.read = read
        acl.administer = administer
        acl.setup = setup
        return acl

    @classmethod
    def authorize(cls, account, customer, class_, *, read=None,
                  administer=None, setup=None):
        """Authorize via default ACLs."""
        if read is None:
            read_expr = True
        else:
            read_expr = cls.read == read

        if administer is None:
            administer_expr = True
        else:
            administer_expr = cls.administer == administer

        if setup is None:
            setup_expr = True
        else:
            setup_expr = cls.setup == setup

        try:
            cls.get(
                (cls.account == account) & (cls.customer == customer)
                & (cls.class_ == class_) & read_expr & administer_expr
                & setup_expr)
        except cls.DoesNotExist:
            return False

        return True

    @classmethod
    def for_terminal(cls, terminal):
        """Yields the respective default ACLs for the respective terminal."""
        return cls.select().where(
            (cls.customer == terminal.customer)
            & (cls.class_ == terminal.class_))

    @property
    def terminals(self):
        """Yields the respective terminals
        associated with the default ACL entry.
        """
        return Terminal.select().where(
            (Terminal.customer == self.customer)
            & (Terminal.class_ == self.class_))


class WatchList(TermgrModel):
    """Mapping in-between accounts, customers and terminal
    classes to notify users about new terminals.
    """

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_update='CASCADE',
        on_delete='CASCADE')
    class_ = ForeignKeyField(
        Class, column_name='class', on_update='CASCADE', on_delete='CASCADE')

    @classmethod
    def add(cls, account, customer, class_):
        """Adds new default ACLs."""
        try:
            return cls.get(
                (cls.account == account) & (cls.customer == customer)
                & (cls.class_ == class_))
        except cls.DoesNotExist:
            acl = cls()
            acl.account = account
            acl.customer = customer
            acl.class_ = class_
            return acl

    @property
    def filename(self):
        """Returns the appropriate file name."""
        return self.customer.name + '_' + self.class_.name + '.csv'

    @property
    def notified(self):
        """Yields terminals that were already notified about."""
        for rterm in ReportedTerminal.select().join(Terminal).where(
                (ReportedTerminal.account == self.account)
                & (Terminal.customer == self.customer)
                & (Terminal.class_ == self.class_)):
            yield rterm.terminal

    @property
    def terminals(self):
        """Yields matching, unreported terminals."""
        notified = tuple(terminal.id for terminal in self.notified)

        with ChangedConnection(Terminal, ReportedTerminal):
            for terminal in Terminal.select().where(
                    (Terminal.customer == self.customer)
                    & (Terminal.class_ == self.class_)
                    & (Terminal.testing == 0)
                    & ~(Terminal.id << notified)).order_by(Terminal.tid):
                yield terminal


class ReportedTerminal(TermgrModel):
    """Lists reported terminals for the respective account."""

    class Meta:
        """Sets the respective table name."""
        table_name = 'reported_terminal'

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE')
    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_update='CASCADE',
        on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, account, terminal, timestamp=None):
        """Marks the respective terminal
        as reported for the given account.
        """
        try:
            reported_terminal = cls.get(
                (cls.account == account) & (cls.terminal == terminal))
        except cls.DoesNotExist:
            reported_terminal = cls()
            reported_terminal.account = account
            reported_terminal.terminal = terminal

        if timestamp is not None:
            reported_terminal.timestamp = timestamp

        return reported_terminal
