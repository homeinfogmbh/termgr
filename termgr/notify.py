"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from collections import defaultdict
from email.mime.application import MIMEApplication
from logging import getLogger
from xml.etree.ElementTree import tostring, Element, SubElement

from emaillib import Mailer, EMail
from functoolsplus import coerce

from termgr.config import CONFIG
from termgr.orm import Deployments, ManufacturerEmail


__all__ = ['notify_manufacturers', 'notify_todays_deployments']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])


def admins():
    """Yields admins's emails."""

    emails_ = CONFIG['notify']['admins'].split(',')
    return filter(None, map(lambda email: email.strip(), emails_))


def systems_dict(systems):
    """Generates the terminals email."""

    systems_by_manufacturer = defaultdict(list)

    for system in systems:
        if system.manufacturer is None:
            continue

        systems_by_manufacturer[system.manufacturer].append(system)

    return systems_by_manufacturer


def generate_manufacturer_email(email, systems):
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


def generate_manufacturer_emails(systems):
    """Mails the respective terminals."""

    for manufacturer, systems in systems_dict(systems):  # pylint:disable=R1704
        if systems:
            for manufacturer_email in ManufacturerEmail.select().where(
                    ManufacturerEmail.manufacturer == manufacturer):
                yield generate_manufacturer_email(manufacturer_email.email, systems)


@coerce(tuple)
def get_html_emails(subject, html):
    """Send emails to admins."""

    html = tostring(html, encoding='unicode', method='html')

    for admin in admins():
        yield EMail(subject, CONFIG['mail']['from'], admin, html=html)


def notify_manufacturers(systems):
    """Notifies the respective manufacturers about systems."""

    emails = tuple(generate_manufacturer_emails(systems))
    MAILER.send(emails)


def notify_todays_deployments():
    """Notifies the adminstrators about deployments."""

    deployments = tuple(Deployments.of_today())

    if not systems:
        return False

    html = Element('html')
    header = SubElement(html, 'header')
    SubElement(header, 'meta', attrib={'charset': 'UTF-8'})
    title = SubElement(header, 'title')
    title.text = 'Ein HOMEINFO System wurde verbaut'
    body = SubElement(html, 'body')
    salutation = SubElement(body, 'span')
    salutation.text = 'Sehr geehrter Administrator,'
    SubElement(body, 'br')
    SubElement(body, 'br')
    text = SubElement(body, 'span')

    if len(deployments) == 1:
        text.text = 'das folgende HOMEINFO System wurde heute verbaut:'
    else:
        text.text = 'die folgenden HOMEINFO System wurden heute verbaut:'

    SubElement(body, 'br')
    SubElement(body, 'br')
    table = SubElement(body, 'table', attrib={'border': '1'})
    row = SubElement(table, 'tr')
    header = SubElement(row, 'th')
    header.text = 'Techniker'
    header = SubElement(row, 'th')
    header.text = 'System'
    header = SubElement(row, 'th')
    header.text = 'Kunde'
    header = SubElement(row, 'th')
    header.text = 'Kundennummer'
    header = SubElement(row, 'th')
    header.text = 'Typ'
    header = SubElement(row, 'th')
    header.text = 'Standort'
    header = SubElement(row, 'th')
    header.text = 'Zeitstempel'

    for deployment in deployments:
        table.append(deployment.to_html_table_row())

    emails = get_html_emails('Verbaute HOMEINFO Systeme', html)
    MAILER.send(emails)
    return True
