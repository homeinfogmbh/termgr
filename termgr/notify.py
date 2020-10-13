"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from logging import getLogger
from xml.etree.ElementTree import tostring, Element, SubElement

from emaillib import Mailer, EMail

from termgr.config import CONFIG
from termgr.orm import Deployments


__all__ = ['notify']


HEADERS = (
    'Techniker',
    'System',
    'Kunde',
    'Kundennummer',
    'Typ',
    'Standort',
    'Zeitstempel'
)
LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'],
    CONFIG['mail']['port'],
    CONFIG['mail']['user'],
    CONFIG['mail']['passwd']
)


def admins():
    """Yields admins's emails."""

    emails_ = CONFIG['notify']['admins'].split(',')
    return filter(None, map(lambda email: email.strip(), emails_))


def get_html_emails(subject, html):
    """Send emails to admins."""

    html = tostring(html, encoding='unicode', method='html')

    for admin in admins():
        yield EMail(subject, CONFIG['mail']['from'], admin, html=html)


def notify(deployments=None, order=True):
    """Notifies the adminstrators about deployments."""

    if deployments is None:
        deployments = Deployments.of_today()

    if order:
        deployments = deployments.order_by(Deployments.timestamp.desc())

    if not deployments:
        return False

    html = Element('html')
    header = SubElement(html, 'header')
    SubElement(header, 'meta', attrib={'charset': 'UTF-8'})
    body = SubElement(html, 'body')
    salutation = SubElement(body, 'p')
    salutation.text = 'Sehr geehrter Administrator,'
    text = SubElement(body, 'p')

    if len(deployments) == 1:
        text.text = 'das folgende HOMEINFO System wurde heute verbaut:'
    else:
        text.text = 'die folgenden HOMEINFO Systeme wurden heute verbaut:'

    table = SubElement(body, 'table', attrib={'border': '1'})
    table.append(Deployments.html_table_header())

    for deployment in deployments:
        table.append(deployment.to_html_table_row())

    emails = get_html_emails('Verbaute HOMEINFO Systeme', html)
    MAILER.send(emails, background=False)
    return True
