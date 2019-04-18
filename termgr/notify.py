"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from collections import defaultdict
from email.mime.application import MIMEApplication
from logging import getLogger

from emaillib import Mailer, EMail
from his import Account

from termgr.config import CONFIG
from termgr.openvpn import OpenVPNPackager
from termgr.orm import WatchList, ReportedTerminal

__all__ = ['notify_accounts']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])


def systems_dict(systems):
    """Generates the terminals email."""

    systems_by_manufacturer = defaultdict(list)

    for system in systems:
        if system.manufacturer is None:
            continue

        systems_by_manufacturer[manufacturer].append(system)

    return systems_by_manufacturer


def generate_email(email, systems):
    """Generates an email for the respective
    manufacturer's email address.
    """

    email = EMail(
        CONFIG['notify']['subject'], CONFIG['mail']['from'], email,
        CONFIG['notify']['body'])
    records = [
        (
            str(system.id),
            system.created.isoformat(),
            system.operating_system.value
        )
        for system in systems
    ]
    csv = '\r\n'.join(','.join(record) for record in records)
    attachment = MIMEApplication(csv.encode(), Name='systems.csv')
    email.attach(attachment)
    return email


def generate_emails(systems):
    """Mails the respective terminals."""

    for manufacturer, systems in systems_dict(systems):
        if systems:
            for manufacturer_email in ManufacturerEmail.select().where(
                    ManufacturerEmail.manufacturer == manufacturer):
                yield generate_email(manufacturer_email.email, systems)


def notify_manufacturers(systems):
    """Notifies the respective manufacturers about systems."""

    if accounts is None:
        accounts = Account

    for account in accounts:
        mail_terminals(account)
