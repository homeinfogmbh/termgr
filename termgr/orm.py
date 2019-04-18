"""ORM models for termgr."""

from peewee import ForeignKeyField

from his import Account
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel
from terminallib import System

from termgr.config import CONFIG


__all__ = ['SystemAdministrator', 'CustomerAdministrator']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class TermgrModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class SystemAdministrator(TermgrModel):
    """A system administrator."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'system_administrator'

    system = ForeignKeyField(
        System, column_name='system', on_delete='CASCADE', on_update='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE',
        on_update='CASCADE')


class CustomerAdministrator(TermgrModel):
    """A customer-related administraor."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_administrator'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE',
        on_update='CASCADE')
