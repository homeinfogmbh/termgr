"""ORM models for termgr."""

from datetime import date, datetime, timedelta
from xml.etree.ElementTree import Element, SubElement

from peewee import DateTimeField, ForeignKeyField

from his import Account
from hwdb import Deployment, System
from peeweeplus import MySQLDatabase, JSONModel

from termgr.config import CONFIG


__all__ = ['Deployments']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])
HTML_TABLE_HEADERS = (
    'Techniker',
    'System',
    'Kunde',
    'Kundennummer',
    'Typ',
    'Standort',
    'Zeitstempel'
)


class TermgrModel(JSONModel):   # pylint: disable=R0903
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


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
        tomorrow = today + timedelta(days=1)
        condition = (cls.timestamp >= today) & (cls.timestamp < tomorrow)
        return cls.select().where(condition)

    @classmethod
    def html_table_header(cls):
        """Returns an HTML DOM of the table header."""
        row = Element('tr')

        for text in HTML_TABLE_HEADERS:
            header = SubElement(row, 'th')
            header.text = text

        return row

    @property
    def html_table_columns(self):
        """Yields the column contents for the HTML table representation."""
        yield self.account.full_name or self.account.name
        yield str(self.system.id)
        yield self.deployment.customer.name
        yield str(self.deployment.customer.id)
        yield self.deployment.type.value
        yield str(self.deployment.address)
        yield self.timestamp.isoformat()    # pylint: disable=E1101

    def to_html_table_row(self):
        """Returns an HTML DOM of a table row."""
        row = Element('tr')

        for column in self.html_table_columns:
            table_column = SubElement(row, 'td')
            table_column.text = column

        return row
