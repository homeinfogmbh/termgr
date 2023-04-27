"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from logging import getLogger
from xml.etree.ElementTree import tostring, Element, SubElement
from typing import Iterable, List

from emaillib import Mailer, EMail

from termgr.config import get_config
from termgr.orm import DeploymentHistory


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


def get_mailer() -> Mailer:
    """Returns the mailer from the configuration."""

    return Mailer(
        (config := get_config()).get('mail', 'host'),
        config.get('mail', 'port'),
        config.get('mail', 'user'),
        config.get('mail', 'passwd')
    )


def get_admins() -> Iterable[str]:
    """Yields admins' emails."""

    emails_ = get_config().get('notify', 'admins', fallback='').split(',')
    return filter(None, map(lambda email: email.strip(), emails_))


def get_html(deployments: List[DeploymentHistory]) -> Element:
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
    table.append(DeploymentHistory.html_table_header())

    for deployment in deployments:
        table.append(deployment.to_html_table_row())

    return html


def get_emails(subject: str, html: Element) -> Iterable[EMail]:
    """Yields emails with HTML body."""

    html = tostring(html, encoding='unicode', method='html')
    sender = get_config().get('mail', 'from')

    for admin in get_admins():
        yield EMail(subject, sender, admin, html=html)


def notify(deployments: Iterable[DeploymentHistory] = None) -> bool:
    """Notifies the administrators about deployments."""

    if deployments is None:
        deployments = DeploymentHistory.of_today()

    deployments = deployments.order_by(DeploymentHistory.timestamp.desc())

    if not deployments:
        return False

    emails = get_emails('Verbaute HOMEINFO Systeme', get_html(deployments))
    get_mailer().send(emails)
    return True
