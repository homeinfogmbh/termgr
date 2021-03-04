"""ORM models for termgr."""

from __future__ import annotations
from datetime import date, datetime, timedelta
from xml.etree.ElementTree import Element, SubElement
from typing import Iterable

from peewee import JOIN, DateTimeField, ForeignKeyField, ModelSelect

from his import Account
from mdb import Address, Company, Customer
from hwdb import Deployment, System
from peeweeplus import MySQLDatabase, JSONModel

from termgr.config import CONFIG


__all__ = ['DeploymentHistory']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])
HTML_TABLE_HEADERS = (
    'Techniker',
    'System',
    'Alter Standort',
    'Neuer Standort',
    'Zeitstempel'
)


class TermgrModel(JSONModel):   # pylint: disable=R0903
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class DeploymentHistory(TermgrModel):
    """Deployment actions of technitians."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'deployment_history'

    account = ForeignKeyField(
        Account, column_name='account', on_update='CASCADE',
        on_delete='CASCADE', lazy_load=False)
    system = ForeignKeyField(
        System, column_name='system', on_update='CASCADE', on_delete='CASCADE',
        lazy_load=False)
    old_deployment = ForeignKeyField(
        Deployment, null=True, column_name='old_deployment',
        on_update='CASCADE', on_delete='SET NULL', lazy_load=False)
    new_deployment = ForeignKeyField(
        Deployment, null=True, column_name='new_deployment',
        on_update='CASCADE', on_delete='CASCADE', lazy_load=False)
    timestamp = DateTimeField(default=datetime.now)

    def __str__(self):
        """Returns a string for the terminal."""
        return '\t'.join(
            (self.timestamp.isoformat(), self.account.name,
             str(self.system_id), str(self.old_deployment_id),
             str(self.new_deployment_id))
        )

    @classmethod
    def add(cls, account: Account, system: System, old_deployment: Deployment):
        """Creates and saves a new record."""
        record = cls(
            account=account.id, system=system, old_deployment=old_deployment,
            new_deployment=system.deployment)
        record.save()
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects deployment histories."""
        if not cascade:
            return super().select(*args, **kwargs)

        new_deployment = Deployment.alias()
        new_deployment_customer = Customer.alias()
        new_deployment_company = Company.alias()
        new_deployment_address = Address.alias()
        args = {
            cls, Account, System, Deployment, Customer, Company, Address,
            new_deployment, new_deployment_address, new_deployment_customer,
            new_deployment_company, *args
        }
        return super().select(*args, **kwargs).join(Account).join_from(
            cls, System).join_from(
            # Old deployment.
            cls, Deployment, on=cls.old_deployment == Deployment.id,
            join_type=JOIN.LEFT_OUTER).join(
            Customer, join_type=JOIN.LEFT_OUTER).join(
            Company, join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, Address, on=Deployment.address == Address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            # New deployment.
            cls, new_deployment, on=cls.new_deployment == new_deployment.id,
            join_type=JOIN.LEFT_OUTER).join(
            new_deployment_customer, join_type=JOIN.LEFT_OUTER).join(
            new_deployment_company, join_type=JOIN.LEFT_OUTER).join_from(
            new_deployment, new_deployment_address,
            on=new_deployment.address == new_deployment_address.id,
            join_type=JOIN.LEFT_OUTER)

    @classmethod
    def of_today(cls) -> ModelSelect:
        """Yields deployments that were made today."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        condition = (cls.timestamp >= today) & (cls.timestamp < tomorrow)
        return cls.select(cascade=True).where(condition)

    @classmethod
    def html_table_header(cls) -> Element:
        """Returns an HTML DOM of the table header."""
        row = Element('tr')

        for text in HTML_TABLE_HEADERS:
            header = SubElement(row, 'th')
            header.text = text

        return row

    @property
    def html_table_columns(self) -> Iterable[str]:
        """Yields the column contents for the HTML table representation."""
        yield self.account.full_name or self.account.name
        yield str(self.system.id)
        yield self.old_deployment.to_html()
        yield self.new_deployment.to_html()
        yield self.timestamp.isoformat()    # pylint: disable=E1101

    def to_html_table_row(self) -> Element:
        """Returns an HTML DOM of a table row."""
        row = Element('tr')

        for value in self.html_table_columns:
            table_column = SubElement(row, 'td')

            if isinstance(value, Element):
                table_column.append(value)
            else:
                table_column.text = value

        return row
