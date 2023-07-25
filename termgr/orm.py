"""ORM models for termgr."""

from __future__ import annotations
from datetime import date, datetime, timedelta
from xml.etree.ElementTree import Element, SubElement
from typing import Any, Iterable

from peewee import JOIN, DateTimeField, ForeignKeyField, Select

from his import Account
from mdb import Address, Company, Customer
from hwdb import Deployment, System
from peeweeplus import MySQLDatabaseProxy, JSONModel


__all__ = ["DeploymentHistory"]


DATABASE = MySQLDatabaseProxy("termgr")
HTML_TABLE_HEADERS = (
    "Techniker",
    "System",
    "Alter Standort",
    "Neuer Standort",
    "Zeitstempel",
)


class TermgrModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:
        database = DATABASE
        schema = database.database


class DeploymentHistory(TermgrModel):
    """Deployment actions of technitians."""

    FIELDS = ["Timestamp           ", "Account", "System", "Old", "New"]

    class Meta:
        table_name = "deployment_history"

    account = ForeignKeyField(
        Account,
        column_name="account",
        on_update="CASCADE",
        on_delete="CASCADE",
        lazy_load=False,
    )
    system = ForeignKeyField(
        System,
        column_name="system",
        on_update="CASCADE",
        on_delete="CASCADE",
        lazy_load=False,
    )
    old_deployment = ForeignKeyField(
        Deployment,
        null=True,
        column_name="old_deployment",
        on_update="CASCADE",
        on_delete="SET NULL",
        lazy_load=False,
    )
    new_deployment = ForeignKeyField(
        Deployment,
        null=True,
        column_name="new_deployment",
        on_update="CASCADE",
        on_delete="CASCADE",
        lazy_load=False,
    )
    timestamp = DateTimeField(default=datetime.now)

    def __str__(self):
        """Returns a string for the terminal."""
        return "\t".join(
            (
                self.timestamp.isoformat(),
                self.account_name,
                str(self.system_id),
                str(self.old_deployment_id),
                str(self.new_deployment_id),
            )
        )

    @classmethod
    def add(cls, account: Account, system: System, old_deployment: Deployment):
        """Creates and saves a new record."""
        record = cls(
            account=account,
            system=system,
            old_deployment=old_deployment,
            new_deployment=system.deployment,
        )
        record.save()
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects deployment histories."""
        if not cascade:
            return super().select(*args)

        new_deployment = Deployment.alias()
        new_deployment_customer = Customer.alias()
        new_deployment_company = Company.alias()
        new_deployment_address = Address.alias()
        return (
            super()
            .select(
                cls,
                Account,
                System,
                Deployment,
                Customer,
                Company,
                Address,
                new_deployment,
                new_deployment_address,
                new_deployment_customer,
                new_deployment_company,
                *args,
            )
            .join(Account)
            .join_from(cls, System)
            .join_from(
                # Old deployment.
                cls,
                Deployment,
                on=cls.old_deployment == Deployment.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join(Customer, join_type=JOIN.LEFT_OUTER)
            .join(Company, join_type=JOIN.LEFT_OUTER)
            .join_from(
                Deployment,
                Address,
                on=Deployment.address == Address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                # New deployment.
                cls,
                new_deployment,
                on=cls.new_deployment == new_deployment.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join(new_deployment_customer, join_type=JOIN.LEFT_OUTER)
            .join(new_deployment_company, join_type=JOIN.LEFT_OUTER)
            .join_from(
                new_deployment,
                new_deployment_address,
                on=new_deployment.address == new_deployment_address.id,
                join_type=JOIN.LEFT_OUTER,
            )
        )

    @classmethod
    def of_today(cls) -> Select:
        """Yields deployments that were made today."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        condition = (cls.timestamp >= today) & (cls.timestamp < tomorrow)
        return cls.select(cascade=True).where(condition)

    @classmethod
    def html_table_header(cls) -> Element:
        """Returns an HTML DOM of the table header."""
        row = Element("tr")

        for text in HTML_TABLE_HEADERS:
            header = SubElement(row, "th")
            header.text = text

        return row

    @property
    def account_name(self) -> str:
        """Returns the account name."""
        try:
            return self.account.name
        except AttributeError:
            return str(self.account)

    @property
    def html_table_columns(self) -> Iterable[str]:
        """Yields the column contents for the HTML table representation."""
        yield self.account.full_name or self.account.name
        yield str(self.system.id)

        if self.old_deployment is None:
            yield "N/A"
        else:
            yield self.old_deployment.to_html()

        if self.new_deployment is None:
            yield "-"
        else:
            yield self.new_deployment.to_html()

        yield self.timestamp.isoformat()

    @property
    def shallow_json(self) -> dict[str, Any]:
        """Return a shallow JSON representation with minimal information."""
        return {
            "id": self.id,
            "account": {
                "id": self.account.id,
                "name": self.account.name,
                "fullName": self.account.full_name,
            },
            "system": self.system_id,
            "oldDeployment": self.old_deployment_id,
            "newDeployment": self.new_deployment_id,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_html_table_row(self) -> Element:
        """Returns an HTML DOM of a table row."""
        row = Element("tr")

        for value in self.html_table_columns:
            table_column = SubElement(row, "td")

            if isinstance(value, Element):
                table_column.append(value)
            else:
                table_column.text = value

        return row

    def to_json(self, *, shallow: bool = False, **kwargs) -> dict[str, Any]:
        """Return a JSON-ish dict."""

        if shallow:
            return self.shallow_json

        return super().to_json(**kwargs)
