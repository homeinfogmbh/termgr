"""Terminal query web service."""

from datetime import datetime

from terminallib import Terminal
from wsgilib import Error, JSON, XML

from termgr import dom
from .abc import TermgrHandler

__all__ = ['QueryHandler']


def xml_terminals(terminals):
    """Returns terminals as XML response."""

    terminals_dom = dom.terminals()

    for terminal in terminals:
        terminal_dom = dom.Terminal()
        terminal_dom.tid = terminal.tid
        terminal_dom.cid = terminal.customer.id
        terminal_dom.scheduled = terminal.scheduled
        terminal_dom.deployed = terminal.deployed
        terminal_dom.annotation = terminal.annotation

        if terminal.location:
            address_dom = dom.Address()
            address_dom.annotation = terminal.location.annotation

            if terminal.location.address:
                address = terminal.location.address
                address_dom.street = address.street
                address_dom.house_number = address.house_number
                address_dom.zip_code = address.zip_code
                address_dom.city = address.city

            terminal_dom.address = address_dom

        terminals_dom.terminal.append(terminal_dom)

    return XML(terminals_dom)


class QueryHandler(TermgrHandler):
    """Handles requests for the TerminalQuery."""

    @property
    def cid(self):
        """Returns the customer ID."""
        try:
            cid = self.query['cid']
        except KeyError:
            return None
        else:
            try:
                return int(cid)
            except ValueError:
                raise Error('Invalid customer ID.', status=400) from None

    @property
    def scheduled(self):
        """Returns the scheduled date."""
        try:
            scheduled = self.query['scheduled']
        except KeyError:
            return None
        else:
            try:
                scheduled = datetime.strptime(scheduled, '%Y-%m-%d')
            except ValueError:
                raise Error('Invalid ISO date: {}.'.format(
                    scheduled)) from None
            else:
                return scheduled.date()

    @property
    def terminals(self):
        """List terminals of customer with CID."""

        cid = self.cid
        scheduled = self.scheduled
        undeployed = self.query.get('undeployed', False)

        if cid is None:
            terminals = Terminal
        else:
            terminals = Terminal.select().where(
                (Terminal.customer == cid) &
                (Terminal.testing == 0))

        for terminal in terminals:
            if terminal.testing:
                continue

            if scheduled is not None:
                if terminal.scheduled is None:
                    continue
                elif terminal.scheduled.date() != scheduled:
                    continue

            if undeployed and terminal.deployed is not None:
                continue

            if self.user.authorize(terminal, read=True):
                yield terminal

    @property
    def json(self):
        """Returns the JSON indentation."""
        try:
            json = self.query['json']
        except KeyError:
            return False
        else:
            if json is True:
                return None

            try:
                return int(json)
            except ValueError:
                raise Error('Invalid indentation: {}.'.format(json)) from None

    def get(self):
        """Interpret query dictionary."""
        json = self.json

        if json is False:
            return xml_terminals(self.terminals)

        return JSON(
            [terminal.to_dict(short=True) for terminal in self.terminals],
            indent=json)
