"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from collections import defaultdict
from email.mime.application import MIMEApplication
from logging import getLogger

from emaillib import Mailer, EMail

from termgr.config import CONFIG
from termgr.openvpn import OpenVPNPackager
from termgr.orm import User, WatchList, ReportedTerminal

__all__ = ['notify_accounts']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])


def get_terminals(account):
    """Generates the terminals email."""

    terminals = defaultdict(list)

    for watchlist in WatchList.select().where(WatchList.account == account):
        for terminal in watchlist.terminals:
            terminals[watchlist].append(terminal)

    return terminals


def gen_emails(recipient, wl_terminals):
    """Generates the terminals email."""

    email = EMail(
        CONFIG['notify']['subject'], CONFIG['mail']['from'], recipient,
        CONFIG['notify']['body'])
    empty = True

    for watchlist, terminals in wl_terminals.items():
        lines = [terminal.to_csv() for terminal in terminals]

        if lines:
            # Use DOS line breaks for compatibility with Windows systems.
            csv = '\r\n'.join(str(line) for line in lines)
            attachment = MIMEApplication(csv.encode(), Name=watchlist.filename)
            email.attach(attachment)
            empty = False

    if not empty:
        yield email


def mail_terminals(account):
    """Mails the respective terminals."""

    if user.email is None:
        LOGGER.error(
            'No email address configured for account "%s".', account.name)
        return False

    terminals = get_terminals(account)
    emails = tuple(gen_emails(account.email, terminals))
    MAILER.send(emails)
    incomplete = []

    for terminals_ in terminals.values():
        for terminal in terminals_:
            if not OpenVPNPackager(terminal).complete:
                incomplete.append(terminal)

            reported_terminal = ReportedTerminal.add(account, terminal)
            reported_terminal.save()

    if incomplete:
        list_ = ', '.join(str(terminal) for terminal in incomplete)
        email = EMail(
            'Terminals without OpenVPN config.',
            CONFIG['mail']['from'], CONFIG['notify']['admin'], list_)
        MAILER.send([email])
        return False

    return True


def notify_accounts(accounts=None):
    """Notifies the respective users about new terminals."""

    if accounts is None:
        accounts = Account

    for account in users:
        mail_terminals(account)
