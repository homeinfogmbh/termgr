"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from logging import getLogger
from xml.etree.ElementTree import tostring, Element, SubElement
from typing import Iterable, List

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


def get_admins() -> Iterable[str]:
    """Yields admins's emails."""

    emails_ = CONFIG['notify']['admins'].split(',')
    return filter(None, map(lambda email: email.strip(), emails_))


def get_html(deployments: List[Deployments]) -> Element:
    """Returns an HTML element."""

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

    return html


def get_emails(subject: str, html: str) -> Iterable[EMail]:
    """Yields emails with HTML body."""

    html = tostring(html, encoding='unicode', method='html')

    for admin in get_admins():
        yield EMail(subject, CONFIG['mail']['from'], admin, html=html)


def notify(deployments: Iterable[Deployments] = None) -> bool:
    """Notifies the adminstrators about deployments."""

    if deployments is None:
        deployments = Deployments.of_today()

    deployments = deployments.order_by(Deployments.timestamp.desc())

    if not deployments:
        return False

    emails = get_emails('Verbaute HOMEINFO Systeme', get_html(deployments))
    MAILER.send(emails, background=False)
    return True
