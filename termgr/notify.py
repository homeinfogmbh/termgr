"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from logging import getLogger
from xml.etree.ElementTree import tostring, Element, SubElement

from emaillib import Mailer, EMail
from functoolsplus import coerce

from termgr.config import CONFIG
from termgr.orm import Deployments


__all__ = ['notify_todays_deployments']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])


def admins():
    """Yields admins's emails."""

    emails_ = CONFIG['notify']['admins'].split(',')
    return filter(None, map(lambda email: email.strip(), emails_))


@coerce(tuple)
def get_html_emails(subject, html):
    """Send emails to admins."""

    html = tostring(html, encoding='unicode', method='html')

    for admin in admins():
        yield EMail(subject, CONFIG['mail']['from'], admin, html=html)


def notify_todays_deployments():
    """Notifies the adminstrators about deployments."""

    deployments = tuple(Deployments.of_today().order_by(
        Deployments.timestamp.desc()))

    if not deployments:
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
        text.text = 'die folgenden HOMEINFO Systeme wurden heute verbaut:'

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
    MAILER.send(emails, background=False)
    return True
