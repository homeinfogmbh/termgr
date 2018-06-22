"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from collections import defaultdict
from email.mime.application import MIMEApplication
from logging import getLogger

from emaillib import Mailer, EMail

from termgr.config import CONFIG
from termgr.openvpn import OpenVPNPackager
from termgr.orm import User, WatchList, ReportedTerminal
from termgr.util import TerminalCSVRecord

__all__ = ['notify_users']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])


def get_terminals(user):
    """Generates the terminals email."""

    terminals = defaultdict(list)

    for watchlist in WatchList.select().where(WatchList.user == user):
        for terminal in watchlist.terminals:
            terminals[watchlist].append(terminal)

    return terminals


def gen_emails(recipient, terminals_):
    """Generates the terminals email."""

    email = EMail(
        CONFIG['notify']['subject'], CONFIG['mail']['from'], recipient,
        CONFIG['notify']['body'])
    empty = True

    for watchlist, terminals in terminals_.items():
        filename = watchlist.customer.name or ''
        filename += '_' + watchlist.class_.name + '.csv'
        lines = [TerminalCSVRecord.from_terminal(term) for term in terminals]

        if lines:
            # Use DOS line breaks for compatibility with Windows systems.
            csv_file = '\r\n'.join(str(line) for line in lines)
            attachment = MIMEApplication(csv_file.encode(), Name=filename)
            email.attach(attachment)
            empty = False

    if not empty:
        yield email


def mail_terminals(user):
    """Mails the respective terminals."""

    if user.email is None:
        LOGGER.error('No email address configured for user "%s".', user.name)
        return False

    terminals = get_terminals(user)
    MAILER.send(user.email, terminals)
    incomplete = []

    for _, terminals_ in terminals:
        for terminal in terminals_:
            if not OpenVPNPackager(terminal).complete:
                incomplete.append(terminal)

            reported_terminal = ReportedTerminal.add(user, terminal)
            reported_terminal.save()

    if incomplete:
        list_ = ', '.join(str(terminal) for terminal in incomplete)
        email = EMail(
            'Terminals without OpenVPN config.',
            CONFIG['mail']['from'], CONFIG['notify']['admin'], list_)
        MAILER.send([email])
        return False

    return True


def notify_users(users=None):
    """Notifies the respective users about new terminals."""

    if users is None:
        users = User

    for user in users:
        mail_terminals(user)
