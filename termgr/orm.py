"""ORM models for termgr."""

from datetime import date, datetime, timedelta
from xml.etree.ElementTree import Element, SubElement

from peewee import CharField, DateTimeField, ForeignKeyField

from his import Account
from hwdb import Deployment, System
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from termgr.config import CONFIG


__all__ = ['ManufacturerEmail', 'Deployments']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class TermgrModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class ManufacturerEmail(TermgrModel):
    """Maps emails to manufacturer customers."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'manufacturer_emails'

    manufacturer = ForeignKeyField(
        Customer, column_name='manufacturer', on_delete='CASCADE',
        on_update='CASCADE')
    email = CharField(255)


class Deployments(TermgrModel):
    """Deployment actions of technitians."""

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE')
    system = ForeignKeyField(
        System, column_name='system', on_update='CASCADE', on_delete='CASCADE')
    deployment = ForeignKeyField(
        Deployment, column_name='deployment', on_update='CASCADE',
        on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, account, system, deployment, timestamp=None):
        """Creates and saves a new record."""
        record = cls(
            account=account.id, system=system, deployment=deployment,
            timestamp=timestamp or datetime.now())
        record.save()
        return record

    @classmethod
    def of_today(cls):
        """Yields deployments that were made today."""
        today = date.today()
        start = datetime(today.year, today.month, today.day)
        tomorrow = today + timedelta(days=1)
        end = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        return cls.select().where(
            (cls.timestamp >= start) & (cls.timestamp < end))

    def to_html_table_row(self):
        """Returns an HTML DOM."""
        row = Element('tr')
        column = SubElement(row, 'td')
        column.text = self.account.full_name or self.account.name
        column = SubElement(row, 'td')
        column.text = str(self.system.id)
        column = SubElement(row, 'td')
        column.text = self.deployment.customer.name
        column = SubElement(row, 'td')
        column.text = str(self.deployment.customer.id)
        column = SubElement(row, 'td')
        column.text = self.deployment.type.value
        column = SubElement(row, 'td')
        column.text = str(self.deployment.address)
        column = SubElement(row, 'td')
        column.text = self.timestamp.isoformat()
        return row
