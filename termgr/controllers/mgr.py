"""Controller for terminal management management"""

from datetime import datetime
from homeinfolib.mime import mimetype
from homeinfolib.wsgi import WsgiController, Error
from terminallib.db import Terminal
from ..lib.db2xml import terminal2xml
from ..lib.termgr import termgr
from homeinfo.crm.address import Address

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalManager']


class TerminalDetails():
    """Terminal details wrapper"""

    @classmethod
    def mockup(cls):
        """Mockup for testing"""
        with open('/home/rne/asdm04.jpg', 'rb') as f:
            data = f.read()
        status = 'UP'
        uptime = 10000
        screenshot = (datetime.now(), mimetype(data), data)
        touch_events = [(datetime.now(), 0, 1, 3),
                        (datetime.now(), 123, 423, 54)]
        return cls(status, uptime, screenshot, touch_events)

    def __init__(self, status, uptime, screenshot, touch_events):
        """Sets detail data"""
        self._status = status
        self._uptime = uptime
        self._screenshot = screenshot
        self._touch_events = touch_events

    @property
    def status(self):
        """Returns the status"""
        return self._status

    @property
    def uptime(self):
        """Returns the uptime"""
        return self._uptime

    @property
    def screenshot(self):
        """Returns the screenshot"""
        return self._screenshot

    @property
    def touch_events(self):
        """Returns the touch events"""
        return self._touch_events


class TerminalManager(WsgiController):
    """Manages terminals"""

    def _run(self):
        """Runs the terminal manager"""
        cid = self._query_dict.get('cid')
        if cid is not None:
            try:
                cid = int(cid)
            except (TypeError, ValueError):
                return Error('Invalid customer ID', status=400)
        tid = self._query_dict.get('tid')
        if tid is not None:
            tid = int(tid)
        cls = self._query_dict.get('cls')
        if cls is not None:
            cls = int(cls)
        action = self._query_dict.get('action')
        if action == 'list':
            return self._list_terminals(cid, cls)
        elif action == 'details':
            return self._details(cid, tid)
        else:
            return None

    def _list_terminals(self, cid, cls):
        """Lists available terminals"""
        if cid is None:
            if cls is None:
                terminals = Terminal.iselect(True)  # @UndefinedVariable
            else:
                terminals = Terminal.iselect(   # @UndefinedVariable
                    Terminal._cls == cls)
        else:
            if cls is None:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    Terminal.customer == cid)
            else:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    (Terminal.customer == cid) & (Terminal._cls == cls))
        result = termgr()
        for terminal in terminals:
            xml_data = terminal2xml(terminal)
            result.terminal.append(xml_data)
        return result

    def _details(self, cid, tid):
        """Get details of a certain terminal"""
        result = termgr()
        if cid is None or tid is None:
            return result  # TODO: handle error
        else:
            terminal = Terminal.iget(   # @UndefinedVariable
                (Terminal.customer == cid)
                & (Terminal.tid == tid))
            details = TerminalDetails.mockup()  # XXX: Testing
            terminal_detail = terminal2xml(terminal, cid=True, details=details)
            result.terminal_detail = terminal_detail
            return result

    def _add(self, cid, tid, street, house_number, zip_code, city, cls=None,
             domain=None, ipv4addr=None, virtual_display=None):
        """Adds a terminal with the specified configuration"""
        term = Terminal.by_ids(cid, tid)
        if term is None:
            term = Terminal()
            term.customer = cid
            term.tid = tid
            addr = Address.iselect(  # @UndefinedVariable
                (Address.street == street) &
                (Address.house_number == house_number) &
                (Address.zip == zip_code) &
                (Address.city == city))
            addr = Address()
            addr.street = street
            addr
