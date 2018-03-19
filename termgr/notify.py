"""New terminals nosification, ACL setting, OpenVPN key checks and mailing."""

from email.mime.application import MIMEApplication
from logging import getLogger

from emaillib import Mailer, EMail

from termgr.config import CONFIG
from termgr.openvpn import OpenVPNPackager
from termgr.orm import User, WatchList, ReportedTerminal

__all__ = ['notify_users']


LOGGER = getLogger(__file__)
MAILER = Mailer(
    CONFIG['mail']['host'], CONFIG['mail']['port'],
    CONFIG['mail']['user'], CONFIG['mail']['passwd'])
SEP = ';'


def terminal_fields(terminal):
    """Yields fields of the terminal for the CSV file."""

    address = None

    if terminal.location:
        address = terminal.location.address

    fields = (str(terminal.tid), terminal.customer.cid)

    if address is not None:
        fields += (address.street or '', address.house_number or '',
                   address.zip_code or '', address.city or '')
    else:
        fields += ('', '', '', '')

    return fields


def terminal_to_csv_record(terminal, sep=SEP):
    """Converts the terminal into a CSV record."""

    return sep.join(terminal_fields(terminal))


def mail_terminals(user):
    """Mails the respective terminals."""

    if user.email is None:
        LOGGER.error('No email address configured for user "%s".', user.name)

    terminals = []
    email = EMail(
        CONFIG['notify']['subject'], CONFIG['mail']['from'], user.email,
        CONFIG['notify']['body'])
    empty = True

    for watchlist in WatchList.select().where(WatchList.user == user):
        lines = []
        filename = watchlist.customer.name or ''
        filename += '_' + watchlist.class_.name + '.csv'

        for terminal in watchlist.terminals:
            terminals.append(terminal)
            lines.append(terminal_to_csv_record(terminal))

        if lines:
            csv_file = '\r\n'.join(lines)   # Use DOS line breaks.
            attachment = MIMEApplication(csv_file.encode(), Name=filename)
            email.attach(attachment)
            empty = False

    if not empty:
        MAILER.send([email])
        incomplete = []

        for terminal in terminals:
            if not OpenVPNPackager(terminal).complete:
                incomplete.append(terminal)

            reported_terminal = ReportedTerminal.add(user, terminal)
            reported_terminal.save()

        if incomplete:
            list_ = ', '.join(str(terminal) for terminal in incomplete)
            email = EMail(
                'Terminals without OpenVPN config.', CONFIG['mail']['from'],
                CONFIG['notify']['admin'], list_)
            MAILER.send([email])


def notify_users(users=None):
    """Notifies the respective users about new terminals."""

    if users is None:
        users = User

    for user in users:
        mail_terminals(user)
